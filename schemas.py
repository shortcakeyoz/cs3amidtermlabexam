from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    isbn: str = Field(min_length=1)
    publication_year: int | None = None
    stock_quantity: int = Field(default=1, ge=0)
    category_id: int


class BookResponse(BaseModel):
    id: int
    title: str
    isbn: str
    publication_year: int | None
    stock_quantity: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)
