from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.author.dao import AuthorDAO
from app.author.schemas import SAuthorBase, SAuthorFilter, SAuthorID
from app.dao.session_maker import SessionDep, TransactionSessionDep
from app.users.auth import get_current_admin_user, get_current_user
from app.users.models import User

router = APIRouter(prefix="/author", tags=["Author"])


@router.get("/all_authors/", summary='Получить список всех авторов книг')
async def get_all_authors(user_data: User = Depends(get_current_user), session: AsyncSession = SessionDep):
    return await AuthorDAO.find_all(session=session, filters=None)


@router.get("/get_author_by_id/", summary='Получить автора по id')
async def get_author(id: int, user_data: User = Depends(get_current_admin_user), session: AsyncSession = SessionDep):
    author = await AuthorDAO.find_one_or_none_by_id(session=session, data_id=id)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Автора с указанным вами id не существует')
    return author


@router.post("/create_author/", summary='Создать автора книги')
async def create_author(author_data: SAuthorBase, user_data: User = Depends(get_current_admin_user),
                        session: AsyncSession = TransactionSessionDep) -> dict:
    author = await AuthorDAO.find_one_or_none(session=session, filters=SAuthorFilter(last_name=author_data.last_name))
    if author:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Автор уже существует!")
    author_data_dict = author_data.model_dump()
    new_author = await AuthorDAO.add(session=session, values=SAuthorBase(**author_data_dict))
    return {'message': f'Автор успешно создан!', 'id': new_author.id}


@router.put("/update_author_by_id/", summary='Обновить данные об авторе')
async def update_author(author_id: SAuthorID, update_data: SAuthorBase,
                        user_data: User = Depends(get_current_admin_user),
                        session: AsyncSession = TransactionSessionDep):
    rez = await AuthorDAO.update(session=session, filters=author_id, values=update_data)
    if rez is None:
        return {'message': f'Не удалось обновить запись!'}
    return {'message': f'Успешно обновлена {rez} запись!', 'id': author_id}


@router.delete("/delete_author_by_id/", summary='Удалить автора по id')
async def delete_author_by_id(id: SAuthorID, user_data: User = Depends(get_current_admin_user),
                              session: AsyncSession = TransactionSessionDep):
    rez = await AuthorDAO.delete(session=session, filters=id)
    if rez is None:
        return {'message': f'Не удалось удалить автора!'}
    return {'message': f'Автор удален!'}
