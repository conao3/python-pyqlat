from __future__ import annotations

import grance


app = grance.Grance()


@app.query("hello")
def hello() -> str:
    return "world"


def test_main():
    query = "{ hello }"
    expected = {
        "data": {
            "hello": "world",
        },
    }
    assert app.execute(query).formatted == expected
