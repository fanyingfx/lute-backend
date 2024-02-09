from litestar import Controller, get, post
from litestar.di import Provide
from litestar.dto import DTOData

from app.domain.words.dependencies import provides_word_service
from app.domain.words.dtos import WordCreate, WordCreateDTO, WordDTO
from app.domain.words.models import Word
from app.domain.words.services import WordService

__all__ = ("WordController",)


class WordController(Controller):
    path = "/word"
    tags = ["word"]
    dependencies = {
        "word_service": Provide(provides_word_service),
    }
    return_dto = WordDTO

    @get("/word_id/{word_id:int}")
    async def get_book_by_id(self, word_service: WordService, word_id: int) -> Word:
        book = await word_service.get_one_or_none(item_id=word_id)
        return word_service.to_dto(book)

    @post("/create", dto=WordCreateDTO)
    async def create_word(self, word_service: WordService, data: DTOData[WordCreate]) -> Word:
        db_obj = await word_service.create(data.as_builtins())
        return word_service.to_dto(db_obj)
