from __future__ import annotations

import inspect
import typing
from collections.abc import Callable
from typing import Any
from typing import TypeAlias

import graphql


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


class TypeConverter:
    def __init__(self) -> None:
        self.input_rules: dict[
            str,
            tuple[Callable[[type], bool], GraphQLInputType],
        ] = {}
        self.output_rules: dict[
            str,
            tuple[Callable[[type], bool], GraphQLOutputType],
        ] = {}

    def input_type_rule(
        self,
        name: str,
        type_: GraphQLInputType,
    ) -> Callable[[Callable[[type], bool]], Callable[[type], bool]]:
        def _wrapper(func: Callable[[type], bool]) -> Callable[[type], bool]:
            self.input_rules[name] = (func, type_)
            return func

        return _wrapper

    def output_type_rule(
        self,
        name: str,
        type_: GraphQLOutputType,
    ) -> Callable[[Callable[[type], bool]], Callable[[type], bool]]:
        def _wrapper(func: Callable[[type], bool]) -> Callable[[type], bool]:
            self.output_rules[name] = (func, type_)
            return func

        return _wrapper

    def convert_input_type(self, type_: type) -> GraphQLInputType:
        # priority: last added rule -> first added rule
        for func, ret_type in reversed(self.input_rules.values()):
            if func(type_):
                return ret_type

        raise TypeError(f"Cannot convert {type_} to GraphQL type")

    def convert_output_type(self, type_: type) -> GraphQLOutputType:
        # priority: last added rule -> first added rule
        for func, ret_type in reversed(self.output_rules.values()):
            if func(type_):
                return ret_type

        raise TypeError(f"Cannot convert {type_} to GraphQL type")


type_converter = TypeConverter()


@type_converter.input_type_rule("str", graphql.GraphQLString)
@type_converter.output_type_rule("str", graphql.GraphQLString)
def is_str(type_: type) -> bool:
    return issubclass(type_, str)


@type_converter.input_type_rule("int", graphql.GraphQLInt)
@type_converter.output_type_rule("int", graphql.GraphQLInt)
def is_int(type_: type) -> bool:
    return issubclass(type_, int)


@type_converter.input_type_rule("float", graphql.GraphQLFloat)
@type_converter.output_type_rule("float", graphql.GraphQLFloat)
def is_float(type_: type) -> bool:
    return issubclass(type_, float)


@type_converter.input_type_rule("bool", graphql.GraphQLBoolean)
@type_converter.output_type_rule("bool", graphql.GraphQLBoolean)
def is_bool(type_: type) -> bool:
    return issubclass(type_, bool)


class Qlot:
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
