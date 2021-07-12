from xmlparsingexception import XmlParsingException
from xmltag import XmlTag

xmltags = {}
animationNamespace = None


def StrToXmlTag(function):
    def wrapper(tagAsStr):
        tag = XmlTag(tagAsStr)
        return function(tag)

    return wrapper


class XmlTagService:

    def translateTag(self, tag):
        tag = XmlTag(tag)
        name = tag.getTagName()
        if name not in xmltags.keys():
            raise XmlParsingException("Cannot translate tag {}:{}".format(name, tag.str))
        return xmltags[name](tag.str)


class DoHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.getAttributes()
        if tag.str.count('<') == 1:
            return self._handleStartTag()
        return self._handleStartTag() + tag.getTagContent() + self._handleEndTag()

    def _handleStartTag(self):
        givenPath = self.attrs["animation"]
        path = givenPath if animationNamespace is None else animationNamespace + givenPath
        return "^start({}) ".format(path)

    def _handleEndTag(self):
        givenPath = self.attrs["animation"]
        path = givenPath if animationNamespace is None else animationNamespace + givenPath
        return " ^wait({}) ".format(path)


def nextHandler(tag):
    return " $event=next "


@StrToXmlTag
def pauseHandler(tag):
    attrs = tag.getAttributes()
    return " \\pau={}\\ ".format(attrs.get('time', 100))


@StrToXmlTag
def emphHandler(tag):
    attrs = tag.getAttributes()
    if "word" not in attrs.keys():
        raise XmlParsingException("Emph tag. Missing 'word' attribute")
    if "pos" not in attrs.keys():
        raise XmlParsingException("Emph tag. Missing 'pos' attribute")
    return " \\emph={}\\ {} ".format(attrs["pos"], attrs["word"])


@StrToXmlTag
def setHandler(tag):
    attrs = tag.getAttributes()
    ret = ""
    if "voice" in attrs.keys():
        ret += " \\style={}\\ ".format(attrs["voice"])
    if "animation-ns" in attrs.keys():
        global animationNamespace
        animationNamespace = attrs["animation-ns"].rstrip("/") + "/"
    return ret


xmltags = {
    "do": DoHandler(),
    "next": nextHandler,
    "pause": pauseHandler,
    "emph": emphHandler,
    "set": setHandler
}
