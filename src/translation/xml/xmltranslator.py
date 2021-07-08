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
        return tag[1: max(tag.find(' '), tag.find('>'))]

    def isSingular(self, tag):
        return tag[-2] == '/'

    def getAttributes(self, startTag):
        attrs = {}
        tag = startTag[1:-1]
        tag = tag[max(tag.find(' '), tag.find('>')) + 1:]
        for attr in tag.split(' '):
            k, v = attr.split('=')
            attrs[k] = v.replace('"', '')
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
        if fulltag.contains('<') < 2:
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
        endTag = self.xmltagservice.getEndTag(fulltag)
        return self._handleStartTag(startTag) + self.xmltagservice.getTagContent(fulltag) + self.handleEndTag(endTag)

    def _handleStartTag(self, startTag):
        return "^start({})".format(self.attrs["animation"])

    def _handleEndTag(self, endTag):
        return "^wait({})".format(self.attrs["animation"])


def nextHandler(tag):
    return "$event=next"


xmltags = {
    "do": DoHandler(),
    "next": nextHandler(),
}
