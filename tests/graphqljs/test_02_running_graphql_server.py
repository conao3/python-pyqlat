from __future__ import annotations

import fastapi.testclient
import grance


grance_app = grance.Grance()
fastapi_app = fastapi.FastAPI()


@grance_app.query("hello")
def hello() -> str:
    return "world"


@fastapi_app.post("/graphql")
async def graphql(request: fastapi.Request) -> fastapi.Response:
    request_body_ = await request.body()
    request_body = request_body_.decode()

    return fastapi.responses.JSONResponse(
        grance_app.execute(request_body).formatted,
    )


client = fastapi.testclient.TestClient(fastapi_app)


def test_main():
    query = "{ hello }"
    expected = {
        "data": {
            "hello": "world",
        },
    }
    res = client.post("/graphql", content=query)
    assert res.json() == expected
