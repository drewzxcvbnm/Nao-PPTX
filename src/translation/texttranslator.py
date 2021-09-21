# coding=utf-8
from naoxml.xmltranslator import XmlTagService
from naoxml.xmltag import XmlTag
from naoxml.xmlfinder import XmlFinder
import re


class XmlTranslator:

    def __init__(self):
        self.xml_tag_service = XmlTagService()
        self.xml_finder = XmlFinder()

    def process(self, text):
        r = XmlTag(XmlTag(self._xmlwrap(text)).get_translated_tag_as_string())
        if r.name == "temptag":
            return r.content
        return r.str

    @staticmethod
    def _xmlwrap(text):
        if text[0] == '<':
            return text
        return "<temptag>" + text + "</temptag>"


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
    def __init__(self):
        pass  # empty init

    text_processors = [CharacaterNormalizer(),
                       XmlTranslator(),
                       DuplicateSpaceRemover()]

    @staticmethod
    def translate(text):
        for processor in TextTranslationSystem.text_processors:
            text = processor.process(text)
        return text
