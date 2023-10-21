from __future__ import annotations

import graphql

schema = graphql.GraphQLSchema(
    query=graphql.GraphQLObjectType(
        name="RootQueryType",
        fields={
            "hello": graphql.GraphQLField(
                graphql.GraphQLString,
                resolve=lambda obj, info: "world",
            ),
            "helloArgs": graphql.GraphQLField(
                graphql.GraphQLString,
                args={
                    "name": graphql.GraphQLArgument(
                        graphql.GraphQLString,
                        default_value="stranger",
                    ),
                },
                resolve=lambda obj, info, name: f"Hello {name}!",
            ),
        },
    ),
)

if __name__ == "__main__":
    # expect: ExecutionResult(data={'hello': 'world'}, errors=None)
    print(graphql.graphql_sync(schema, "{ hello }"))

    # expect: ExecutionResult(data={'helloArgs': 'Hello stranger!'}, errors=None)
    print(graphql.graphql_sync(schema, "{ helloArgs }"))

    # expect: ExecutionResult(data={'helloArgs': 'Hello GraphQL!'}, errors=None)
    print(graphql.graphql_sync(schema, '{ helloArgs(name: "GraphQL") }'))
