from __future__ import annotations

import asyncio
from enum import Enum
from typing import Any

import graphql
from graphql import GraphQLArgument
from graphql import GraphQLEnumType
from graphql import GraphQLField
from graphql import GraphQLInterfaceType
from graphql import GraphQLList
from graphql import GraphQLNonNull
from graphql import GraphQLObjectType
from graphql import GraphQLSchema
from graphql import GraphQLString


luke = {
    "id": "1000",
    "name": "Luke Skywalker",
    "homePlanet": "Tatooine",
    "friends": ["1002", "1003", "2000", "2001"],
    "appearsIn": [4, 5, 6],
}

vader = {
    "id": "1001",
    "name": "Darth Vader",
    "homePlanet": "Tatooine",
    "friends": ["1004"],
    "appearsIn": [4, 5, 6],
}

han = {
    "id": "1002",
    "name": "Han Solo",
    "homePlanet": None,
    "friends": ["1000", "1003", "2001"],
    "appearsIn": [4, 5, 6],
}

leia = {
    "id": "1003",
    "name": "Leia Organa",
    "homePlanet": "Alderaan",
    "friends": ["1000", "1002", "2000", "2001"],
    "appearsIn": [4, 5, 6],
}

tarkin = {
    "id": "1004",
    "name": "Wilhuff Tarkin",
    "homePlanet": None,
    "friends": ["1001"],
    "appearsIn": [4],
}

human_data = {
    "1000": luke,
    "1001": vader,
    "1002": han,
    "1003": leia,
    "1004": tarkin,
}

threepio = {
    "id": "2000",
    "name": "C-3PO",
    "primaryFunction": "Protocol",
    "friends": ["1000", "1002", "1003", "2001"],
    "appearsIn": [4, 5, 6],
}

artoo = {
    "id": "2001",
    "name": "R2-D2",
    "primaryFunction": "Astromech",
    "friends": ["1000", "1002", "1003"],
    "appearsIn": [4, 5, 6],
}

droid_data = {
    "2000": threepio,
    "2001": artoo,
}


def get_character_type(character: dict[str, Any], _info: Any, _type: Any) -> str:
    return "Droid" if character["id"] in droid_data else "Human"


def get_character(id: str) -> dict[str, Any] | None:
    """Helper function to get a character by ID."""
    return human_data.get(id) or droid_data.get(id)


def get_friends(character: dict[str, Any], _info: Any) -> list[dict[str, Any] | None]:
    """Allows us to query for a character's friends."""
    return [get_character(elm) for elm in character.get("friends", [])]


def get_hero(root: Any, _info: Any, episode: int) -> dict[str, Any]:
    """Allows us to fetch the undisputed hero of the trilogy, R2-D2."""
    if episode == 5:
        return luke  # Luke is the hero of Episode V
    return artoo  # Artoo is the hero otherwise


def get_human(root: Any, _info: Any, id: str) -> dict[str, Any] | None:
    """Allows us to query for the human with the given id."""
    return human_data.get(id)


def get_droid(root: Any, _info: Any, id: str) -> dict[str, Any] | None:
    """Allows us to query for the droid with the given id."""
    return droid_data.get(id)


def get_secret_backstory(_character: dict[str, Any], _info: Any) -> None:
    """Raise an error when attempting to get the secret backstory."""
    raise RuntimeError("secretBackstory is secret.")


class EpisodeEnum(Enum):
    NEWHOPE = 4
    EMPIRE = 5
    JEDI = 6


episode_enum = GraphQLEnumType(
    "Episode",
    EpisodeEnum,
    description="One of the films in the Star Wars Trilogy",
)


character_interface = GraphQLInterfaceType(
    "Character",
    lambda: {
        "id": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The id of the character.",
        ),
        "name": GraphQLField(
            GraphQLString,
            description="The name of the character.",
        ),
        "friends": GraphQLField(
            GraphQLList(character_interface),
            description="The friends of the character,"
            " or an empty list if they have none.",
        ),
        "appearsIn": GraphQLField(
            GraphQLList(episode_enum),
            description="Which movies they appear in.",
        ),
        "secretBackstory": GraphQLField(
            GraphQLString,
            description="All secrets about their past.",
        ),
    },
    resolve_type=get_character_type,
    description="A character in the Star Wars Trilogy",
)


human_type = GraphQLObjectType(
    "Human",
    lambda: {
        "id": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The id of the human.",
        ),
        "name": GraphQLField(
            GraphQLString,
            description="The name of the human.",
        ),
        "friends": GraphQLField(
            GraphQLList(character_interface),
            description="The friends of the human,"
            " or an empty list if they have none.",
            resolve=get_friends,
        ),
        "appearsIn": GraphQLField(
            GraphQLList(episode_enum),
            description="Which movies they appear in.",
        ),
        "homePlanet": GraphQLField(
            GraphQLString,
            description="The home planet of the human, or null if unknown.",
        ),
        "secretBackstory": GraphQLField(
            GraphQLString,
            resolve=get_secret_backstory,
            description="Where are they from" " and how they came to be who they are.",
        ),
    },
    interfaces=[character_interface],
    description="A humanoid creature in the Star Wars universe.",
)


