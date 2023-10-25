from __future__ import annotations

import graphql
import pydantic
import qlot


qlot_app = qlot.Qlot()


class BlogImage(pydantic.BaseModel):
    url: str | None
    # width: int
    # height: int


@qlot_app.query("image")
def image() -> BlogImage:
    return BlogImage(url="example.com/img/logo.png")  # , width=400, height=200)


if __name__ == "__main__":
    # expect: ExecutionResult(data={'image': {'url': 'example.com/img/logo.png', 'width': 400, 'height': 200}}, errors=None)
    print(qlot_app.execute("{ image { url, width, height } }"))

    print(graphql.print_schema(qlot_app.schema))
