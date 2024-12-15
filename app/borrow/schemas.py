from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator, model_validator


class SBorrowCreate(BaseModel):
    book_id: int = Field(..., description="ID книги")
    reader_name: str = Field(..., min_length=2, max_length=50, description="Имя читателя, от 2 до 50 символов")
    date_of_issue: date = Field(..., description="Дата выдачи")

    @field_validator("date_of_issue")
    @classmethod
    def validate_date_in_past(cls, value: date) -> date:
        if value > datetime.now().date():
            raise ValueError(
                f'Дата должна быть в прошлом, текущая дата: {datetime.now().date()}, введенная дата: {value}')
        return value


class SBorrowID(BaseModel):
    id: int = Field(..., description="ID выдачи")


class SBorrowUpdateReturnDate(BaseModel):
    return_date: date = Field(default=date.today(), description="Дата возврата")

    @field_validator("return_date")
    @classmethod
    def validate_date_in_past(cls, value: date) -> date:
        if value > datetime.now().date():
            raise ValueError(
                f'Дата должна быть текущей либо прошедшей, текущая дата: {datetime.now().date()}, введенная дата: {value}')
        return value


class SBorrow(BaseModel):
    book_id: int = Field(..., description="ID книги")
    reader_name: str = Field(..., min_length=2, max_length=50, description="Имя читателя, от 2 до 50 символов")
    date_of_issue: date = Field(..., description="Дата выдачи")
    # return_date: date = Field(default=None, description="Дата возврата")

    # @field_validator("date_of_issue", "return_date")
    # @classmethod
    # def validate_date_in_past(cls, value: date) -> date:
    #     if value > datetime.now().date():
    #         raise ValueError(
    #             f'Дата должна быть в прошлом, текущая дата: {datetime.now().date()}, введенная дата: {value}')
    #     return value
    #
    # @model_validator(mode="after")
    # def validate_return_date(self) -> 'SBorrow':
    #     if self.return_date and self.date_of_issue > self.return_date:
    #         raise ValueError(
    #             f'"Дата выдачи должна быть раньше даты возврата. Выдана: {self.date_of_issue}, возвращена: {self.return_date}')
    #     return self