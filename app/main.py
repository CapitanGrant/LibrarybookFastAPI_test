from fastapi import FastAPI
from app.author.router import router as author_router
from app.book.router import router as book_router
from app.borrow.router import router as borrow_router


app = FastAPI()


@app.get('/')
def home_page():
    return {"message": "Добро пожаловать! Данное приложение осуществляет "
                       "простое управление CRUD операциями по работе с библиотекой книг!"}


app.include_router(author_router)
app.include_router(book_router)
app.include_router(borrow_router)
