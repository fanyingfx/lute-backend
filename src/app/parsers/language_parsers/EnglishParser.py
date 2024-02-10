import spacy

from app.parsers.language_parsers.LanguageParser import LanguageParser, Singleton

__all__ = ("EnglishParser",)


@Singleton
class EnglishParser(LanguageParser):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def split_sentences(self, text):
        pass

    def split_sentences_and_tokenize(self, text):
        return self.nlp(text).sents

    def tokenize(self, text):
        pass
