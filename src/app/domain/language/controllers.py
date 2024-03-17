from litestar import Controller, get, post
from litestar.di import Provide
from litestar.dto import DTOData
from litestar.pagination import OffsetPagination

import app.domain.parser.language_parsers.paser_config
from app.db.models.language import Language
from app.domain.language.dependencies import provides_language_service
from app.domain.language.dtos import LanguageCreateDTO, LanguageData, LanguageDTO
from app.domain.language.services import LanguageService

# from app.domain.parser import parser_tool

__all__ = ("LanguageController",)


class LanguageController(Controller):
    path = "/language"
    tags = ["language"]
    dependencies = {
        "language_service": Provide(provides_language_service),
    }
    return_dto = LanguageDTO

    @get("/languages")
    async def list_languages(self, language_service: LanguageService) -> OffsetPagination[Language]:
        languages = await language_service.list()
        return language_service.to_dto(languages)

    @get("/parsers")
    async def list_parsers(self) -> list[str]:
        return app.domain.parser.language_parsers.paser_config.list_all_parsers()

    @post("/create", dto=LanguageCreateDTO)
    async def create_language(self, language_service: LanguageService, data: DTOData[LanguageData]) -> Language:
        db_obj = await language_service.create(data.as_builtins())
        return language_service.to_dto(db_obj)

    # @post("/update/{word_string:str}")
    # async def update_word(self, word_service: WordService, data: WordUpdate) -> Word:
    #     # await word_service.get(word_string=data.as_builtins())
    #     raise NotImplementedError
