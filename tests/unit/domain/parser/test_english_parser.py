from app.domain.parser import LanguageParser


def test_english_parser() -> None:
    parser = LanguageParser.get_parser("english")
    assert parser is not None


def test_english_tokenizer() -> None:
    parser = LanguageParser.get_parser("english")
    text = "I am good. "
    assert [t.word_string for t in parser.tokenize(text)] == ["I", "am", "good", "."]
