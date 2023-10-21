from __future__ import annotations

import functools

import graphene.types.definitions
import graphene.types.schema
import graphql
from graphene import ObjectType
from graphene import String


class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `first_name`
    # By default, the argument name will automatically be camel-based into firstName in the generated schema
    hello = String(first_name=String(default_value="stranger"))
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (first_name) for the Field and returns data for the query Response
    def resolve_hello(root, info, first_name):
        return f"Hello {first_name}!"

    def resolve_goodbye(root, info):
        return "See ya!"


if __name__ == "__main__":
    type_map = graphene.types.schema.TypeMap(query=Query)

    # expect: Query, []
    print(type_map.query, type_map.types)

    schema = graphql.GraphQLSchema(
        query=type_map.query,
    )

    # ExecutionResult(data={'hello': 'Hello stranger!'}, errors=None)
    print(graphql.graphql_sync(schema, "{ hello }"))

    ###

    type_map = graphene.types.schema.TypeMap()
    schema = graphql.GraphQLSchema(
        query=type_map.create_objecttype(Query),
    )
    print(graphql.graphql_sync(schema, "{ hello }"))

    ###

    type_map = graphene.types.schema.TypeMap()
    schema = graphql.GraphQLSchema(
        query=graphene.types.definitions.GrapheneObjectType(
            graphene_type=Query,
            name="Query",
            fields=functools.partial(type_map.create_fields_for_type, Query),
        ),
    )
    print(graphql.graphql_sync(schema, "{ hello }"))

    ###

    type_map = graphene.types.schema.TypeMap()

    fields = {}
    for field_name, field in Query._meta.fields.items():
        field_type = type_map.add_type(field.type)
        args = {}
        for arg_name, arg in field.args.items():
            arg_type = type_map.add_type(arg.type)
            args[arg_name] = graphql.GraphQLArgument(
                type_=arg_type,
                default_value=arg.default_value,
            )
        fields[field_name] = graphql.GraphQLField(
            type_=field_type,
            args=args,
            resolve=field.wrap_resolve(
                type_map.get_function_for_type(
                    Query,
                    f"resolve_{field_name}",
                    field_name,
                    field.default_value,
                ),
            ),
        )

    schema = graphql.GraphQLSchema(
        query=graphene.types.definitions.GrapheneObjectType(
            graphene_type=Query,
            name="Query",
            fields=fields,
        ),
    )
    print(graphql.graphql_sync(schema, "{ hello }"))
