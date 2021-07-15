# coding=utf-8
from naoxml.xmltranslator import XmlTagService, XmlTranslationException
from naoxml.xmltag import XmlTag
from naoxml.xmlfinder import XmlFinder
import re


class WidthFirstXmlTranslator:

    def __init__(self):
        self.xmlTagService = XmlTagService()
        self.xmlFinder = XmlFinder()

    def process(self, text):
        self.text = text
        while self.text.find('<') != -1:
            l, r, t = self.xmlFinder.findXmlTag(self.text)
            t = self.xmlTagService.translateTag(t)
            self._replace(l, r, t)
        return self.text.replace("{split}","<split/>")

    def _replace(self, lbound, rbound, replacement):
        self.text = self.text[:lbound] + replacement + self.text[rbound + 1:]


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
        print text
        return text


class DuplicateSpaceRemover:

    def process(self, text):
        return re.sub(" +", " ", text)


class TextTranslationSystem:
    textProcessors = [CharacaterNormalizer(),
                      WidthFirstXmlTranslator(),
                      DuplicateSpaceRemover()]

    @staticmethod
    def translate(text):
        for processor in TextTranslationSystem.textProcessors:
            text = processor.process(text)
        return text
