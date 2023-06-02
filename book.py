from pydantic import BaseModel

class Book(BaseModel):
    identifier: int | None = None
    title: str | None = None
    author: str | None = None
    year: int | None = None
    quantity: int | None = None