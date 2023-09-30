from __future__ import annotations

from graphql import graphql_sync
from graphql import GraphQLField
from graphql import GraphQLObjectType
from graphql import GraphQLSchema
from graphql import GraphQLString


schema = GraphQLSchema(
    query=GraphQLObjectType(
        name="RootQueryType",
        fields={
            "hello": GraphQLField(GraphQLString, resolve=lambda obj, info: "world"),
        },
    ),
)

if __name__ == "__main__":
    query = "{ hello }"

    # expect: ExecutionResult(data={'hello': 'world'}, errors=None)
    print(graphql_sync(schema, query))
