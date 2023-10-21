from __future__ import annotations

import qlot


qlot_app = qlot.Qlot()


def hello() -> str:
    return "world"


if __name__ == "__main__":
    query = "{ hello }"

    # expect: ExecutionResult(data={'hello': 'world'}, errors=None)
    print(hello())
