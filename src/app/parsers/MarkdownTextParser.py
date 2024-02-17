from dataclasses import dataclass

import mistune
from dacite import from_dict

__all__ = (
    "BlockSegment",
    "EmptySegment",
    "HardLineBreakSegment",
    "ImageSegment",
    "MarkDownNode",
    "NodeAttr",
    "ParagraphSegment",
    "SoftLineBreakSegment",
    "TextParagraphSegment",
    "TextToken",
    "TokenSentence",
    "WordToken",
    "flatten_segments",
    "parse_node",
    "parse_paragraph",
    "markdown",
)

markdown = mistune.create_markdown(renderer=None)


@dataclass
class TextToken:
    token_string: str
    token_lemma: str
    token_pos: str
    is_eos: bool = False
    is_punct: bool = False


# kw_only for dataclass inheritance
# https://medium.com/@aniscampos/python-dataclass-inheritance-finally-686eaf60fbb5
@dataclass(kw_only=True)
class WordToken:
    word_string: str
    word_lemma: str
    word_pos: str
    is_multiple_words: bool = False
    is_word: bool = False
    is_eos: bool = False
    next_is_ws: bool = False
    word_status: int = 0


@dataclass(kw_only=True)
class VWord(WordToken):
    word_pronunciation: str | None = None
    word_explanation: str | None = None
    word_tokens: list[str]


@dataclass
class TokenSentence:
    segment_value: list[VWord]
    segment_raw: str = ""
    segment_type: str = "sentence"
    paragraph_order: int = 0
    sentence_order: int = 0


@dataclass
class ImageSegment:
    segment_value: str
    segment_raw: str = ""
    segment_type: str = "image"


@dataclass
class TextRawParagraphSegment:
    segment_value: str
    segment_type: str = "textrawparagraph"


@dataclass
class TextParagraphSegment:
    segment_value: list[TokenSentence]
    segment_raw: str = ""
    segment_type: str = "textparagraph"
    segment_order: int = 0


@dataclass
class SoftLineBreakSegment:
    segment_value: str
    segment_raw: str = ""
    segment_type: str = "softlinebreak"


@dataclass
class ParagraphSegment:
    segment_value: list[ImageSegment | TextParagraphSegment | SoftLineBreakSegment]
    segment_raw: str = ""
    segment_type: str = "paragraph"


@dataclass
class BlockSegment:
    segment_value: str
    segment_raw: str = ""
    segment_type: str = "block"


@dataclass
class HardLineBreakSegment:
    segment_value: str
    segment_raw: str = ""
    segment_type: str = "hardlinebreak"


@dataclass
class EmptySegment:
    segment_raw: str = ""
    segment_value: str = ""


# @dataclass
# class Segment:
Segment = (
    ImageSegment
    | SoftLineBreakSegment
    | HardLineBreakSegment
    | BlockSegment
    | ParagraphSegment
    | EmptySegment
    | TextRawParagraphSegment
)


@dataclass
class NodeAttr:
    url: str | None
    info: str | None


@dataclass
class MarkDownNode:
    type: str  # noqa
    raw: str | None
    attrs: NodeAttr | None
    children: list["MarkDownNode"] | None = None


def parse_paragraph(paragraph: MarkDownNode) -> ParagraphSegment:
    if paragraph.children is None:
        raise ValueError(f"No children found for paragraph: {paragraph}")

    def parse_child(child: MarkDownNode) -> ImageSegment | TextRawParagraphSegment | SoftLineBreakSegment:
        match child.type:
            case "text" | "codespan":  # treat text in double quote as normal text
                return TextRawParagraphSegment(child.raw)
            case "softbreak":
                return SoftLineBreakSegment("")
            case "image":
                return ImageSegment(child.attrs.url)
            # case "codespan":
        raise ValueError(f"Unknown child type of paragraph: {child.type}")

    return ParagraphSegment(segment_value=[parse_child(child) for child in paragraph.children])


def parse_node(node: MarkDownNode) -> Segment:
    match node.type:
        case "paragraph":
            return parse_paragraph(node)
        case "blank_line":
            return HardLineBreakSegment(segment_value="")
        case "block_code":
            return BlockSegment(segment_value=node.raw)
        case "heading":
            return EmptySegment()
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


if __name__ == "__main__":
    source_text_file = "../test/source.txt"
    with open(source_text_file) as f:  # noqa
        doc = markdown(f.read())
    segments = [parse_node(from_dict(data_class=MarkDownNode, data=m)) for m in doc]

    res = flatten_segments(segments)
    r = {s.segment_type for s in res}
