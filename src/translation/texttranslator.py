# coding=utf-8
import re
from naoxml.xmltranslator import XmlTranslator


class CharacaterNormalizer:
    def __init__(self):
        self.not_normalized_dic = {
            '“': '"',
            '”': '"',
            '«': '"',
            '»': '"'
        }

    def process(self, text):
        for k, v in self.not_normalized_dic.items():
            text = text.replace(k, v)
        return text


class DuplicateSpaceRemover:

    def __init__(self):
        pass  # empty init

    @staticmethod
    def process(text):
        return re.sub(" +", " ", text)


class TextTranslationSystem:
    def __init__(self, presentation):
        self.text_processors = [CharacaterNormalizer(),
                                XmlTranslator(presentation),
                                DuplicateSpaceRemover()]

    def translate(self, text):
        for processor in self.text_processors:
            text = processor.process(text)
        return text
