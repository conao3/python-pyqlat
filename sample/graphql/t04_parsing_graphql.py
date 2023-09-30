from __future__ import annotations

import graphql  # type: ignore
from graphql import parse


if __name__ == "__main__":
    document = parse(
        """\
type Query {
  me: User
}

type User {
  id: ID
  name: String
}
""",
    )

    # expect: DocumentNode at 0:65
    print(document)

    # {
    #     "kind": "document",
    #     "definitions": [
    #         {
    #             "kind": "object_type_definition",
    #             "description": None,
    #             "name": {"kind": "name", "value": "Query"},
    #             "directives": [],
    #             "interfaces": [],
    #             "fields": [
    #                 {
    #                     "kind": "field_definition",
    #                     "description": None,
    #                     "name": {"kind": "name", "value": "me"},
    #                     "directives": [],
    #                     "arguments": [],
    #                     "type": {
    #                         "kind": "named_type",
    #                         "name": {"kind": "name", "value": "User"},
    #                     },
    #                 }
    #             ],
    #         },
    #         {
    #             "kind": "object_type_definition",
    #             "description": None,
    #             "name": {"kind": "name", "value": "User"},
    #             "directives": [],
    #             "interfaces": [],
    #             "fields": [
    #                 {
    #                     "kind": "field_definition",
    #                     "description": None,
    #                     "name": {"kind": "name", "value": "id"},
    #                     "directives": [],
    #                     "arguments": [],
    #                     "type": {
    #                         "kind": "named_type",
    #                         "name": {"kind": "name", "value": "ID"},
    #                     },
    #                 },
    #                 {
    #                     "kind": "field_definition",
    #                     "description": None,
    #                     "name": {"kind": "name", "value": "name"},
    #                     "directives": [],
    #                     "arguments": [],
    #                     "type": {
    #                         "kind": "named_type",
    #                         "name": {"kind": "name", "value": "String"},
    #                     },
    #                 },
    #             ],
    #         },
    #     ],
    # }
    print(document.to_dict())

    query = parse(
        """\
{
    me {
        id
        name
    }
}
""",
    )

    # {
    #     "kind": "document",
    #     "definitions": [
    #         {
    #             "kind": "operation_definition",
    #             "name": None,
    #             "directives": [],
    #             "variable_definitions": [],
    #             "selection_set": {
    #                 "kind": "selection_set",
    #                 "selections": [
    #                     {
    #                         "kind": "field",
    #                         "directives": [],
    #                         "alias": None,
    #                         "name": {"kind": "name", "value": "me"},
    #                         "arguments": [],
    #                         "selection_set": {
    #                             "kind": "selection_set",
    #                             "selections": [
    #                                 {
    #                                     "kind": "field",
    #                                     "directives": [],
    #                                     "alias": None,
    #                                     "name": {"kind": "name", "value": "id"},
    #                                     "arguments": [],
    #                                     "selection_set": None,
    #                                 },
    #                                 {
    #                                     "kind": "field",
    #                                     "directives": [],
    #                                     "alias": None,
    #                                     "name": {"kind": "name", "value": "name"},
    #                                     "arguments": [],
    #                                     "selection_set": None,
    #                                 },
    #                             ],
    #                         },
    #                     }
    #                 ],
    #             },
    #             "operation": "query",
    #         }
    #     ],
    # }
    print(query.to_dict())
