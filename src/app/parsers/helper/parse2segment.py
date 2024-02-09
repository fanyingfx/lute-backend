import random
from collections.abc import Iterator
from dataclasses import dataclass

import mistune
import spacy
from dacite import from_dict
from spacy.tokens import Span

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
    "parse_text",
    "split_sentence",
)


nlp = spacy.load("en_core_web_sm")
markdown = mistune.create_markdown(renderer=None)


@dataclass
class TextToken:
    token_string: str
    token_lemma: str
    token_pos: str
    is_eos: bool = False
    is_punct: bool = False


@dataclass
class WordToken:
    word_string: str
    word_lemma: str
    word_pos: str
    is_multiple_words: bool = False
    is_word: bool = False
    is_eos: bool = False
    next_is_ws: bool = False
    word_status: int = 0


@dataclass
class TokenSentence:
    segment_value: list[WordToken]
    segment_raw: str = ""

    segment_type: str = "sentence"


@dataclass
class ImageSegment:
    segment_value: str
    segment_raw: str = ""
    segment_type: str = "image"


@dataclass
class TextParagraphSegment:
    segment_value: list[TokenSentence]
    segment_raw: str = ""
    segment_type: str = "textparagraph"


@dataclass
class ParagraphSegment:
    segment_value: list[ImageSegment | TextParagraphSegment]
    segment_raw: str = ""
    segment_type: str = "paragraph"


@dataclass
class BlockSegment:
    segment_value: str
    segment_raw: str = ""
    segment_type: str = "block"


@dataclass
class SoftLineBreakSegment:
    segment_value: str
    segment_raw: str = ""
    segment_type: str = "softlinebreak"


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
Segment = ImageSegment | SoftLineBreakSegment | HardLineBreakSegment | BlockSegment | ParagraphSegment | EmptySegment


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


def split_sentence(sentences: str) -> Iterator[Span]:
    return nlp(sentences).sents


def parse_text(text) -> TextParagraphSegment:
    token_sentences = []
    for sent in split_sentence(text):
        words = []
        for token in sent:
            words.append(
                WordToken(
                    word_string=token.text,
                    word_lemma=token.lemma_,
                    word_pos=token.pos_,
                    word_status=random.randint(0, 5),  # noqa
                    is_word=not token.is_punct,
                    is_eos=token.is_sent_end,
                    next_is_ws=token.whitespace_ == " ",
                    is_multiple_words=False,
                )
            )

        token_sentences.append(TokenSentence(segment_value=words))
    return TextParagraphSegment(segment_value=token_sentences, segment_raw=text)


def parse_paragraph(paragraph: MarkDownNode) -> ParagraphSegment:
    if paragraph.children is None:
        raise ValueError(f"No children found for paragraph: {paragraph}")

    def parse_child(child: MarkDownNode) -> list[Segment]:
        match child.type:
            case "text" | "codespan":  # treat text in double quote as normal text
                return parse_text(child.raw)
            case "softbreak":
                return SoftLineBreakSegment("")
            case "image":
                return ImageSegment(child.attrs.url)
            # case "codespan":
        raise ValueError(f"Unknown child type: {child.type}")

    return ParagraphSegment(segment_value=[parse_child(child) for child in paragraph.children])


def parse_node(node: MarkDownNode) -> Segment:
    match node.type:
        case "paragraph":
            return parse_paragraph(node)
        case "blank_line":
            return HardLineBreakSegment(segment_value="")
        case "block_code":
            return BlockSegment(segment_value=node.raw)
    raise ValueError(f"Unrecognized node: {node}")


def flatten_segments(segments: list[Segment]) -> list[Segment]:
    res_node_list: list[Segment] = []
    for segment in segments:
        match segment:
            case ParagraphSegment():
                res_node_list.extend(segment.segment_value)
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
