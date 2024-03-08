from typing import TYPE_CHECKING, Annotated, Any

from litestar import Controller, get

__all__ = ("BookController", "BookTextController")

from litestar import MediaType, delete, patch, post
from litestar.datastructures import UploadFile
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.enums import RequestEncodingType
from litestar.pagination import OffsetPagination
from litestar.params import Body, Parameter

from app.db.models.book import Book, BookText
from app.db.models.word import Word
from app.domain.book.dependencies import provides_book_service, provides_booktext_service
from app.domain.book.dtos import (
    BookCreate,
    BookCreateDTO,
    BookDTO,
    BookPatchDTO,
    BookTextCreate,
    BookTextCreateDTO,
    BookTextDTO,
    BookUpdate,
    ParsedBookText,
    ParsedBookTextDTO,
)
from app.domain.book.services import BookService, BookTextService
from app.domain.parser import parser_tool
from app.domain.parser.markdown_text_parser import (
    parse_markdown,
)
from app.domain.word.dependencies import provides_word_service
from app.domain.word.dtos import WordDTO
from app.domain.word.services import WordService

if TYPE_CHECKING:
    from app.domain.parser import LanguageParser


class BookController(Controller):
    path = "/book"
    tags = ["book"]
    dependencies = {
        "book_service": Provide(provides_book_service),
    }
    return_dto = BookDTO

    # @get("/book_id/{book_id:int}")
    # async def get_book_by_id(self, book_service: BookService, book_id: int) -> Book:
    #     book = await book_service.get(item_id=book_id)
    #
    #     return book_service.to_dto(book)

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
        db_obj = book_service.to_dto(db_obj)
        return book_service.to_dto(db_obj)

    @post("/add_book_and_content", dto=BookCreateDTO)
    async def add_book_and_content(self, book_service: BookService, data: DTOData[BookCreate]) -> dict[str, Any]:
        contents = data.create_instance().texts
        if contents is None or len(contents) == 0:
            from litestar.exceptions import HTTPException

            raise HTTPException("Content cannot be empty")
        db_obj = await book_service.create_with_contents(data.as_builtins(), contents)
        return {"book_id": db_obj.id, "message": f"{data.as_builtins()['book_name']} created successfully"}

    @patch("/update", dto=BookPatchDTO)
    async def update_book(
        self, book_service: BookService, data: DTOData[BookUpdate], book_id: Annotated[int, Parameter(title="BookID")]
    ) -> Book:
        db_obj = await book_service.update(item_id=book_id, data=data.create_instance().__dict__)
        return book_service.to_dto(db_obj)

    @delete("/delete/{book_id:int}")
    async def delete_book(self, book_id: int, book_service: BookService) -> None:
        _ = await book_service.delete(item_id=book_id, auto_commit=True)


class BookTextController(Controller):
    path = "/book"
    tags = ["book", "booktext"]
    dependencies = {
        "booktext_service": Provide(provides_booktext_service),
        "word_service": Provide(provides_word_service),
    }
    return_dto = BookTextDTO

    @post("/add_booktext", dto=BookTextCreateDTO)
    async def add_booktext(self, booktext_service: BookTextService, data: DTOData[BookTextCreate]) -> BookText:
        db_obj = await booktext_service.create(data.as_builtins())
        return booktext_service.to_dto(db_obj)

    @post("/upload_book_text", media_type=MediaType.TEXT)
    async def handle_file_upload(
        self,
        booktext_service: BookTextService,
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
        book_id: int,
        book_text_id: int,
    ) -> str:
        content = await data.read()
        await booktext_service.update(BookText(ref_book_id=book_id, book_text=content.decode()), item_id=book_text_id)
        return f"{data.filename} successfully uploaded"

    @get("/list_words", return_dto=WordDTO)
    async def list_words(self, word_service: WordService) -> OffsetPagination[Word]:
        # collection_filter = CollectionFilter("is_multiple_words", [True])
        db_obj = await word_service.list()
        return word_service.to_dto(db_obj)

    @get("/booktext/{booktext_id:int}", return_dto=ParsedBookTextDTO)
    async def get_booktext(
        self, booktext_service: BookTextService, word_service: WordService, booktext_id: int
    ) -> ParsedBookText:
        db_obj: BookText = await booktext_service.get(item_id=booktext_id)
        parser: LanguageParser = db_obj.book.language.get_parser()
        word_index: dict[str, list[Word]] = await word_service.load_word_index(db_obj.book.language_id)
        segmentlist = parse_markdown(db_obj.book_text)
        res = await parser_tool.get_parsed_text_segments(segmentlist, parser, word_index)

        return ParsedBookText(data=res)
