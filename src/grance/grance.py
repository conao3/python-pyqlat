from __future__ import annotations

import inspect
import typing
from collections.abc import Callable
from typing import Any
from typing import TypeAlias

import graphql
import pydantic


GraphQLInputType: TypeAlias = (
    graphql.GraphQLScalarType
    | graphql.GraphQLEnumType
    | graphql.GraphQLInputObjectType
    | graphql.GraphQLWrappingType[Any]
)

GraphQLOutputType: TypeAlias = (
    graphql.GraphQLScalarType
    | graphql.GraphQLObjectType
    | graphql.GraphQLInterfaceType
    | graphql.GraphQLUnionType
    | graphql.GraphQLEnumType
    | graphql.GraphQLWrappingType[Any]
)

GraphQLNullableType: TypeAlias = (
    graphql.GraphQLScalarType
    | graphql.GraphQLObjectType
    | graphql.GraphQLInterfaceType
    | graphql.GraphQLUnionType
    | graphql.GraphQLEnumType
    | graphql.GraphQLInputObjectType
    | graphql.GraphQLList[Any]
)


class TypeConverter:
    def __init__(self) -> None:
        self.input_rules: dict[
            str,
            Callable[[type], GraphQLInputType | None],
        ] = {}
        self.output_rules: dict[
            str,
            Callable[[type], GraphQLOutputType | None],
        ] = {}

    def input_type_rule[
        R: GraphQLInputType | None,
    ](self, name: str) -> Callable[[Callable[[type], R]], Callable[[type], R]]:
        def _wrapper(func: Callable[[type], R]) -> Callable[[type], R]:
            self.input_rules[name] = func
            return func

        return _wrapper

    def output_type_rule[
        R: GraphQLOutputType | None,
    ](self, name: str) -> Callable[[Callable[[type], R]], Callable[[type], R]]:
        def _wrapper(func: Callable[[type], R]) -> Callable[[type], R]:
            self.output_rules[name] = func
            return func

        return _wrapper

    def convert_input_type(self, type_: type) -> GraphQLInputType:
        type_, nonnull = peel_nonnull(type_)

        # priority: last added rule -> first added rule
        for func in reversed(self.input_rules.values()):
            if ret := func(type_):
                if nonnull:
                    return graphql.GraphQLNonNull(ret)
                return ret

        raise TypeError(f"Cannot convert {type_} to GraphQL type")

    def convert_output_type(self, type_: type) -> GraphQLOutputType:
        type_, nonnull = peel_nonnull(type_)

        # priority: last added rule -> first added rule
        for func in reversed(self.output_rules.values()):
            if ret := func(type_):
                # if nonnull:
                #     return graphql.GraphQLNonNull(ret)
                return ret

        raise TypeError(f"Cannot convert {type_} to GraphQL type")


type_converter = TypeConverter()


@type_converter.input_type_rule("str")
@type_converter.output_type_rule("str")
def is_str(type_: type) -> graphql.GraphQLScalarType | None:
    if issubclass(type_, str):
        return graphql.GraphQLString


@type_converter.input_type_rule("int")
@type_converter.output_type_rule("int")
def is_int(type_: type) -> graphql.GraphQLScalarType | None:
    if issubclass(type_, int):
        return graphql.GraphQLInt


@type_converter.input_type_rule("float")
@type_converter.output_type_rule("float")
def is_float(type_: type) -> graphql.GraphQLScalarType | None:
    if issubclass(type_, float):
        return graphql.GraphQLFloat


@type_converter.input_type_rule("bool")
@type_converter.output_type_rule("bool")
def is_bool(type_: type) -> graphql.GraphQLScalarType | None:
    if issubclass(type_, bool):
        return graphql.GraphQLBoolean


@type_converter.output_type_rule("object")
def is_object(type_: type) -> graphql.GraphQLObjectType | None:
    if issubclass(type_, pydantic.BaseModel):
        fields = {}
        for name, field_info in type_.model_fields.items():
            if not field_info.annotation:
                raise TypeError(f"Field {name} of {type_} has no annotation")

            type_, nonnull = peel_nonnull(field_info.annotation)
            graphql_type = type_converter.convert_output_type(type_)
            if nonnull:
                graphql_type.__required__ = True

            fields[name] = graphql.GraphQLField(type_=graphql_type)

        return graphql.GraphQLObjectType(
            name=type_.__name__,
            fields=fields,
        )


def peel_nonnull(type_: type) -> tuple[type, bool]:
    if typing.get_origin(type_) is typing.Union:
        type_list = typing.get_args(type_)
        if len(type_list) > 2:
            raise TypeError(f"GraphQL does not support Union type {type_}{type_list}")

        if type(None) in type_list:
            type_a, type_b = type_list
            if type_a is type(None):
                inner_type = type_b
            else:
                inner_type = type_a
            return inner_type, False

    return type_, True


class Grance:
    def __init__(self) -> None:
        self._query: dict[str, graphql.GraphQLField] = {}
        self._mutation: dict[str, graphql.GraphQLField] = {}
        self._subscription: dict[str, graphql.GraphQLField] = {}

    def query[**P, R](self, name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
        def _query(func: Callable[P, R]) -> Callable[P, R]:
            resolver_signature = inspect.signature(func)
            resolver_types = typing.get_type_hints(func)
            resolver_return_type = type_converter.convert_output_type(
                resolver_types.pop("return"),
            )
            resolver_args = {
                name: graphql.GraphQLArgument(
                    type_=type_converter.convert_input_type(type_),
                    default_value=resolver_signature.parameters[name].default,
                )
                for name, type_ in resolver_types.items()
            }

            def resolver(
                obj: Any,
                info: graphql.GraphQLResolveInfo,
                *args: P.args,
                **kwargs: P.kwargs,
            ) -> R:
                sys_args: dict[str, Any] = {}
                if "obj" in resolver_types:
                    sys_args["obj"] = obj

                if "info" in resolver_types:
                    sys_args["info"] = info

                return func(*args, **kwargs, **sys_args)

            self._query[name] = graphql.GraphQLField(
                type_=resolver_return_type,
                args=resolver_args,
                resolve=resolver,
            )
            return func

        return _query

    def mutation[**P, R](self, name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
        def _mutation(func: Callable[P, R]) -> Callable[P, R]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                return func(*args, **kwargs)

            return wrapper

        return _mutation

    def subscription[
        **P,
        R,
    ](self, name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
        def _subscription(func: Callable[P, R]) -> Callable[P, R]:
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                return func(*args, **kwargs)

            return wrapper

        return _subscription

    @property
    def schema(self) -> graphql.GraphQLSchema:
        return graphql.GraphQLSchema(
            query=graphql.GraphQLObjectType(
                name="Query",
                fields=self._query,
            ),
        )

    def execute(self, query: str) -> graphql.ExecutionResult:
        return graphql.graphql_sync(self.schema, query)
