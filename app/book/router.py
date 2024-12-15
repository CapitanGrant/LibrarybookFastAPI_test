from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.book.schemas import SBook, SBookFilter, SBookID
from app.book.dao import BookDAO
from app.dao.session_maker import SessionDep, TransactionSessionDep

# uvicorn app.main:app --port 8000

router = APIRouter(prefix="/book", tags=["Book"])


@router.get('/all_books/', summary='Получение списка книг')
async def get_all_books(session: AsyncSession = SessionDep):
    return await BookDAO.find_all(session=session, filters=None)


@router.get('/get_book_by_id/', summary='Получение информации о книге по ID')
async def get_book_by_id(id: int, session: AsyncSession = SessionDep):
    rez = await BookDAO.find_one_or_none_by_id(session=session, data_id=id)
    if rez is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='По заданному ID книги не существует')
    return rez


@router.post("/create_book/", summary='Добавление книги')
async def create_book(book_data: SBook, session: AsyncSession = TransactionSessionDep):
    rez = await BookDAO.find_one_or_none(session=session, filters=SBookFilter(book_name=book_data.book_name))
    if rez:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Книга уже существует!")
    book_data_dict = book_data.model_dump()
    new_book = await BookDAO.add(session=session, values=SBook(**book_data_dict))
    return {'message': f'Книга успешно создана!', 'id': new_book.id}


@router.put('/update_book_by_id/', summary='Обновление книги по ID')
async def update_book(book_id: SBookID, update_data: SBook,
                      session: AsyncSession = TransactionSessionDep):
    rez = await BookDAO.update(session=session, filters=book_id, values=update_data)
    if rez is None:
        return {'message': f'Не удалось обновить запись!'}
    return {'message': f'Успешно обновлена {rez} запись!', 'id': book_id}


@router.delete('/delete_book_by_id/', summary='Удаление книги по ID')
async def delete_book(book_id: SBookID, session: AsyncSession = TransactionSessionDep):
    rez = await BookDAO.delete(session=session, filters=book_id)
    if rez is None:
        return {'message': f'Не удалось удалить книгу!'}
    return {'message': f'Книга удалена!'}