droid_type = GraphQLObjectType(
    "Droid",
    lambda: {
        "id": GraphQLField(
            GraphQLNonNull(GraphQLString),
            description="The id of the droid.",
        ),
        "name": GraphQLField(
            GraphQLString,
            description="The name of the droid.",
        ),
        "friends": GraphQLField(
            GraphQLList(character_interface),
            description="The friends of the droid,"
            " or an empty list if they have none.",
            resolve=get_friends,
        ),
        "appearsIn": GraphQLField(
            GraphQLList(episode_enum),
            description="Which movies they appear in.",
        ),
        "secretBackstory": GraphQLField(
            GraphQLString,
            resolve=get_secret_backstory,
            description="Construction date and the name of the designer.",
        ),
        "primaryFunction": GraphQLField(
            GraphQLString,
            description="The primary function of the droid.",
        ),
    },
    interfaces=[character_interface],
    description="A mechanical creature in the Star Wars universe.",
)


query_type = GraphQLObjectType(
    "Query",
    lambda: {
        "hero": GraphQLField(
            character_interface,
            args={
                "episode": GraphQLArgument(
                    episode_enum,
                    description=(
                        "If omitted, returns the hero of the whole saga."
                        " If provided, returns the hero of that particular episode."
                    ),
                ),
            },
            resolve=get_hero,
        ),
        "human": GraphQLField(
            human_type,
            args={
                "id": GraphQLArgument(
                    GraphQLNonNull(GraphQLString),
                    description="id of the human",
                ),
            },
            resolve=get_human,
        ),
        "droid": GraphQLField(
            droid_type,
            args={
                "id": GraphQLArgument(
                    GraphQLNonNull(GraphQLString),
                    description="id of the droid",
                ),
            },
            resolve=get_droid,
        ),
    },
)


schema = GraphQLSchema(query_type)

# type Query {
#   hero(
#     """
#     If omitted, returns the hero of the whole saga. If provided, returns the hero of that particular episode.
#     """
#     episode: Episode
#   ): Character
#   human(
#     """id of the human"""
#     id: String!
#   ): Human
#   droid(
#     """id of the droid"""
#     id: String!
#   ): Droid
# }
#
# """A character in the Star Wars Trilogy"""
# interface Character {
#   """The id of the character."""
#   id: String!
#
#   """The name of the character."""
#   name: String
#
#   """The friends of the character, or an empty list if they have none."""
#   friends: [Character]
#
#   """Which movies they appear in."""
#   appearsIn: [Episode]
#
#   """All secrets about their past."""
#   secretBackstory: String
# }
#
# """One of the films in the Star Wars Trilogy"""
# enum Episode {
#   NEWHOPE
#   EMPIRE
#   JEDI
# }
#
# """A humanoid creature in the Star Wars universe."""
# type Human implements Character {
#   """The id of the human."""
#   id: String!
#
#   """The name of the human."""
#   name: String
#
#   """The friends of the human, or an empty list if they have none."""
#   friends: [Character]
#
#   """Which movies they appear in."""
#   appearsIn: [Episode]
#
#   """The home planet of the human, or null if unknown."""
#   homePlanet: String
#
#   """Where are they from and how they came to be who they are."""
#   secretBackstory: String
# }
#
# """A mechanical creature in the Star Wars universe."""
# type Droid implements Character {
#   """The id of the droid."""
#   id: String!
#
#   """The name of the droid."""
#   name: String
#
#   """The friends of the droid, or an empty list if they have none."""
#   friends: [Character]
#
#   """Which movies they appear in."""
#   appearsIn: [Episode]
#
#   """Construction date and the name of the designer."""
#   secretBackstory: String
#
#   """The primary function of the droid."""
#   primaryFunction: String
# }
print(graphql.print_schema(schema))


async def query_artoo():
    result = await graphql.graphql(
        schema,
        """\
{
  droid(id: "2001") {
    name
    primaryFunction
  }
}
""",
    )
    print(result)


# expect: ExecutionResult(data={'droid': {'name': 'R2-D2', 'primaryFunction': 'Astromech'}}, errors=None)
asyncio.run(query_artoo())


result = graphql.graphql_sync(
    schema,
    """\
query FetchHuman($id: String!) {
  human(id: $id) {
    name
    homePlanet
  }
}
""",
    variable_values={"id": "1000"},
)

# expect: ExecutionResult(data={'human': {'name': 'Luke Skywalker', 'homePlanet': 'Tatooine'}}, errors=None)
print(result)


result = graphql.graphql_sync(
    schema,
    """\
{
  human(id: "1000") {
    name
    homePlace
  }
}
""",
)

# expect: ExecutionResult(
#     data=None,
#     errors=[
#         GraphQLError("Cannot query field 'homePlace' on type 'Human'. Did you mean 'homePlanet'?", locations=[SourceLocation(line=5, column=9)])
#     ]
# )
print(result)
