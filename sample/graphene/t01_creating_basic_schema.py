from __future__ import annotations

from graphene import ObjectType
from graphene import Schema
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


schema = Schema(query=Query)

if __name__ == "__main__":
    # expect: <graphene.types.schema.Schema object at 0x7f30ab7ea810>
    print(object.__str__(schema))

    query = "{ hello }"
    result = schema.execute(query)
    # expect: ExecutionResult(data={'hello': 'Hello stranger!'}, errors=None)
    print(result)

    query_with_argument = '{ hello(firstName: "GraphQL") }'
    result = schema.execute(query_with_argument)
    # expect: ExecutionResult(data={'hello': 'Hello GraphQL!'}, errors=None)
    print(result)
