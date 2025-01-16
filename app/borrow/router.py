from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.borrow.dao import BorrowDAO
from app.borrow.schemas import SBorrowCreate, SBorrowID, SBorrowUpdateReturnDate, SBorrowReaderName
from app.dao.session_maker import SessionDep, TransactionSessionDep
from loguru import logger

from app.users.auth import get_current_admin_user, get_current_user
from app.users.models import User

# uvicorn app.main:app --port 8001

router = APIRouter(prefix="/borrow", tags=["Borrows"])


@router.get("/all_borrows/", summary='Получить список всех задач')
async def get_all_borrows(user_data: User = Depends(get_current_admin_user), session: AsyncSession = SessionDep):
    return await BorrowDAO.find_all(session=session, filters=None)


@router.get("/all_reader/", summary='Получить список всех читателей')
async def get_all_borrows(user_data: User = Depends(get_current_admin_user), session: AsyncSession = SessionDep):
    return await BorrowDAO.find_all_reader_name(session=session, filters=None)


@router.get('/get_borrow_by_id/', summary='Получение информации о выдаче книги по ID')
async def get_book_by_id(id: int, user_data: User = Depends(get_current_admin_user),
                         session: AsyncSession = SessionDep):
    rez = await BorrowDAO.find_one_or_none_by_id(session=session, data_id=id)
    if rez is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='По заданному ID записи о выдаче не существует')
    return rez


@router.post('/create_borrow/', summary='Создать запись о выдаче книги')
async def create_borrow(borrow_data: SBorrowCreate, user_data: User = Depends(get_current_user),
                        session: AsyncSession = TransactionSessionDep):
    try:
        borrow_data_dict = borrow_data.model_dump()
        new_borrow = await BorrowDAO.add(session=session, values=SBorrowCreate(**borrow_data_dict))
        if new_borrow:
            return {'message': f'Запись успешно создана!', 'id': new_borrow.id}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Не удалось создать запись')
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при работе с базой данных: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ошибка базы данных.")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ошибка: {str(e)}")


@router.patch('/update_borrow_by_id/', summary='Обновление статуса выданной книги')
async def update_borrow(id: SBorrowID, update_data: SBorrowUpdateReturnDate,
                        user_data: User = Depends(get_current_user),
                        session: AsyncSession = TransactionSessionDep):
    rez = await BorrowDAO.update(session=session, filters=id, values=update_data)
    if rez is None:
        return {'message': f'Не удалось обновить запись!'}
    return {'message': f'Успешно обновлена {rez} запись!'}


@router.delete('/delete_borrow_by_id/', summary='Удаление записи о выданной книге')
async def update_borrow(borrow_id: SBorrowID, user_data: User = Depends(get_current_admin_user),
                        session: AsyncSession = TransactionSessionDep):
    rez = await BorrowDAO.delete(session=session, filters=borrow_id)
    if rez is None:
        return {'message': f'Не удалось удалить запись!'}
    return {'message': f'Запись успешно удалена!'}
