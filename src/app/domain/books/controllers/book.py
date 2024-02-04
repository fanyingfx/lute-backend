from typing import Annotated

from litestar import Controller, get

__all__ = ("BookController",)


from litestar import delete, patch, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.pagination import OffsetPagination
from litestar.params import Parameter

from app.domain.books.dependencies import provides_book_service
from app.domain.books.dtos import BookCreate, BookCreateDTO, BookDTO, BookPatchDTO, BookUpdate
from app.domain.books.models import Book
from app.domain.books.services import BookService


class BookController(Controller):
    path = "/book"
    tags = ["book"]
    dependencies = {"book_service": Provide(provides_book_service)}
    return_dto = BookDTO

    @get("/book_id/{book_id:int}")
    async def get_book_by_id(self, book_service: BookService, book_id: int) -> Book:
        book = await book_service.get(item_id=book_id)
        return book_service.to_dto(book)

    @get("/list")
    async def list_books(
        self,
        book_service: BookService,
    ) -> OffsetPagination[Book]:
        result = await book_service.list()
        return book_service.to_dto(result)

    @post("/add", dto=BookCreateDTO)
    async def add_book(self, book_service: BookService, data: DTOData[BookCreate]) -> Book:
        db_obj = await book_service.create(data.as_builtins())
        return book_service.to_dto(db_obj)

    @patch("/update", dto=BookPatchDTO)
    async def update_book(
        self, book_service: BookService, data: DTOData[BookUpdate], book_id: Annotated[int, Parameter(title="BookID")]
    ) -> Book:
        db_obj = await book_service.update(item_id=book_id, data=data.create_instance().__dict__)
        return book_service.to_dto(db_obj)

    @delete("/delete/{book_id:int}")
    async def delete_book(self, book_id: int, book_service: BookService) -> None:
        _ = await book_service.delete(item_id=book_id, auto_commit=True)
