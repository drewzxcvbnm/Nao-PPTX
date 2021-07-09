import re


class XmlParsingException(Exception):
    pass


xmltags = {}


class XmlTagService:

    def translateTag(self, fulltag):
        name = self.getTagName(fulltag)
        if name not in xmltags.keys():
            raise XmlParsingException("Cannot translate tag {}:{}".format(name, fulltag))
        return xmltags[name](fulltag)

    def getTagName(self, tag):
        if ' ' in tag:
            return tag[1: tag.find(' ')]
        return re.sub("(<|>|/)", "", tag)

    def isSingular(self, tag):
        return tag[-2] == '/'

    def getAttributes(self, startTag):
        attrs = {}
        name = self.getTagName(startTag)
        tag = re.sub("(<|>|/|{})".format(name), "", startTag).strip(" ")
        if tag == "":
            return attrs
        for attr in tag.split(' '):
            k, v = attr.split('=')
            start_search = v.find('"') + 1
            attrs[k] = v[start_search: v[start_search:].find('"') + 1]
        return attrs

    def getStartTag(self, fulltag):
        lbound = fulltag.find('<')
        rbound = fulltag.find('>')
        tag = fulltag[lbound:rbound + 1]
        return tag

    def getEndTag(self, fulltag):
        if fulltag.contains('<') < 2:
            raise XmlParsingException("Cannot extract end from:{}".format(fulltag))
        lbound = fulltag.rfind('<')
        rbound = fulltag.rfind('>')
        tag = fulltag[lbound:rbound + 1]
        return tag

    def getTagContent(self, fulltag):
        if fulltag.count('<') < 2:
            raise XmlParsingException("Cannot extract content from:{}".format(fulltag))
        srbound = fulltag.find('>')
        elbound = fulltag.rfind('<')
        return fulltag[srbound + 1:elbound]


class DoHandler:

    def __init__(self):
        self.xmltagservice = XmlTagService()

    def __call__(self, fulltag):
        startTag = self.xmltagservice.getStartTag(fulltag)
        self.attrs = self.xmltagservice.getAttributes(startTag)
        if fulltag.count('<') == 1:
            return self._handleStartTag(fulltag)
        return self._handleStartTag() + self.xmltagservice.getTagContent(fulltag) + self._handleEndTag()

    def _handleStartTag(self):
        return "^start({}) ".format(self.attrs["animation"])

    def _handleEndTag(self):
        return " ^wait({}) ".format(self.attrs["animation"])


def nextHandler(tag):
    return "$event=next"


def pauseHandler(tag):
    s = XmlTagService()
    attrs = s.getAttributes(tag)
    return "\\pau={}\\".format(attrs.get('time', 100))


xmltags = {
    "do": DoHandler(),
    "next": nextHandler,
    "pause": pauseHandler,
}
