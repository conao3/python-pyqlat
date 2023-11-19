from __future__ import annotations

import random
from typing import Any

import grance


app = grance.Grance()


@app.query("quote_of_the_day")
def handler_quote_of_the_day() -> str:
    return "Take it easy" if random.random() < 0.5 else "Salvation lies within"


@app.query("random")
def handler_random() -> float:
    return random.random()


@app.query("roll_three_dice")
def handler_roll_three_dice() -> list[int]:
    return [random.randint(1, 6) for _ in range(3)]


def test_main(mocker: Any):
    mocker.patch.object(random, "random", return_value=0.3)
    mocker.patch.object(random, "randint", return_value=2)

    query = """
    {
        quoteOfTheDay
        random
        rollThreeDice
    }
    """
    expected = {
        "data": {
            "quoteOfTheDay": "Take it easy",
            "random": 0.3,
            "rollThreeDice": [2, 2, 2],
        },
    }
    assert app.execute(query).formatted == expected
