from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain.parser.language_parsers.language_parser import LanguageParser

spacy_model_mapping = {
    "english": "en_core_web_sm",
}
fugashi_unidic = {
    "written_japanese": "C:/Users/fanzh/PycharmProjects/lute-backend/data/cwj",
    "spoken_japanese": "C:/Users/fanzh/PycharmProjects/lute-backend/data/csj",
}
parser_mapping: dict[str, type[LanguageParser]] = {}
parser_instances: dict[str, LanguageParser] = {}
