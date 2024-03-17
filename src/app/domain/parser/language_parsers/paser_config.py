from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from app.config.base import get_user_settings

if TYPE_CHECKING:
    from spacy import Language

    from app.domain.parser import LanguageParser

spacy_model_mapping = {
    "english": "en_core_web_sm",
}
fugashi_unidic = {
    "written_japanese": get_user_settings().unidic_cwj_path_str,
    "spoken_japanese": get_user_settings().unidic_csj_path_str,
}
parser_mapping: dict[str, type[LanguageParser]] = {}
parser_instances: dict[str, LanguageParser] = {}
nlp_mapping: dict[str, Language] = {}


def register_parser(parser_name: str) -> Callable[[type[LanguageParser]], type[LanguageParser]]:
    def wrapper(cls: type[LanguageParser]) -> type[LanguageParser]:
        if parser_name in parser_mapping:
            raise ValueError(f"Parser {parser_name} is already registered")
        if parser_name == "spacy":
            for key in spacy_model_mapping:
                parser_mapping[key] = cls
        elif parser_name == "fugashi":
            for key in fugashi_unidic:
                parser_mapping[key] = cls
        else:
            parser_mapping[parser_name] = cls
        return cls

    return wrapper


def list_all_parsers() -> list[str]:
    return list(parser_mapping.keys())


def parser_exists(parser_name: str) -> bool:
    return parser_name in parser_mapping
