"""
Match word in list, update status, explanation...etc.

"""
import builtins
from collections import defaultdict

from spacy.tokens import Span as TokenSpan

from app.domain.words.models import Word

__all__ = (
    "WordIndex",
    "get_str",
    "match_word_in_sentence",
)


class WordIndex:
    def _init_word_list(self, word_list: list[Word]):
        word_index = defaultdict(list)
        for db_word in word_list:
            if len(db_word.word_tokens) == 0:
                raise ValueError(f"Empty word list: {db_word}")
            # using first word as key for quick search
            # I think one level is enough
            word_index[db_word[0]].append(db_word)
        # using inplace sort to sort the word list
        for key in word_index:
            word_index[key].sort(key=len, reverse=True)
        return word_index

    def __init__(self, word_list: list[Word]):
        self._word_index = self._init_word_list(word_list)

    def __contains__(self, key):
        return key in self._word_index

    def __getitem__(self, key) -> Word:
        return self._word_index[key]

    def __repr__(self):
        return repr(self._word_index)


def get_str(word_token: Word | str | TokenSpan):
    match word_token:
        case builtins.str:
            return word_token
        case Word():
            return word_token.word_string
        case TokenSpan():
            return str(word_token)
    raise ValueError(f"Invalid word token: {word_token}")


# def get_list(word_list:list[Word]|list[str]):
# if not isinstance(word_list, list):


def match_word_in_sentence(sentence_tokens, word_index: WordIndex) -> str:
    start_position = 0
    words_res = []
    count = 0
    while start_position < len(sentence_tokens):
        current_word = sentence_tokens[start_position]
        if current_word in word_index:
            for words_list in word_index[current_word]:
                end_position = start_position
                for word in words_list:
                    if end_position >= len(sentence_tokens) or word != sentence_tokens[end_position]:
                        break
                    end_position += 1
                else:
                    words_res.append(sentence_tokens[start_position:end_position])
                    start_position = end_position
        else:
            words_res.append(sentence_tokens[start_position])
            start_position += 1
        count += 1
        if count > 5000:
            raise OverflowError("Maximum number of word in sentence exceeded!5000! or maybe in the dead loop!")
    return words_res


if __name__ == "__main__":
    import spacy

    nlp = spacy.load("en_core_web_sm")
    words = [["hello", "world"], ["have", "to"], ["hello"], ["have", "to", "go"], ["to", "go"]]
    wi = WordIndex(words)
    text = "Hello there, I have to go home now."
    doc = nlp(text)
    tokens = [t.text for t in doc]
    res = match_word_in_sentence(sentence_tokens=tokens, word_index=wi)
#
