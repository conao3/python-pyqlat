from __future__ import annotations

import pyqlat


qlat = pyqlat.PyQlat()


def hello() -> str:
    return "world"


if __name__ == "__main__":
    query = "{ hello }"

    # expect: ExecutionResult(data={'hello': 'world'}, errors=None)
    print(hello())
