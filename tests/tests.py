from datetime import datetime, timezone, timedelta

import pytest
from jose import jwt
from app.config import get_auth_data

from tests.test_endpoints.create_object import CreateObject
from tests.test_endpoints.get_all_objects import GetAllObject
from tests.test_endpoints.get_object_by_id import GetObjectByID
from tests.test_endpoints.update_object_by_id import UpdateObjectByID

author_payload = {
    "first_name": "Карл",
    "last_name": "Маркс",
    "biography": "Карл Маркс родился 5 мая 1818 года, в городе Трир в Рейнской Пруссии. Его семья была еврейской, но обращается в протестантизм в 1824 году. После окончания гимназии (средней школы) в Трире, Маркс поступил в университет, сначала в Бонне, потом в Берлине, где он изучал право, но больше всего историю и философию. Он завершил свое университетский курс в 1841 году, представив университетскую диссертацию о философии Эпикура.",
    "date_of_birth": "1867-01-01"
}

book_payload = {
    "book_name": "Капитал",
    "author_id": 1,
    "book_description": "stringstringstringstringstringstringstringstringst",
    "date_published": "1877-01-01",
    "book_count": 2
}

borrow_payload = {
    "book_id": 1,
    "reader_name": "Петр",
    "date_of_issue": "2024-12-12"
}

user_payload1 = {
    "email": "user123@example.com",
    "password": "string",
    "phone_number": "+79129459422",
    "first_name": "Василий",
    "last_name": "Пупкин"
}
user_payload2 = {
    "email": "user32@example.com",
    "password": "string",
    "phone_number": "+79126559322",
    "first_name": "Юрий",
    "last_name": "Шуткин"
}

user_login = {
    "email": "user123@example.com",
    "password": "string"
}
user_login_fail = {
    "email": "nouser123@example.com",
    "password": "string"
}

user_add_admin = {
    "id_user": {
        "id": 8
    },
    "is_admin": {
        "is_admin": True
    }
}


@pytest.mark.parametrize('url_create, payload', [("http://127.0.0.1:8000/auth/register/", user_payload1),
                                                 ("http://127.0.0.1:8000/auth/register/", user_payload2)])
@pytest.mark.asyncio
async def test_create_object(url_create, payload):
    '''Тест на создание объекта пользователей, для дальнейшего тестирования вам понадобится вручную наделить правами супер пользователя Василия'''
    create_obj = CreateObject()
    await create_obj.new_object(url=url_create, payload=payload)
    create_obj.check_response_is_200()


@pytest.mark.parametrize('url_login, payload', [("http://127.0.0.1:8000/auth/login/", user_login_fail),
                                                ("http://127.0.0.1:8000/auth/login/", user_login)])
@pytest.mark.asyncio
async def test_login_object(url_login, payload):
    '''Тест на авторизацию пользователя'''
    create_obj = CreateObject()
    if payload == user_login_fail:
        await create_obj.new_object(url=url_login, payload=payload)
        create_obj.check_response_is_401()
    else:
        await create_obj.new_object(url=url_login, payload=payload)
        create_obj.check_response_is_200()


@pytest.fixture
def create_access_token():
    def _create_access_token(user_id: int, is_admin: bool, is_super_admin: bool = False):
        auth_data = get_auth_data()
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
            "is_admin": is_admin,
            "is_super_admin": is_super_admin
        }
        token = jwt.encode(payload, auth_data['secret_key'], algorithm=auth_data['algorithm'])
        return token

    return _create_access_token


@pytest.mark.parametrize('url_update, payload, is_super_admin',
                         [("http://127.0.0.1:8000/auth/add_admin", user_add_admin, False),
                          ("http://127.0.0.1:8000/auth/add_admin", user_add_admin, True)])
