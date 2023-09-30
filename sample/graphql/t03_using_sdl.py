from __future__ import annotations

import graphql
from graphql import build_schema
from graphql import graphql_sync

from .t02_building_type_schema import artoo
from .t02_building_type_schema import droid_data
from .t02_building_type_schema import EpisodeEnum
from .t02_building_type_schema import get_character_type
from .t02_building_type_schema import get_hero
from .t02_building_type_schema import human_data
from .t02_building_type_schema import luke

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


class Root:
    """The root resolvers"""

    def hero(self, info, episode):
        return luke if episode == 5 else artoo

    def human(self, info, id):
        return human_data.get(id)

    def droid(self, info, id):
        return droid_data.get(id)


from graphql import graphql_sync


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

    result = graphql_sync(
        schema,
        """\
{
  droid(id: "2001") {
    name
    primaryFunction
  }
}
""",
        Root(),
    )
    # expect: ExecutionResult(data={'droid': {'name': 'R2-D2', 'primaryFunction': 'Astromech'}}, errors=None)
    print(result)
