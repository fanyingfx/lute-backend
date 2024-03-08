from app.domain.parser import LanguageParser


def test_japanese_parser() -> None:
    parser = LanguageParser.get_parser("japanese")
    assert parser is not None


def test_japanese_tokenizer() -> None:
    parser = LanguageParser.get_parser("japanese")
    text = "私は元気です。"
    assert [t.word_string for t in parser.tokenize(text)] == ["私", "は", "元気", "です", "。"]
