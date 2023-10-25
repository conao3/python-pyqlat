from __future__ import annotations

import grance


app = grance.Grance()


@app.query("hello")
def hello() -> str:
    return "world"


if __name__ == "__main__":
    # expect: ExecutionResult(data={'hello': 'world'}, errors=None)
    print(app.execute("{ hello }"))
