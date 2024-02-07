import random
from collections.abc import Iterator
from dataclasses import dataclass

import mistune
import spacy
from dacite import from_dict
from spacy.tokens import Span

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
    segment_type: str = "sentence"


@dataclass
class ImageSegment:
    segment_value: str
    segment_type: str = "image"


@dataclass
class TextParagraphSegment:
    segment_value: list[TokenSentence]
    segment_type: str = "textparagraph"


@dataclass
class ParagraphSegment:
    segment_value: list[ImageSegment | TextParagraphSegment]
    segment_type: str = "paragraph"


@dataclass
class BlockSegment:
    segment_value: str
    segment_type: str = "block"


@dataclass
class LineBreakSegment:
    segment_value: str
    segment_type: str = "linebreak"


@dataclass
class EmptySegment:
    segment_value: str = ""


# @dataclass
# class Segment:
Segment = [ImageSegment | LineBreakSegment | BlockSegment | ParagraphSegment | EmptySegment]


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
        return TextParagraphSegment(segment_value=token_sentences)
    return None


def parse_paragraph(paragraph: MarkDownNode) -> ParagraphSegment:
    if paragraph.children is None:
        raise ValueError(f"No children found for paragraph: {paragraph}")

    def parse_child(child: MarkDownNode) -> Segment:
        match child.type:
            case "text":
                return parse_text(child.raw)
            case "softbreak":
                return LineBreakSegment("")
            case "image":
                return ImageSegment(child.attrs.url)

    return ParagraphSegment(segment_value=[parse_child(child) for child in paragraph.children])


def parse_node(node: MarkDownNode) -> Segment:
    match node.type:
        case "paragraph":
            return parse_paragraph(node)
        case "blank_line":
            return LineBreakSegment(segment_value="\n")
        case "block_code":
            return BlockSegment(segment_value=node.raw)
    raise ValueError(f"Unrecognized node: {node}")


if __name__ == "__main__":
    source_text_file = "source.txt"
    with open(source_text_file) as f:  # noqa
        doc = markdown(f.read())

    res = [from_dict(data_class=MarkDownNode, data=m) for m in doc]
    # for md_node in res:
