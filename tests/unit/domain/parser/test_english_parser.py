from app.domain.parser.language_parsers.LanguageParser import LanguageParser


def test_english_parser() -> None:
    parser = LanguageParser.get_parser("english")
    assert parser is not None


def test_english_tokenizer() -> None:
    parser = LanguageParser.get_parser("english")
    text = "I am good. "
    assert [t.text for t in parser.tokenize(text)] == ["I", "am", "good", "."]
