import pytest

from app.domain.parser import LanguageParser


def test_japanese_parser() -> None:
    parser = LanguageParser.get_parser("japanese")
    assert isinstance(parser, LanguageParser)


def test_english_parser() -> None:
    parser = LanguageParser.get_parser("english")
    assert isinstance(parser, LanguageParser)


def test_parser_not_exist() -> None:
    with pytest.raises(ValueError):
        LanguageParser.get_parser("spacy")
    with pytest.raises(ValueError):
        LanguageParser.get_parser("chinese")
