from datetime import date

from pydantic import BaseModel
from sqlalchemy import update, func
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.author.models import Author
from app.book.models import Book
from app.dao.base import BaseDAO
from app.borrow.models import Borrow
from loguru import logger
from sqlalchemy.future import select


class BorrowDAO(BaseDAO):
    model = Borrow

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        # Добавить одну запись
        values_dict = values.model_dump(exclude_unset=True)
        logger.info(f"Добавление записи {cls.model.__name__} с параметрами: {values_dict}")
        new_instance = cls.model(**values_dict)
        session.add(new_instance)
        try:
            current_book_count = await session.execute(select(Book.book_count).where(Book.id == new_instance.book_id))
            current_book_count = current_book_count.scalar()
            if current_book_count - 1 < 0:
                raise ValueError(
                    f"Количество выданных книг с ID {new_instance.book_id} не может быть меньше 0, попробуйте получить другую книгу")
            await session.flush()
            await session.execute(
                update(Book)
                .where(Book.id == new_instance.book_id)
                .values(book_count=Book.book_count - 1)
            )
            await session.commit()
            logger.info(f"Запись {cls.model.__name__} и обновление book_count успешно выполнены.")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении записи: {e}")
            raise e
        return new_instance

    @classmethod
    async def update(cls, session: AsyncSession, filters: BaseModel, values: BaseModel):
        # Обновить записи по фильтрам
        filter_dict = filters.model_dump(exclude_unset=True)
        values_dict = values.model_dump(exclude_unset=True)
        if 'return_date' in values_dict:
            current_borrow = await session.execute(
                select(Borrow)
                .where(*[getattr(Borrow, k) == v for k, v in filter_dict.items()])
            )
            current_borrow = current_borrow.scalar_one_or_none()
            if current_borrow and current_borrow.return_date is not None:
                logger.info(f"Ошибка: Книга уже возвращена (return_date: {current_borrow.return_date}).")
                return "Книга уже возвращена."
            if current_borrow is not None:
                logger.info(
                    f"Обновление записей {cls.model.__name__} по фильтру: {filter_dict} с параметрами: {values_dict}")
                query = (
                    sqlalchemy_update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_dict.items()])
                    .values(**values_dict)
                    .execution_options(synchronize_session="fetch")
                )

                try:
                    result = await session.execute(query)
                    rez = await session.execute(select(Borrow)
                                                .where(Borrow.id == current_borrow.id)
                                                .options(joinedload(Borrow.book)))
                    borrow = rez.scalar_one_or_none()
                    if borrow and borrow.book:
                        borrow.book.book_count += 1
                    await session.flush()

                    logger.info(f"Обновлено {result.rowcount} записей.")
                    return result.rowcount
                except SQLAlchemyError as e:
                    await session.rollback()
                    logger.error(f"Ошибка при обновлении записей: {e}")
                    raise e
            else:
                logger.info("Ошибка: Запись не найдена.")
                return "Запись не найдена."

        else:
            logger.info("Ошибка: Не предоставлено значение для return_date.")
            return "Не предоставлено значение для return_date."

    @classmethod
    async def find_all_reader_name(cls, session: AsyncSession, filters: BaseModel | None):
        if filters:
            filter_dict = filters.model_dump(exclude_unset=True)
        else:
            filter_dict = {}
        logger.info(f"Поиск всех записей {cls.model.__name__} по фильтрам: {filter_dict}")
        try:
            query = (
                select(cls.model.reader_name, Book.book_name, Author.first_name, Author.last_name,
                       func.count(cls.model.id))
                .join(Book, cls.model.book_id == Book.id)
                .join(Author, Book.author_id == Author.id)
                .group_by(cls.model.reader_name, Book.book_name, Author.first_name, Author.last_name)
            )
            if filter_dict:
                query = query.filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.all()
            response = {}
            for reader_name, book_name, author_first_name, author_last_name, borrow_count in records:
                if reader_name not in response:
                    response[reader_name] = []
                response[reader_name].append({
                    "Название книги": book_name,
                    "Автор Книги": f"{author_first_name} {author_last_name}",
                    "Количество взятых книг": borrow_count,
                })

            logger.info(f"Найдено {len(response)} уникальных читателей.")
            return response
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске всех записей по фильтрам {filter_dict}: {e}")
            raise