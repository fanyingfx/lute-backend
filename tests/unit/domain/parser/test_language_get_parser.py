import pytest

from app.domain.parser.language_parser import LanguageParser


def test_japanese_parser() -> None:
    parser = LanguageParser.get_parser("japanese")
    assert parser is not None


def test_english_parser() -> None:
    parser = LanguageParser.get_parser("english")
    assert parser is not None


def test_unregister_parser() -> None:
    with pytest.raises(ValueError):
        LanguageParser.get_parser("spacy")
    with pytest.raises(ValueError):
        LanguageParser.get_parser("chinese")
