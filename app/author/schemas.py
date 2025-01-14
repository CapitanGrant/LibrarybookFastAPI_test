from datetime import datetime, date

from pydantic import BaseModel, Field, field_validator


class SAuthorBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50, description="Имя автора, от 2 до 50 символов")
    last_name: str = Field(..., min_length=2, max_length=50, description="Фамилия автора, от 2 до 50 символов")
    date_of_birth: date = Field(..., description="Дата рождения, в формате YYYY-MM-DD")
    biography: str = Field(..., min_length=2, max_length=550, description="Биография писателя, от 2 до 550 символов")

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, values: date) -> date:
        if values >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return values


class SAuthorFilter(BaseModel):
    last_name: str = Field(..., min_length=2, max_length=50, description="Имя автора, от 2 до 50 символов")


class SAuthorID(BaseModel):
    id: int = Field(..., description="ID автора")
