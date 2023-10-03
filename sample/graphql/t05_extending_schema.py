from __future__ import annotations

from graphql import extend_schema
from graphql import graphql_sync
from graphql import parse

from .t02_building_type_schema import schema


schema = extend_schema(
    schema,
    parse(
        """\
extend type Human {
    lastName: String
}
""",
    ),
)


def get_last_name(human, info):
    return human["name"].rsplit(None, 1)[-1]


schema.get_type("Human").fields["lastName"].resolve = get_last_name

if __name__ == "__main__":
    result = graphql_sync(
        schema,
        """\
{
human(id: "1000") {
    lastName
    homePlanet
}
}
""",
    )

    # expect: ExecutionResult(data={'human': {'lastName': 'Skywalker', 'homePlanet': 'Tatooine'}}, errors=None)
    print(result)
