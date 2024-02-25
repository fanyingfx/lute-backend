from collections.abc import Callable

from app.domain.parser.language_parser import LanguageParser, parser_mapping

__all__ = ("register_parser", "list_all_parsers", "parser_exists")

spacy_model_mapping = {
    "english": "en_core_web_sm",
}


def register_parser(parser_name: str) -> Callable[[type[LanguageParser]], type[LanguageParser]]:
    def wrapper(cls: type[LanguageParser]) -> type[LanguageParser]:
        if parser_name in parser_mapping:
            raise ValueError(f"Parser {parser_name} is already registered")
        if parser_name == "spacy":
            for key in spacy_model_mapping:
                parser_mapping[key] = cls
        else:
            parser_mapping[parser_name] = cls
        return cls

    return wrapper


def list_all_parsers() -> list[str]:
    return [name.capitalize() for name in parser_mapping]


def parser_exists(parser_name: str) -> bool:
    return parser_name in parser_mapping
