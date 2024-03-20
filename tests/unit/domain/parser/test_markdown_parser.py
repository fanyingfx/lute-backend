# mypy: ignore-errors
import pytest

from app.domain.parser.markdown_text_parser import (
    BlockSegment,
    HardLineBreakSegment,
    MarkDownNode,
    PageEnd,
    PageStart,
    TextRawParagraphSegment,
    parse_markdown,
    parse_node,
    parse_paragraph,
)


def test_parse_markdown_with_empty_string():
    assert parse_markdown("") == [HardLineBreakSegment()]


def test_parse_markdown_with_page_seperator():
    assert parse_markdown("===page_start===") == [PageStart()]
    assert parse_markdown("===page_end===") == [PageEnd()]


def test_parse_markdown_with_paragraph():
    text = "This is a paragraph."
    assert isinstance(parse_markdown(text)[0], TextRawParagraphSegment)


def test_parse_markdown_with_block_code() -> None:
    text = """```
    This is a block code.
    ```"""
    assert isinstance(parse_markdown(text)[0], BlockSegment)


def test_parse_node_with_unrecognized_type():
    node = MarkDownNode(type="unrecognized", raw="raw")
    with pytest.raises(ValueError):
        parse_node(node)


def test_parse_paragraph_with_unknown_child_type():
    paragraph = MarkDownNode(type="paragraph", children=[MarkDownNode(type="unknown", raw="raw")])
    with pytest.raises(ValueError):
        parse_paragraph(paragraph)
