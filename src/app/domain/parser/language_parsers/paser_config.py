from __future__ import annotations

from typing import TYPE_CHECKING

from app.config.base import get_user_settings

if TYPE_CHECKING:
    from app.domain.parser.language_parsers.language_parser import LanguageParser

spacy_model_mapping = {
    "english": "en_core_web_sm",
}
fugashi_unidic = {
    "written_japanese": get_user_settings().unidic_cwj_path,
    "spoken_japanese": get_user_settings().unidic_csj_path,
}
parser_mapping: dict[str, type[LanguageParser]] = {}
parser_instances: dict[str, LanguageParser] = {}
