from pydantic import BaseModel, Field


class SBook(BaseModel):
    book_name: str = Field(..., min_length=2, max_length=50, description="Название книги, от 2 до 50 символов")
    author_id: int = Field(..., description="ID автора")
    book_description: str = Field(..., min_length=50, max_length=255,
                                  description="Описание книги, от 2 до 255 символов")
    book_count: int = Field(
        default=0,
        ge=0,
        description="Количество доступных экземпляров книги (неотрицательное число)"
    )


class SBookFilter(BaseModel):
    book_name: str = Field(..., min_length=2, max_length=50, description="Название книги, от 2 до 50 символов")


class SBookID(BaseModel):
    id: int = Field(..., description="ID книги")