@pytest.mark.asyncio
async def test_create_admin(url_update, payload, is_super_admin, create_access_token):
    '''Тест на наделение пользователя правами администратора'''
    update_obj = UpdateObjectByID()
    token = create_access_token(user_id=1, is_admin=True, is_super_admin=is_super_admin)

    await update_obj.update_object_by_id(url=url_update, payload=payload, token=token)
    if is_super_admin:
        update_obj.check_response_is_200()  # Ожидаем успешный ответ
    else:
        update_obj.check_response_is_403()


@pytest.mark.parametrize('url, is_admin', [("http://127.0.0.1:8000/author/all_authors/", True),
                                           ("http://127.0.0.1:8000/book/all_books/", True),
                                           ("http://127.0.0.1:8000/borrow/all_borrows/", True),
                                           ("http://127.0.0.1:8000/borrow/all_borrows/", False), ])
@pytest.mark.asyncio
async def test_get_all_object(url, create_access_token, is_admin):
    '''Тест на получение всех объектов по url.'''
    if is_admin:
        token = create_access_token(user_id=1, is_admin=True)
    else:
        token = create_access_token(user_id=2, is_admin=False)
    all_obj = GetAllObject()
    await all_obj.get_all_objects(url, token)
    if is_admin:
        all_obj.check_response_is_200()
    else:
        all_obj.check_response_is_403()


# @pytest.mark.parametrize('url_create, payload, url_delete', [
#     ("http://127.0.0.1:8000/author/create_author/", author_payload,
#      "http://127.0.0.1:8000/author/delete_author_by_id/"),
#     ("http://127.0.0.1:8000/book/create_book/", book_payload, "http://127.0.0.1:8000/book/delete_book_by_id/"),
#     ("http://127.0.0.1:8000/borrow/create_borrow/", borrow_payload,
#      "http://127.0.0.1:8000/borrow/delete_borrow_by_id/")])
# @pytest.mark.asyncio
# async def test_create_object(url_create, payload, url_delete):
#     '''Тест на создание объекта и его удаление.'''
#     create_obj = CreateObject()
#     await create_obj.new_object(url=url_create, payload=payload)
#     create_obj.check_response_is_200()
#     object_id = create_obj.response_json['id']
#     delete_obj = DeleteObject()
#     await delete_obj.delete_object(url=url_delete, payload={'id': object_id})
#     delete_obj.check_response_is_200()


@pytest.mark.asyncio
@pytest.mark.parametrize("obj_type", ["author", "book", "borrow"])
async def test_get_object_by_id(obj_type, obj_id):
    '''Тест на получение объекта по ID.'''
    url = f"http://127.0.0.1:8000/{obj_type}/get_{obj_type}_by_id/?id="
    get_object = GetObjectByID()
    await get_object.get_object_by_id(url, object_id=obj_id)
    get_object.check_response_is_200()
    await get_object.get_object_by_id(url, object_id=9999)
    get_object.check_response_is_404()


@pytest.mark.asyncio
@pytest.mark.parametrize("obj_type", ["author", "book", "borrow"])
async def test_update_object(obj_type, obj_id):
    '''Тест на обновленипе объекта по ID.'''
    update_object = UpdateObjectByID()
    url = f"http://127.0.0.1:8000/{obj_type}/update_{obj_type}_by_id"
    if obj_type == "author":
        payload_author = {
            "author_id": {
                "id": obj_id
            },
            "update_data": {
                "first_name": "string",
                "last_name": "string",
                "date_of_birth": "2024-12-12"
            }
        }
        await update_object.update_object_by_id(url, payload=payload_author)
    elif obj_type == "book":
        payload_book = {
            "book_id": {
                "id": obj_id
            },
            "update_data": {
                "book_name": "Моби Дик",
                "author_id": 1,
                "book_description": "stringstringstringstringstringstringstringstringst",
                "book_count": 4
            }
        }
        await update_object.update_object_by_id(url, payload=payload_book)
    elif obj_type == "borrow":
        payload_borrow = {
            "id": {
                "id": obj_id
            },
            "update_data": {
                "return_date": "2024-12-15"
            }
        }
        await update_object.update_object_by_id(method="PATCH", url=url,
                                                payload=payload_borrow)
    update_object.check_response_is_200()
