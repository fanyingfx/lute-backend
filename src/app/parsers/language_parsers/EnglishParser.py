import spacy

from app.parsers.language_parsers.LanguageParser import LanguageParser, Singleton

__all__ = ("EnglishParser",)


@Singleton
class EnglishParser(LanguageParser):
    language_name = "english"

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def split_sentences(self, text):
        pass

    def split_sentences_and_tokenize(self, text):
        return self.nlp(text).sents

    @classmethod
    def get_language_name(cls):
        if not cls.language_name.islower():
            raise ValueError(f"Language name {cls.language_name} is not lowercase")
        return cls.language_name

    def tokenize(self, text):
        pass
