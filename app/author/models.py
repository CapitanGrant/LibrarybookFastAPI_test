from sqlalchemy import Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.book.models import Book
from app.dao.database import Base


class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(Date, nullable=False)

    books: Mapped[list['Book']] = relationship("Book", back_populates="author")

    def __repr__(self):
        return f"<Author(id={self.id}, name={self.first_name} {self.last_name})>"

    def to_dict(self) -> dict:
        return {key: value for key, value in {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
        }.items() if value is not None}
