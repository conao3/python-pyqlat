from __future__ import annotations

import graphql
from graphql import build_schema
from graphql import graphql_sync

from .t02_building_type_schema import EpisodeEnum
from .t02_building_type_schema import get_character_type
from .t02_building_type_schema import get_hero

schema = build_schema(
    """\
enum Episode { NEWHOPE, EMPIRE, JEDI }

interface Character {
    id: String!
    name: String
    friends: [Character]
    appearsIn: [Episode]
}

type Human implements Character {
    id: String!
    name: String
    friends: [Character]
    appearsIn: [Episode]
    homePlanet: String
}

type Droid implements Character {
    id: String!
    name: String
    friends: [Character]
    appearsIn: [Episode]
    primaryFunction: String
}

type Query {
    hero(episode: Episode): Character
    human(id: String!): Human
    droid(id: String!): Droid
}
""",
)

schema.query_type.fields["hero"].resolve = get_hero
schema.get_type("Character").resolve_type = get_character_type

for name, value in schema.get_type("Episode").values.items():
    value.value = EpisodeEnum[name].value


if __name__ == "__main__":
    # enum Episode {
    #   NEWHOPE
    #   EMPIRE
    #   JEDI
    # }
    #
    # interface Character {
    #   id: String!
    #   name: String
    #   friends: [Character]
    #   appearsIn: [Episode]
    # }
    #
    # type Human implements Character {
    #   id: String!
    #   name: String
    #   friends: [Character]
    #   appearsIn: [Episode]
    #   homePlanet: String
    # }
    #
    # type Droid implements Character {
    #   id: String!
    #   name: String
    #   friends: [Character]
    #   appearsIn: [Episode]
    #   primaryFunction: String
    # }
    #
    # type Query {
    #   hero(episode: Episode): Character
    #   human(id: String!): Human
    #   droid(id: String!): Droid
    # }
    print(graphql.print_schema(schema))

    result = graphql_sync(
        schema,
        """\
{
  hero(episode: EMPIRE) {
    name
    appearsIn
  }
}
""",
    )

    # expect: ExecutionResult(data={'hero': {'name': 'Luke Skywalker', 'appearsIn': ['NEWHOPE', 'EMPIRE', 'JEDI']}}, errors=None)
    print(result)
