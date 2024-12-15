from app.dao.base import BaseDAO
from app.book.models import Book


class BookDAO(BaseDAO):
    model = Book
