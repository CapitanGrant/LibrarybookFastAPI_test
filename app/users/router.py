from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm import SessionTransaction
from sqlalchemy.orm.sync import update

from app.dao.session_maker import TransactionSessionDep, SessionDep
from app.users.auth import get_password_hash, authenticate_user, get_current_user, get_current_super_admin_user
from app.users.dao import UsersDAO
from app.users.models import User
from app.users.schemas import SUserRegister, SUserMail, SUserAuth, SUserIsAdmin, SUserID
from app.dao.database import AsyncSession
from app.users.utils import create_access_token

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post("/register/")
async def register_user(user_data: SUserRegister, session: AsyncSession = TransactionSessionDep) -> dict:
    user_filter = SUserMail(email=user_data.email)
    user = await UsersDAO.find_one_or_none(session=session, filters=user_filter)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(session=session, values=SUserRegister(**user_dict))
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def login_user(response: Response, user_data: SUserAuth, session: AsyncSession = SessionDep) -> dict:
    user_filter = SUserMail(email=user_data.email)
    check = await authenticate_user(session=session, email=user_filter, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неверная почта или пароль')
    access_token = create_access_token({'sub': str(check.id)})
    response.set_cookie(key='users_access_token', value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)):
    return user_data


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@router.put("/add_admin/")
async def add_admin(id_user: SUserID, is_admin: SUserIsAdmin, session: AsyncSession = TransactionSessionDep,
                    user_data: User = Depends(get_current_super_admin_user)):
    rez = await UsersDAO.update(session=session, filters=id_user, values=is_admin)
    if rez is None:
        return {'message': f'Не удалось обновить запись!'}
    return {'message': f'Успешно обновлена {rez} запись!', 'id': id_user.id}
