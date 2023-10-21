from __future__ import annotations

import qlot


qlot_app = qlot.Qlot()


@qlot_app.query("hello")
def hello() -> str:
    return "world"


@qlot_app.query("helloArgs")
def hello_args(name: str = "stranger") -> str:
    return f"Hello {name}!"


if __name__ == "__main__":
    # expect: ExecutionResult(data={'hello': 'world'}, errors=None)
    print(qlot_app.execute("{ hello }"))

    # expect: ExecutionResult(data={'helloArgs': 'Hello stranger!'}, errors=None)
    print(qlot_app.execute("{ helloArgs }"))

    # expect: ExecutionResult(data={'helloArgs': 'Hello GraphQL!'}, errors=None)
    print(qlot_app.execute('{ helloArgs(name: "GraphQL") }'))
