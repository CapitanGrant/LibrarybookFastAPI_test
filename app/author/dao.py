from app.dao.base import BaseDAO
from app.author.models import Author


class AuthorDAO(BaseDAO):
    model = Author
