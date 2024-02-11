from tokenize import Token

from pytest import fixture

from app.domain.books.services import match_word_in_sentence
from app.domain.words.models import Word
from app.domain.words.services import WordIndex
from app.parsers.language_parsers.EnglishParser import EnglishParser
from app.parsers.MarkdownTextParser import VWord


# async def match_word_in_sentence(sentence: Iterable[Token], max_loop_num: int,word_index:WordIndex) -> TokenSentence:
def assert_vword_equal(vword1: VWord, vword2: VWord) -> None:
    assert all(
        [
            vword1.word_string == vword2.word_string,
            vword1.word_lemma == vword2.word_lemma,
            vword1.word_pos == vword2.word_pos,
            vword1.word_explanation == vword2.word_explanation,
            vword1.is_multiple_words == vword2.is_multiple_words,
            vword1.next_is_ws == vword2.next_is_ws,
            vword1.word_status == vword2.word_status,
            vword1.is_eos == vword2.is_eos,
            vword1.is_word == vword2.is_word,
        ]
    )


def assert_vword_list_equal(vwordlist1, vwordlist2) -> None:
    for vword1, vword2 in zip(vwordlist1, vwordlist2):
        assert_vword_equal(vword1, vword2)


@fixture()
def word_index() -> WordIndex:
    word1 = Word(
        word_string="have",
        word_lemma="have",
        word_pos="v",
        is_multiple_words=False,
        word_status=1,
        word_pronunciation="",
        word_explanation="own",
        word_counts=1,
        word_tokens=["have"],
    )
    word2 = Word(
        word_string="have to",
        word_lemma="have to",
        word_pos="v",
        is_multiple_words=True,
        word_status=2,
        word_pronunciation="",
        word_explanation="must do something",
        word_counts=2,
        word_tokens=["have", "to"],
    )

    return WordIndex([word1, word2])


@fixture()
def sentence_tokens() -> list[Token]:
    english_parser: EnglishParser = EnglishParser()
    sentence = "I have to go home."
    sents = english_parser.split_sentences_and_tokenize(sentence)

    return list(next(sents))  # in the test case, there only one sentence.


@fixture()
async def get_vwords(sentence_tokens, word_index) -> list[VWord]:
    max_loop_num = len(sentence_tokens) * 100
    token_sentence = await match_word_in_sentence(sentence_tokens, word_index, max_loop_num)
    return token_sentence.segment_value


@fixture()
def expectedVwords():
    return [
        VWord(
            word_string="I",
            word_lemma="I",
            word_pos="PRON",
            is_multiple_words=False,
            is_word=True,
            is_eos=False,
            next_is_ws=True,
            word_status=0,
            word_pronunciation="",
            word_explanation="",
        ),
        VWord(
            word_string="have to",
            word_lemma="have to",
            word_pos="v",
            is_multiple_words=True,
            is_word=True,
            is_eos=False,
            next_is_ws=True,
            word_status=2,
            word_pronunciation="",
            word_explanation="must do something",
        ),
        VWord(
            word_string="go",
            word_lemma="go",
            word_pos="VERB",
            is_multiple_words=False,
            is_word=True,
            is_eos=False,
            next_is_ws=True,
            word_status=0,
            word_pronunciation="",
            word_explanation="",
        ),
        VWord(
            word_string="home",
            word_lemma="home",
            word_pos="ADV",
            is_multiple_words=False,
            is_word=True,
            is_eos=False,
            next_is_ws=False,
            word_status=0,
            word_pronunciation="",
            word_explanation="",
        ),
        VWord(
            word_string=".",
            word_lemma=".",
            word_pos="PUNCT",
            is_multiple_words=False,
            is_word=False,
            is_eos=True,
            next_is_ws=False,
            word_status=0,
            word_pronunciation="",
            word_explanation="",
        ),
    ]


def test_match_word_in_sentece(get_vwords, expectedVwords):
    assert_vword_list_equal(get_vwords, expectedVwords)
