from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.borrow.models import Borrow
from app.dao.database import Base


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    book_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('author.id'), nullable=False)
    book_description: Mapped[str] = mapped_column(String, nullable=False)
    book_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    author: Mapped['Author'] = relationship('Author', back_populates='books')
    borrows: Mapped[list['Borrow']] = relationship('Borrow', back_populates='book')

    def __repr__(self):
        return f'<Book({self.id}, title={self.book_name})>'

    def to_dict(self) -> dict:
        return {key: value for key, value in {
            'id': self.id,
            'book_name': self.book_name,
            'author_id': self.author_id,
            'book_discription': self.book_description,
            'book_count': self.book_count,
        }.items() if value is not None}
