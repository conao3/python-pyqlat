# graphql

## Conversion

- SDL: `str` - GraphQL Schema Definition Language
- Introspection JSON: `TypedDict` - GraphQL Schema Introspection Result
- GraphQL Schema: `graphql.GraphQLSchema` - GraphQL Schema Object

```python
import graphql

# GraphQL Schema -> SDL
graphql.print_schema(schema)

# GraphQL Schema -> Introspection JSON
graphql.introspection_from_schema(schema)

# SDL -> GraphQL Schema
graphql.build_schema(sdl)

# Introspection JSON -> GraphQL Schema
graphql.build_client_schema(introspection)

# Introspection JSON -> (GraphQL Schema) -> SDL
graphql.print_schema(graphql.build_client_schema(introspection))
```
