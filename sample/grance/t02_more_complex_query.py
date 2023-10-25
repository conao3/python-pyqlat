from __future__ import annotations

import grance


app = grance.Grance()


@app.query("hello")
def hello() -> str:
    return "world"


@app.query("helloArgs")
def hello_args(name: str = "stranger") -> str:
    return f"Hello {name}!"


if __name__ == "__main__":
    # expect: ExecutionResult(data={'hello': 'world'}, errors=None)
    print(app.execute("{ hello }"))

    # expect: ExecutionResult(data={'helloArgs': 'Hello stranger!'}, errors=None)
    print(app.execute("{ helloArgs }"))

    # expect: ExecutionResult(data={'helloArgs': 'Hello GraphQL!'}, errors=None)
    print(app.execute('{ helloArgs(name: "GraphQL") }'))
