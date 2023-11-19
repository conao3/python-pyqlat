from __future__ import annotations

import random
from typing import Any

import grance


app = grance.Grance()


@app.query("roll_three_dice")
def handler_roll_three_dice(num_dice: int, num_sides: int = 6) -> list[int]:
    return [random.randint(1, num_sides) for _ in range(num_dice)]


def test_main(mocker: Any):
    mocker.patch.object(random, "randint", return_value=2)

    query = """
    {
        rollThreeDice(numDice: 3, numSides: 6)
    }
    """
    expected = {
        "data": {
            "rollThreeDice": [2, 2, 2],
        },
    }
    assert app.execute(query).formatted == expected
