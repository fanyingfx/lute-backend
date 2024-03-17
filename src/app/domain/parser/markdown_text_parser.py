import dataclasses
from dataclasses import dataclass
from typing import NotRequired, TypedDict

import mistune
from mistune.markdown import Markdown
from mistune.plugins.formatting import mark

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

markdown: Markdown = mistune.create_markdown(renderer=None, plugins=[mark])


class AttrNode(TypedDict):
    url: NotRequired[str]
    info: NotRequired[str]


class MarkDownNode(TypedDict):
    type: str
    raw: NotRequired[str]
    children: NotRequired[list["MarkDownNode"]]
    attrs: NotRequired[AttrNode]


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
    segment_type: str = "sentence"
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
    segment_type: str = "segment"


@dataclass
class ImageSegment(BaseSegment):
    segment_type: str = "image"


@dataclass
class TextRawParagraphSegment(BaseSegment):
    segment_type: str = "textrawparagraph"


@dataclass
class TextParagraphSegment:
    segment_value: list[SentenceSegment]
    segment_raw: str = ""
    segment_type: str = "textparagraph"
    segment_order: int = 0


@dataclass
class SoftLineBreakSegment(BaseSegment):
    segment_type: str = "softlinebreak"


@dataclass
class PageSeperator(BaseSegment):
    segment_type: str = "pageseperator"


@dataclass
class ParagraphSegment:
    segment_value: list[ImageSegment | TextRawParagraphSegment | SoftLineBreakSegment | PageSeperator]
    segment_raw: str = ""
    segment_type: str = "paragraph"


@dataclass
class BlockSegment(BaseSegment):
    segment_type: str = "block"


@dataclass
class HardLineBreakSegment(BaseSegment):
    segment_type: str = "hardlinebreak"


@dataclass
class EmptySegment(BaseSegment):
    segment_type: str = "empty"


type Segment = (  # type: ignore[valid-type]
    ImageSegment
    | SoftLineBreakSegment
    | HardLineBreakSegment
    | BlockSegment
    | ParagraphSegment
    | EmptySegment
    | TextRawParagraphSegment
    | PageSeperator
)


@dataclass
class NodeAttr:
    url: str | None
    info: str | None


def parse_paragraph(paragraph: MarkDownNode) -> ParagraphSegment:
    # if paragraph["children"] is None:
    #     raise ValueError(f"No children found for paragraph: {paragraph}")

    def parse_child(
        child: MarkDownNode,
    ) -> ImageSegment | TextRawParagraphSegment | SoftLineBreakSegment | PageSeperator:
        match child:
            case {"type": "text" | "codespan", "raw": raw}:  # treat text in double quote as normal text
                return TextRawParagraphSegment(raw)
            case {"type": "softbreak"}:
                return SoftLineBreakSegment()
            case {"type": "image", "attrs": {"url": url}}:
                return ImageSegment(url)
            case {"type": "mark", "children": [{"raw": "page_seperator", "type": "text"}]}:
                return PageSeperator()
        raise ValueError(f"Unknown child type of paragraph: {child['type']}")

    return ParagraphSegment(segment_value=[parse_child(child) for child in paragraph["children"]])


def parse_node(node: MarkDownNode) -> Segment:
    match node:
        case {"type": "paragraph", "children": children}:
            return parse_paragraph({"type": "paragraph", "children": children})
        case {"type": "blank_line"}:
            return HardLineBreakSegment(segment_value="")
        case {"type": "block_code", "raw": raw}:
            return BlockSegment(segment_value=raw)
        case {"type": "heading"}:
            return EmptySegment()
        case _:
            raise ValueError(f"Unrecognized markdown node: {node}")


def flatten_segments(segments: list[Segment]) -> list[Segment]:
    res_node_list: list[Segment] = []
    for segment in segments:
        match segment:
            case ParagraphSegment():
                res_node_list.extend(segment.segment_value)
            case EmptySegment():
                pass
            case _:
                res_node_list.append(segment)
    return res_node_list


def parse_markdown(text: str) -> list[Segment]:
    _doc: list[MarkDownNode] = markdown(text)
    _segments = [parse_node(m) for m in _doc]
    return flatten_segments(_segments)


if __name__ == "__main__":
    source_text_file = "test.md"
    with open(source_text_file) as f:  # noqa
        doc: list[MarkDownNode] = markdown(f.read())
    segments = [parse_node(m) for m in doc]

    res = flatten_segments(segments)
    r = {s.segment_type for s in res}
    print(r)  # noqa
