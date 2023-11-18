from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field


class User(BaseModel):
    name: str = Field(default="John Doe")


user = User()
print(user)
# > name='John Doe'
