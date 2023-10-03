from __future__ import annotations

import graphql

from .t02_building_type_schema import schema

if __name__ == "__main__":
    errors = graphql.validate(
        schema,
        graphql.parse(
            """\
{
  human(id: NEWHOPE) {
    name
    homePlace
    friends
  }
}
""",
        ),
    )

    # [
    #     GraphQLError(
    #         "String cannot represent a non string value: NEWHOPE",
    #         locations=[SourceLocation(line=2, column=13)],
    #     ),
    #     GraphQLError(
    #         "Cannot query field 'homePlace' on type 'Human'. Did you mean 'homePlanet'?",
    #         locations=[SourceLocation(line=4, column=5)],
    #     ),
    #     GraphQLError(
    #         "Field 'friends' of type '[Character]' must have a selection of subfields. Did you mean 'friends { ... }'?",
    #         locations=[SourceLocation(line=5, column=5)],
    #     ),
    # ]
    print(errors)
