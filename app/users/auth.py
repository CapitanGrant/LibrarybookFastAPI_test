from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.session_maker import SessionDep
from app.users.models import User
from app.users.schemas import SUserMail
from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone
from app.config import get_auth_data
from app.exceptions import TokenExpiredException, NoJwtException, NoUserIdException, ForbiddenException
from app.users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: SUserMail, password: str, session: AsyncSession = SessionDep):
    user = await UsersDAO.find_one_or_none(session=session, filters=email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    print(token)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token


async def get_current_user(token: str = Depends(get_token), session: AsyncSession = SessionDep):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен истек')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')
    user = await UsersDAO.find_one_or_none_by_id(session=session, data_id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')

    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.is_admin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')
