from litestar import Controller, Request, delete, get, post
from litestar.di import Provide
from litestar.dto import DTOData

from app.db.models.word import Word
from app.domain.word.dependencies import provides_word_service
from app.domain.word.dtos import WordCreate, WordCreateDTO, WordDTO, WordPatchDTO, WordUpdate
from app.domain.word.services import WordService

__all__ = ("WordController",)


class WordController(Controller):
    path = "/word"
    tags = ["word"]
    dependencies = {
        "word_service": Provide(provides_word_service),
    }
    return_dto = WordDTO

    @get("/word_id/{word_id:int}")
    async def get_word_by_id(self, word_service: WordService, word_id: int) -> Word:
        word = await word_service.get(item_id=word_id)
        return word_service.to_dto(word)

    @get("/word_string/{word_string:str}")
    async def search_word_string(self, word_service: WordService, word_string: str) -> Word:
        db_word = await word_service.get_one(word_string=word_string)
        return word_service.to_dto(db_word)

    @post(path="/create_or_update", dto=WordPatchDTO)
    async def create_or_update(self, word_service: WordService, data: DTOData[WordUpdate], request: Request) -> Word:
        db_obj = await word_service.create_or_update(data.create_instance().__dict__)
        await word_service.update_word_index(db_obj.language_id, db_obj.first_word)
        # request.app.emit("word_updated", language_name=db_obj.language.language_name, word_string=db_obj.first_word)
        return word_service.to_dto(db_obj)

    @post("/create", dto=WordCreateDTO)
    async def create_word(self, word_service: WordService, data: DTOData[WordCreate]) -> Word:
        db_obj = await word_service.create(data.as_builtins())
        await word_service.update_word_index(db_obj.language_id, db_obj.first_word)
        return word_service.to_dto(db_obj)

    @delete("/delete/{word_id:int}")
    async def delete_word(self, word_service: WordService, word_id: int, request: Request) -> None:
        db_obj = await word_service.delete(item_id=word_id, auto_commit=True)
        await word_service.update_word_index(db_obj.language_id, db_obj.first_word)
        # return word_service.to_dto(db_obj)

    @post("/update/{word_string:str}")
    async def update_word(self, word_service: WordService, data: WordUpdate) -> Word:
        await word_service.get(word_string=data.as_builtins())
