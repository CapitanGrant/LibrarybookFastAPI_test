import pytest
from tests.test_endpoints.create_object import CreateObject
from tests.test_endpoints.delete_object import DeleteObject


@pytest.fixture
def create_object():
    return CreateObject()


@pytest.fixture
def del_object():
    return DeleteObject()


@pytest.fixture
async def obj_id(create_object: CreateObject, del_object: DeleteObject, obj_type: str):
    obj_payloads = {
        "author": {
            "url": "http://127.0.0.1:8000/author/create_author/",
            "payload": {
                "first_name": "Карлоs",
                "last_name": "Марксоs",
                "date_of_birth": "1867-01-01"
            },
            "delete_url": "http://127.0.0.1:8000/author/delete_author_by_id/"
        },
        "book": {
            "url": "http://127.0.0.1:8000/book/create_book/",
            "payload": {
                "book_name": "Капитал",
                "author_id": 1,
                "book_description": "stringstringstringstringstringstringstringstringst",
                "book_count": 2
            },
            "delete_url": "http://127.0.0.1:8000/book/delete_book_by_id/"
        },
        "borrow": {
            "url": "http://127.0.0.1:8000/borrow/create_borrow/",
            "payload": {
                "book_id": 1,
                "reader_name": "strinфыаg",
                "date_of_issue": "2024-12-12"},
            "delete_url": "http://127.0.0.1:8000/borrow/delete_borrow_by_id/"
        }
    }
    obj_payload = obj_payloads[obj_type]

    await create_object.new_object(url=obj_payload["url"], payload=obj_payload["payload"])
    try:
        yield create_object.response_json['id']
    finally:
        if create_object.response_json and "id" in create_object.response_json:
            object_id = create_object.response_json['id']
            await del_object.delete_object(url=obj_payload["delete_url"],
                                           payload={"id": object_id})
