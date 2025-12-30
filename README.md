# Grance

A type-driven GraphQL schema builder for Python. Define your GraphQL API using native Python type hints and Pydantic models.

## Overview

Grance eliminates the boilerplate typically associated with GraphQL schema definition. Instead of manually defining types, fields, and resolvers separately, you write standard Python functions with type annotations and Grance generates the corresponding GraphQL schema automatically.

## Features

- Automatic schema generation from Python type hints
- Pydantic model support for complex object types
- Built-in field name conversion (snake_case to camelCase)
- Seamless integration with graphql-core
- Support for nullable types, lists, and nested objects

## Installation

```bash
pip install grance
```

Or with Poetry:

```bash
poetry add grance
```

## Quick Start

```python
import grance

app = grance.Grance()

@app.query("hello")
def hello() -> str:
    return "world"

result = app.execute("{ hello }")
print(result.data)  # {'hello': 'world'}
```

## Working with Arguments

```python
@app.query("greet")
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Query: { greet(name: "Alice") }
```

## Using Pydantic Models

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str | None

@app.query("user")
def get_user(id: int) -> User:
    return User(id=id, name="Alice", email="alice@example.com")

# Query: { user(id: 1) { id name email } }
```

## Requirements

- Python 3.12+
- graphql-core
- Pydantic 2.x

## License

Apache-2.0

## Contributing

### Pre-commit Hooks

This project uses pre-commit for code quality checks. To set up:

```bash
poetry run pre-commit install -t pre-commit
```
