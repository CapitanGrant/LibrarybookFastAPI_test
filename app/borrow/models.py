from datetime import datetime, date

from sqlalchemy import Integer, String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base


class Borrow(Base):
    __tablename__ = 'borrows'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey('books.id'), nullable=False)
    reader_name: Mapped[str] = mapped_column(String, nullable=False)
    date_of_issue: Mapped[datetime] = mapped_column(Date, nullable=False, default=date.today())
    return_date: Mapped[datetime] = mapped_column(Date, nullable=True, default=None)

    book: Mapped['Book'] = relationship('Book', back_populates='borrows')

    def __repr__(self):
        return f"<Borrow(id={self.id}, book_id={self.book_id}, borrower={self.reader_name})>"

    def to_dict(self) -> dict:
        return {key: value for key, value in {
            'id': self.id,
            'book_id': self.book_id,
            'reader_name': self.reader_name,
            'date_of_issue': self.date_of_issue,
            'return_date': self.return_date,
        }.items() if value is not None}
