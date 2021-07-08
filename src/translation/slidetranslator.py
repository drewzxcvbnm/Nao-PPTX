from xml.xmltranslator import XmlTagService, XmlParsingException


class DepthFirstXmlParser:

    def __init__(self):
        self.xmlTagService = XmlTagService()

    def parse(self, text):
        self.text = text
        while self.text.find('<') != -1:
            lbound, rbound, tag = self._findTag(self.text)
            self._handleTag(lbound, rbound, tag, self.text[rbound + 1:])
        return self.text

    def _handleTag(self, lbound, rbound, tag, text):
        if self._isSingular(tag):
            r = self.xmlTagService.translate(tag)
            self._replace(lbound, rbound, r)
            return
        lbound2, rbound2, tag2 = self._findTag(text)
        if not self._isValidEndTag(tag, tag2):
            self._handlTag(lbound2, rbound2, tag2, text[rbound2 + 1:])
        r = self.xmlTagService.translate(text[lbound:rbound2])
        self._replace(lbound, rbound2, r)

    def _isValidEndTag(self, startTag, endTag):
        startName = self.xmlTagService.getTagName(startTag)
        endName = self.xmlTagService.getTagName(endTag)
        return startName == endName and endTag[1] == '/'

    def _findTag(self, text):
        lbound = text.find('<')
        rbound = text.find('>')
        tag = self.text[lbound:rbound + 1]
        if tag.count('<') > 1:
            raise XmlParsingException("Tag '{}' contains '<' within itself.".format(tag))
        return (lbound, rbound, tag)

    def _replace(self, lbound, rbound, replacement):
        self.text = self.text[:lbound] + replacement + self.text[rbound + 1:]

    def _isSingular(self, tag):
        return tag[-2] == '/'


class WidthFirstXmlParser:

    def __init__(self):
        self.xmlTagService = XmlTagService()

    def parse(self, text):
        self.text = text
        while self.text.find('<') != -1:
            tagFinder = self._getTagFinder(self.text)
            l1, r1, stag = next(tagFinder)
            if self._isSingular(stag):
                r = self.xmlTagService.translate(stag)
                self._replace(l1, r1, r)
                continue
            l2, r2, etag = self._getEndTag(stag, tagFinder)
            tag = self.text[l1:r2 + 1]
            r = self.xmlTagService.translate(tag)
            self._replace(l1, r2, r)
        return self.text

    def _getEndTag(self, stag, tagFinder):
        stagName = self.xmlTagService.getTagName(stag)
        numToFind = 1
        l, r, tag = None, None, None
        while numToFind > 0:
            l, r, tag = next(tagFinder)
            if self._isValidEndTag(stag, tag):
                numToFind -= 1
            elif self.xmlTagService.getTagName(tag) == stagName and not self._isSingular(tag):
                numToFind += 1
        return l, r, tag

    def _getTagFinder(self, text):
        while text.find('<') != -1:
            l, r, t = self._findTag(text)
            text = text[r + 1:]
            yield l, r, t

    def _replace(self, lbound, rbound, replacement):
        self.text = self.text[:lbound] + replacement + self.text[rbound + 1:]

    def _findTag(self, text):
        lbound = text.find('<')
        rbound = text.find('>')
        tag = self.text[lbound:rbound + 1]
        if tag.count('<') > 1:
            raise XmlParsingException("Tag '{}' contains '<' within itself.".format(startTag))
        return (lbound, rbound, tag)

    def _isSingular(self, tag):
        return tag[-2] == '/'

    def _isValidEndTag(self, startTag, endTag):
        startName = self.xmlTagService.getTagName(startTag)
        endName = self.xmlTagService.getTagName(endTag)
        return startName == endName and endTag[1] == '/'


class SlideTranslationSystem:
    parsers = [WidthFirstXmlParser()]

    @staticmethod
    def translate(slideText):
        for parser in SlideTranslationSystem.parsers:
            slideText = parser.parse(slideText)
        return slideText
