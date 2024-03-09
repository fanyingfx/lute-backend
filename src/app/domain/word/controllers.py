from typing import Annotated

from litestar import Controller, MediaType, Request, delete, get, post
from litestar.datastructures import UploadFile
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.enums import RequestEncodingType
from litestar.params import Body

from app.config.base import get_user_settings
from app.db.models.word import Word
from app.domain.word.dependencies import provides_word_image_service, provides_word_service
from app.domain.word.dtos import WordCreate, WordCreateDTO, WordDTO, WordPatchDTO, WordUpdate
from app.domain.word.services import WordImageService, WordService

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
    async def create_or_update(self, word_service: WordService, data: DTOData[WordUpdate]) -> Word:
        db_obj = await word_service.create_or_update(data.create_instance().__dict__)
        await word_service.update_word_index(db_obj.language_id, db_obj.first_word)
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
        # await word_service.get(word_string=data.as_builtins())
        raise NotImplementedError

    @post(
        "/upload_word_image",
        media_type=MediaType.TEXT,
        dependencies={"word_image_service": Provide(provides_word_image_service)},
    )
    async def save_word_image(
        self,
        word_image_service: WordImageService,
        word_service: WordService,
        data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
        save_local: bool = False,
        word_id: int | None = None,
        image_name: str | None = None,
    ) -> str:
        if save_local and image_name:
            content = await data.read()
            with (get_user_settings().WORD_IMAGE_PATH / image_name).open("wb") as f:
                f.write(content)
            if word_id is not None:
                db_obj = await word_image_service.create(
                    {"word_id": word_id, "word_image_name": image_name.split(".")[0], "word_image_path": image_name}
                )
                await word_service.update_word_index(db_obj.word.language_id, db_obj.word.first_word)

        filename = data.filename
        return f"{filename}"
