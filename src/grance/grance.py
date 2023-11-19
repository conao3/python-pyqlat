from __future__ import annotations

import inspect
import types as pytypes
import typing
from collections.abc import Callable
from typing import Any

import graphql
import pydantic.alias_generators


type GraphQLInputType[T: graphql.GraphQLType] = (
    graphql.GraphQLScalarType
    | graphql.GraphQLEnumType
    | graphql.GraphQLInputObjectType
    | graphql.GraphQLWrappingType[T]
)


type GraphQLInputInnerType = (
    graphql.GraphQLScalarType | graphql.GraphQLEnumType | graphql.GraphQLInputObjectType
)


type GraphQLOutputType[T: graphql.GraphQLType] = (
    graphql.GraphQLScalarType
    | graphql.GraphQLObjectType
    | graphql.GraphQLInterfaceType
    | graphql.GraphQLUnionType
    | graphql.GraphQLEnumType
    | graphql.GraphQLWrappingType[T]
)


type GraphQLOutputInnerType = (
    graphql.GraphQLScalarType
    | graphql.GraphQLObjectType
    | graphql.GraphQLInterfaceType
    | graphql.GraphQLUnionType
    | graphql.GraphQLEnumType
)


type GraphQLNullableType[T: graphql.GraphQLType] = (
    graphql.GraphQLScalarType
    | graphql.GraphQLObjectType
    | graphql.GraphQLInterfaceType
    | graphql.GraphQLUnionType
    | graphql.GraphQLEnumType
    | graphql.GraphQLInputObjectType
    | graphql.GraphQLList[T]
)


class FieldType[T: GraphQLNullableType[graphql.GraphQLType]](pydantic.BaseModel):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    type_: T
    required: bool = True

    def input_type(self) -> GraphQLInputType[T]:
        if self.required:
            return graphql.GraphQLNonNull(self.type_)
        else:
            type_ = typing.cast(GraphQLInputType[T], self.type_)
            return type_

    def output_type(self) -> GraphQLOutputType[T]:
        if self.required:
            return graphql.GraphQLNonNull(self.type_)
        else:
            type_ = typing.cast(GraphQLOutputType[T], self.type_)
            return type_


type InputTypeFunction[T: GraphQLNullableType[graphql.GraphQLType]] = Callable[
    [type],
    FieldType[T] | None,
]
type OutputTypeFunction[T: GraphQLNullableType[graphql.GraphQLType]] = Callable[
    [type],
    FieldType[T] | None,
]
type IdentityFunction[T] = Callable[[T], T]


class TypeConverter:
    def __init__(self) -> None:
        self.input_rules: dict[str, InputTypeFunction[Any]] = {}
        self.output_rules: dict[str, OutputTypeFunction[Any]] = {}

    def input_type_rule[
        T: GraphQLNullableType[graphql.GraphQLType],
    ](self, name: str) -> IdentityFunction[InputTypeFunction[T]]:
        def _wrapper(func: InputTypeFunction[T]) -> InputTypeFunction[T]:
            self.input_rules[name] = func
            return func

        return _wrapper

    def output_type_rule[
        T: GraphQLNullableType[graphql.GraphQLType],
    ](self, name: str) -> IdentityFunction[OutputTypeFunction[T]]:
        def _wrapper(func: OutputTypeFunction[T]) -> OutputTypeFunction[T]:
            self.output_rules[name] = func
            return func

        return _wrapper

    def convert_input_type(self, type_: type) -> FieldType[GraphQLInputInnerType]:
        type_, nullable = peel_nullable(type_)

        # priority: last added rule -> first added rule
        for func in reversed(self.input_rules.values()):
            if ret := func(type_):
                ret.required = not nullable

                return ret

        raise TypeError(f"Cannot convert {type_} to GraphQL type")

    def convert_output_type(self, type_: type) -> FieldType[GraphQLOutputInnerType]:
        type_, nullable = peel_nullable(type_)

        # priority: last added rule -> first added rule
        for func in reversed(self.output_rules.values()):
            if ret := func(type_):
                ret.required = not nullable

                return ret

        raise TypeError(f"Cannot convert {type_} to GraphQL type")


type_converter = TypeConverter()


@type_converter.input_type_rule("str")
@type_converter.output_type_rule("str")
def is_str(type_: type) -> FieldType[graphql.GraphQLScalarType] | None:
    if issubclass(type_, str):
        return FieldType(type_=graphql.GraphQLString)


@type_converter.input_type_rule("int")
@type_converter.output_type_rule("int")
def is_int(type_: type) -> FieldType[graphql.GraphQLScalarType] | None:
    if issubclass(type_, int):
        return FieldType(type_=graphql.GraphQLInt)


@type_converter.input_type_rule("float")
@type_converter.output_type_rule("float")
def is_float(type_: type) -> FieldType[graphql.GraphQLScalarType] | None:
    if issubclass(type_, float):
        return FieldType(type_=graphql.GraphQLFloat)


@type_converter.input_type_rule("bool")
@type_converter.output_type_rule("bool")
def is_bool(type_: type) -> FieldType[graphql.GraphQLScalarType] | None:
    if issubclass(type_, bool):
        return FieldType(type_=graphql.GraphQLBoolean)


@type_converter.output_type_rule("object")
def is_object(type_: type) -> FieldType[graphql.GraphQLObjectType] | None:
    if issubclass(type_, pydantic.BaseModel):
        fields = {}
        for name, field_info in type_.model_fields.items():
            if not field_info.annotation:
                raise TypeError(f"Field {name} of {type_} has no annotation")

            graphql_type = type_converter.convert_output_type(field_info.annotation)

            fields[name] = graphql.GraphQLField(type_=graphql_type.output_type())

        return FieldType(
            type_=graphql.GraphQLObjectType(
                name=type_.__name__,
                fields=fields,
            ),
        )


def peel_nullable(type_: type) -> tuple[type, bool]:
    if typing.get_origin(type_) in (typing.Union, pytypes.UnionType):
        type_list = typing.get_args(type_)
        if len(type_list) > 2:
            raise TypeError(f"GraphQL does not support Union type {type_}{type_list}")

        if type(None) in type_list:
            type_a, type_b = type_list
            if type_a is type(None):
                inner_type = type_b
            else:
                inner_type = type_a
            return inner_type, True

    return type_, False


class Grance:
    def __init__(self) -> None:
        self._query: dict[str, graphql.GraphQLField] = {}
        self._mutation: dict[str, graphql.GraphQLField] = {}
        self._subscription: dict[str, graphql.GraphQLField] = {}

    def query[**P, R](self, name_: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
        name = pydantic.alias_generators.to_camel(name_)

        def _query(func: Callable[P, R]) -> Callable[P, R]:
            resolver_signature = inspect.signature(func)
            resolver_types = typing.get_type_hints(func)
            resolver_return_type = type_converter.convert_output_type(
                resolver_types.pop("return"),
            )
            resolver_args = {
                name: graphql.GraphQLArgument(
                    type_=type_converter.convert_input_type(type_).input_type(),
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
                type_=resolver_return_type.output_type(),
                args=resolver_args,
                resolve=resolver,
            )
            return func

        return _query

    def mutation[
        **P,
        R,
    ](self, name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
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
