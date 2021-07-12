# coding=utf-8
from naoxml.xmltranslator import XmlTagService, XmlParsingException
from naoxml.xmltag import XmlTag
import re


def catchError(message, arg):
    def decorator(function):
        def inner(*args, **kwargs):
            a = None
            if isinstance(arg, int):
                a = args[arg]
            else:
                a = kwargs[arg]
            try:
                r = function(*args, **kwargs)
            except Exception as e:
                raise XmlParsingException(message + str(a))
            return r

        return inner

    return decorator


class WidthFirstXmlParser:

    def __init__(self):
        self.xmlTagService = XmlTagService()

    def parse(self, text):
        self.text = text
        while self.text.find('<') != -1:
            tagFinder = self._getTagFinder(self.text)
            l1, r1, stag = next(tagFinder)
            if self._isSingular(stag):
                r = self.xmlTagService.translateTag(stag)
                self._replace(l1, r1, r)
                continue
            l2, r2, etag = self._getEndTag(stag, tagFinder)
            tag = self.text[l1:r2 + 1]
            r = self.xmlTagService.translateTag(tag)
            self._replace(l1, r2, r)
        return self.text

    @catchError("Error finding end tag for:", 1)
    def _getEndTag(self, stag, tagFinder):
        stagName = XmlTag(stag).getTagName()
        numToFind = 1
        l, r, tag = None, None, None
        while numToFind > 0:
            l, r, tag = next(tagFinder)
            if self._isValidEndTag(stag, tag):
                numToFind -= 1
            elif XmlTag(tag).getTagName() == stagName and not self._isSingular(tag):
                numToFind += 1
        return l, r, tag

    def _getTagFinder(self, text):
        texti = 0
        while text.find('<') != -1:
            l, r, t = self._findTag(text)
            text = text[r + 1:]
            yield l + texti, r + texti, t
            texti += r + 1

    def _replace(self, lbound, rbound, replacement):
        self.text = self.text[:lbound] + replacement + self.text[rbound + 1:]

    def _findTag(self, text):
        lbound = text.find('<')
        rbound = text.find('>')
        tag = text[lbound:rbound + 1]
        if tag.count('<') > 1:
            raise XmlParsingException("Tag '{}' contains '<' within itself.".format(tag))
        return (lbound, rbound, tag)

    def _isSingular(self, tag):
        return tag[-2] == '/'

    def _isValidEndTag(self, startTag, endTag):
        startName = XmlTag(startTag).getTagName()
        endName = XmlTag(endTag).getTagName()
        return startName == endName and endTag[1] == '/'


class CharacaterNormalizer:
    def __init__(self):
        self.notNormalizedDic = {
            '“': '"',
            '”': '"',
            '«': '"',
            '»': '"'
        }

    def parse(self, text):
        for k, v in self.notNormalizedDic.items():
            text = text.replace(k, v)
        print text
        return text


class DuplicateSpaceRemover:

    def parse(self, text):
        return re.sub(" +", " ", text)


class SlideTranslationSystem:
    parsers = [CharacaterNormalizer(),
               WidthFirstXmlParser(),
               DuplicateSpaceRemover()]

    @staticmethod
    def translate(slideText):
        for parser in SlideTranslationSystem.parsers:
            slideText = parser.parse(slideText)
        return slideText
