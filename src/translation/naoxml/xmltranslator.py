from xmltranslationexception import XmlTranslationException
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
            return tag.str
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
        raise XmlTranslationException("Emph tag. Missing 'word' attribute")
    if "pos" not in attrs.keys():
        raise XmlTranslationException("Emph tag. Missing 'pos' attribute")
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


class RmodeHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.getAttributes()
        if tag.isSingular():
            return self._handleStartTag()
        return self._handleStartTag() + tag.getTagContent() + self._handleEndTag()

    def _handleStartTag(self):
        mode = self.attrs["mode"]
        return " \\readmode={}\\ ".format(mode)

    def _handleEndTag(self):
        return " \\readmode=sent\\ "


class VolHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.getAttributes()
        if tag.isSingular():
            return self._handleStartTag()
        return self._handleStartTag() + tag.getTagContent() + self._handleEndTag()

    def _handleStartTag(self):
        value = self.attrs["value"]
        return " \\vol={}\\ ".format(value)

    def _handleEndTag(self):
        return " \\vol=100\\ "


class RspdHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.getAttributes()
        if tag.isSingular():
            return self._handleStartTag()
        return self._handleStartTag() + tag.getTagContent() + self._handleEndTag()

    def _handleStartTag(self):
        speed = self.attrs["speed"]
        return " \\rspd={}\\ ".format(speed)

    def _handleEndTag(self):
        return " \\rspd=100\\ "


@StrToXmlTag
def rstHandler(tag):
    return " \\rst\\ "


class VideoHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.getAttributes()
        if tag.isSingular():
            return " $event=startvideo <split/> "
        return self._handleStartTag() + tag.getTagContent() + self._handleEndTag()

    def _handleStartTag(self):
        return " $event=startvideo "

    def _handleEndTag(self):
        return " <split/> "


xmltags = {
    "do": DoHandler(),
    "next": nextHandler,
    "pause": pauseHandler,
    "emph": emphHandler,
    "set": setHandler,
    "rspd": RspdHandler(),
    "vol": VolHandler(),
    "rmode": RmodeHandler(),
    "rst": rstHandler,
    "video": VideoHandler(),
    "split": lambda x: " {split} "
}
