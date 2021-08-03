# coding=utf-8
from naoxml.xmltranslator import XmlTagService
from naoxml.xmltag import XmlTag
from naoxml.xmlfinder import XmlFinder
import re


class XmlTranslator:

    def __init__(self):
        self.xmlTagService = XmlTagService()
        self.xmlFinder = XmlFinder()

    def process(self, text):
        r = XmlTag(XmlTag(self._xmlwrap(text)).get_translated_tag_as_string())
        if r.tag_name == "temptag":
            return r.content
        return r.str

    @staticmethod
    def _xmlwrap(text):
        if text[0] == '<':
            return text
        return "<temptag>" + text + "</temptag>"


class CharacaterNormalizer:
    def __init__(self):
        self.notNormalizedDic = {
            '“': '"',
            '”': '"',
            '«': '"',
            '»': '"'
        }

    def process(self, text):
        for k, v in self.notNormalizedDic.items():
            text = text.replace(k, v)
        return text


class DuplicateSpaceRemover:

    def __init__(self):
        pass

    @staticmethod
    def process(text):
        return re.sub(" +", " ", text)


class TextTranslationSystem:
    def __init__(self):
        pass

    textProcessors = [CharacaterNormalizer(),
                      XmlTranslator(),
                      DuplicateSpaceRemover()]

    @staticmethod
    def translate(text):
        for processor in TextTranslationSystem.textProcessors:
            text = processor.process(text)
        return text
