from __future__ import annotations

import graphql

BlogImage = graphql.GraphQLObjectType(
    name="BlogImage",
    fields={
        "url": graphql.GraphQLField(graphql.GraphQLString),
        "width": graphql.GraphQLField(graphql.GraphQLNonNull(graphql.GraphQLInt)),
        "height": graphql.GraphQLField(graphql.GraphQLNonNull(graphql.GraphQLInt)),
    },
)

schema = graphql.GraphQLSchema(
    query=graphql.GraphQLObjectType(
        name="Query",
        fields={
            "image": graphql.GraphQLField(
                BlogImage,
                resolve=lambda obj, info: {
                    "url": "example.com/img/logo.png",
                    "width": 400,
                    "height": 200,
                },
            ),
        },
    ),
)

if __name__ == "__main__":
    # expect: ExecutionResult(data={'image': {'url': 'example.com/img/logo.png', 'width': 400, 'height': 200}}, errors=None)
    print(graphql.graphql_sync(schema, "{ image { url, width, height } }"))

    print(graphql.print_schema(schema))
