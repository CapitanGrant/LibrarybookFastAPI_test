import pytest

from tests.test_endpoints.create_object import CreateObject
from tests.test_endpoints.delete_object import DeleteObject
from tests.test_endpoints.get_all_objects import GetAllObject
from tests.test_endpoints.get_object_by_id import GetObjectByID
from tests.test_endpoints.update_object_by_id import UpdateObjectByID

author_payload = {
    "first_name": "Карлоs",
    "last_name": "Марксоs",
    "date_of_birth": "1867-01-01"
}

book_payload = {
    "book_name": "Капитал",
    "author_id": 1,
    "book_description": "stringstringstringstringstringstringstringstringst",
    "book_count": 2
}

borrow_payload = {
    "book_id": 1,
    "reader_name": "strinфыаg",
    "date_of_issue": "2024-12-12"
}


@pytest.mark.parametrize('url', ["http://127.0.0.1:8000/author/all_authors/",
                                 "http://127.0.0.1:8000/book/all_books/",
                                 "http://127.0.0.1:8000/borrow/all_borrows/"])
@pytest.mark.asyncio
async def test_get_all_object(url):
    '''Тест на получение всех объектов по url.'''
    all_obj = GetAllObject()
    await all_obj.get_all_objects(url)
    all_obj.check_response_is_200()


@pytest.mark.parametrize('url_create, payload, url_delete', [
    ("http://127.0.0.1:8000/author/create_author/", author_payload,
     "http://127.0.0.1:8000/author/delete_author_by_id/"),
    ("http://127.0.0.1:8000/book/create_book/", book_payload, "http://127.0.0.1:8000/book/delete_book_by_id/"),
    ("http://127.0.0.1:8000/borrow/create_borrow/", borrow_payload,
     "http://127.0.0.1:8000/borrow/delete_borrow_by_id/")])
@pytest.mark.asyncio
async def test_create_object(url_create, payload, url_delete):
    '''Тест на создание объекта и его удаление.'''
    create_obj = CreateObject()
    await create_obj.new_object(url=url_create, payload=payload)
    create_obj.check_response_is_200()
    object_id = create_obj.response_json['id']
    delete_obj = DeleteObject()
    await delete_obj.delete_object(url=url_delete, payload={'id': object_id})
    delete_obj.check_response_is_200()


@pytest.mark.asyncio
@pytest.mark.parametrize("obj_type", ["author", "book", "borrow"])
async def test_get_object_by_id(obj_type, obj_id):
    '''Тест на получение объекта по ID.'''
    url = "http://127.0.0.1:8000/{}/get_{}_by_id/?id="
    get_object = GetObjectByID()
    await get_object.get_object_by_id(url=url.format(obj_type, obj_type), object_id=obj_id)
    get_object.check_response_is_200()
    await get_object.get_object_by_id(url=url.format(obj_type, obj_type), object_id=9999)
    get_object.check_response_is_404()


@pytest.mark.asyncio
@pytest.mark.parametrize("obj_type", ["author", "book", "borrow"])
async def test_update_object(obj_type, obj_id):
    '''Тест на обновленипе объекта по ID.'''
    update_object = UpdateObjectByID()
    url = "http://127.0.0.1:8000/{}/update_{}_by_id"
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
        await update_object.update_object_by_id(url=url.format(obj_type, obj_type), payload=payload_author)
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
        await update_object.update_object_by_id(url=url.format(obj_type, obj_type), payload=payload_book)
    elif obj_type == "borrow":
        payload_borrow = {
            "id": {
                "id": obj_id
            },
            "update_data": {
                "return_date": "2024-12-15"
            }
        }
        await update_object.update_object_by_id(method="PATCH", url=url.format(obj_type, obj_type),
                                                payload=payload_borrow)
    update_object.check_response_is_200()
