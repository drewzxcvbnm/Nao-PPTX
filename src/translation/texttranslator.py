# coding=utf-8
from naoxml.xmltranslator import XmlTagService, XmlTranslationException
from naoxml.xmltag import XmlTag
from naoxml.xmlfinder import XmlFinder
import re


class XmlTranslator:

    def __init__(self):
        self.xmlTagService = XmlTagService()
        self.xmlFinder = XmlFinder()

    def process(self, text):
        r = XmlTag(XmlTag(self._xmlwrap(text)).getTranslatedTagAsString())
        if r.getTagName() == "temptag":
            return r.getTagContent()
        return r.str

    def _xmlwrap(self, text):
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

    def process(self, text):
        return re.sub(" +", " ", text)


class TextTranslationSystem:
    textProcessors = [CharacaterNormalizer(),
                      XmlTranslator(),
                      DuplicateSpaceRemover()]

    @staticmethod
    def translate(text):
        for processor in TextTranslationSystem.textProcessors:
            text = processor.process(text)
        return text
