import dataclasses
from dataclasses import dataclass
from enum import StrEnum
from itertools import chain
from typing import NotRequired, TypedDict

import mistune
from mistune.markdown import Markdown

__all__ = (
    "MarkDownNode",
    "ParagraphSegment",
    "SoftLineBreakSegment",
    "TextParagraphSegment",
    "SentenceSegment",
    "WordToken",
    "TextRawParagraphSegment",
    "parse_markdown",
    "ParsedTextSegment",
    "Segment",
    "VWord",
)

markdown: Markdown = mistune.create_markdown(renderer=None)
PAGE_SEPERATOR_RE = r"^===(?P<page_sep>.+?)===$"


def parse_block_page(block, m, state):  # type: ignore
    text = m.group("page_sep")
    # use ``state.append_token`` to save parsed block math token
    state.append_token({"type": "page_seperator", "raw": text})
    # return the end position of parsed text
    # since python doesn't count ``$``, we have to +1
    # if the pattern is not ended with `$`, we can't +1
    return m.end() + 1


markdown.block.register("page_seperator", PAGE_SEPERATOR_RE, parse_block_page, before="list")


class AttrNode(TypedDict):
    url: NotRequired[str]
    info: NotRequired[str]


class MarkDownNode(TypedDict):
    type: str
    raw: NotRequired[str]
    children: NotRequired[list["MarkDownNode"]]
    attrs: NotRequired[AttrNode]


class SegmentType(StrEnum):
    IMAGE = "image"
    SOFT_LINEBREAK = "softlinebreak"
    HARD_LINEBREAK = "hardlinebreak"
    BLOCK = "block"
    PARAGRAPH = "paragraph"
    EMPTY = "empty"
    TEXT_PARAGRAPH = "textparagraph"
    TEXT_RAW_PARAGRAPH = "textrawparagraph"
    PAGE_START = "pagestart"
    PAGE_END = "pageend"
    SENTENCE = "sentence"
    SEGMENT = "segment"


# kw_only for dataclass inheritance
# https://medium.com/@aniscampos/python-dataclass-inheritance-finally-686eaf60fbb5
@dataclass(kw_only=True)
class WordToken:
    """
    using for parsedToken
    """

    word_string: str
    word_lemma: str
    word_pos: str
    is_word: bool = False
    next_is_ws: bool = False
    word_pronunciation: str = ""
    pos_extra: str = ""


@dataclass
class VWord(WordToken):
    """
    using for frontend
    """

    word_tokens: list[str]
    word_status: int = 0
    is_multiple_words: bool = False
    word_explanation: str = ""
    word_image_src: str | None = None
    word_db_id: int = -1


@dataclass
class SentenceSegment:
    segment_value: list[VWord]
    segment_raw: str = ""
    segment_type: str = SegmentType.SENTENCE
    paragraph_order: int = 0
    sentence_order: int = 0


@dataclass
class ParsedTextSegment:
    segment_words: list[VWord] = dataclasses.field(
        default_factory=list,
    )
    segment_value: str = ""
    segment_raw: str = ""
    segment_type: str = ""
    paragraph_order: int = 0
    sentence_order: int = 0


@dataclass
class BaseSegment:
    segment_value: str = ""
    segment_raw: str = ""
    segment_type: str = SegmentType.SEGMENT


@dataclass
class ImageSegment(BaseSegment):
    segment_type: str = SegmentType.IMAGE


@dataclass
class TextRawParagraphSegment(BaseSegment):
    segment_type: str = SegmentType.TEXT_RAW_PARAGRAPH


@dataclass
class TextParagraphSegment:
    segment_value: list[SentenceSegment]
    segment_raw: str = ""
    segment_type: str = SegmentType.TEXT_PARAGRAPH
    segment_order: int = 0


@dataclass
class SoftLineBreakSegment(BaseSegment):
    segment_type: str = SegmentType.SOFT_LINEBREAK


@dataclass
class PageStart(BaseSegment):
    segment_type: str = SegmentType.PAGE_START


@dataclass
class PageEnd(BaseSegment):
    segment_type: str = SegmentType.PAGE_END


@dataclass
class ParagraphSegment:
    segment_value: list[ImageSegment | TextRawParagraphSegment | SoftLineBreakSegment | PageStart | PageEnd]
    segment_raw: str = ""
    segment_type: str = SegmentType.PARAGRAPH


@dataclass
class BlockSegment(BaseSegment):
    segment_type: str = SegmentType.BLOCK


@dataclass
class HardLineBreakSegment(BaseSegment):
    segment_type: str = SegmentType.HARD_LINEBREAK


@dataclass
class EmptySegment(BaseSegment):
    segment_type: str = SegmentType.EMPTY


type Segment = (  # type: ignore[valid-type]
    ImageSegment
    | SoftLineBreakSegment
    | HardLineBreakSegment
    | BlockSegment
    | ParagraphSegment
    | EmptySegment
    | TextRawParagraphSegment
    | PageStart
    | PageEnd
)


@dataclass
class NodeAttr:
    url: str | None
    info: str | None


def parse_paragraph(paragraph: MarkDownNode) -> list[Segment]:
    # if paragraph["children"] is None:
    #     raise ValueError(f"No children found for paragraph: {paragraph}")

    def parse_child(
        child: MarkDownNode,
    ) -> Segment:
        match child:
            case {"type": "text" | "codespan", "raw": raw}:  # treat text in double quote as normal text
                return TextRawParagraphSegment(raw)
            case {"type": "softbreak"}:
                return SoftLineBreakSegment()
            case {"type": "image", "attrs": {"url": url}}:
                return ImageSegment(url)
            case _:
                raise ValueError(f"Unknown child type of paragraph: {child['type']}")

    return [parse_child(child) for child in paragraph["children"]]


def parse_node(node: MarkDownNode) -> list[Segment]:
    match node:
        case {"type": "page_seperator", "raw": seperator_type}:
            match seperator_type:
                case "page_start":
                    return [PageStart()]
                case "page_end":
                    return [PageEnd()]
                case _:
                    raise ValueError(f"Unknown seperator type: {seperator_type}")
        case {"type": "paragraph", "children": children}:
            return parse_paragraph({"type": "paragraph", "children": children})
        case {"type": "blank_line"}:
            return [HardLineBreakSegment()]
        case {"type": "block_code", "raw": raw}:
            return [BlockSegment(segment_value=raw)]
        case {"type": "heading"}:
            return [EmptySegment()]
        case _:
            raise ValueError(f"Unrecognized markdown node: {node}")


def parse_markdown(text: str) -> list[Segment]:
    _doc: list[MarkDownNode] = markdown(text)
    return list(chain.from_iterable(parse_node(m) for m in _doc))


if __name__ == "__main__":
    source_text_file = "test.md"
    with open(source_text_file) as f:  # noqa
        doc: str = f.read()
    segments = parse_markdown(doc)

    r = {s.segment_type for s in segments}
    print(r)  # noqa
