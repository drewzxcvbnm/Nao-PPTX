from xmlexceptions import XmlTranslationException
from xmltag import XmlTag
from survey.survey import Survey, surveys

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
        name = tag.tag_name
        if name not in xmltags.keys():
            return tag.str
        return xmltags[name](tag.str)


class DoHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.attributes
        if tag.is_singular() == 1:
            return self._handleStartTag() + self._handleEndTag()
        return self._handleStartTag() + tag.content + self._handleEndTag()

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
    attrs = tag.attributes
    return " \\pau={}\\ ".format(attrs.get('time', 100))


@StrToXmlTag
def emphHandler(tag):
    attrs = tag.attributes
    if "word" not in attrs.keys():
        raise XmlTranslationException("Emph tag. Missing 'word' attribute")
    if "pos" not in attrs.keys():
        raise XmlTranslationException("Emph tag. Missing 'pos' attribute")
    return " \\emph={}\\ {} ".format(attrs["pos"], attrs["word"])


@StrToXmlTag
def setHandler(tag):
    attrs = tag.attributes
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
        self.attrs = tag.attributes
        if tag.is_singular():
            return self._handleStartTag()
        return self._handleStartTag() + tag.content + self._handleEndTag()

    def _handleStartTag(self):
        mode = self.attrs["mode"]
        return " \\readmode={}\\ ".format(mode)

    def _handleEndTag(self):
        return " \\readmode=sent\\ "


class VolHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.attributes
        if tag.is_singular():
            return self._handleStartTag()
        return self._handleStartTag() + tag.content + self._handleEndTag()

    def _handleStartTag(self):
        value = self.attrs["value"]
        return " \\vol={}\\ ".format(value)

    def _handleEndTag(self):
        return " \\vol=100\\ "


class RspdHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.attributes
        if tag.is_singular():
            return self._handleStartTag()
        return self._handleStartTag() + tag.content + self._handleEndTag()

    def _handleStartTag(self):
        speed = self.attrs["speed"]
        return " \\rspd={}\\ ".format(speed)

    def _handleEndTag(self):
        return " \\rspd=100\\ "


@StrToXmlTag
def rstHandler(tag):
    return " \\rst\\ "


class MediaHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.attributes
        if tag.is_singular():
            return " $event=startmedia <split/> "
        return self._handleStartTag() + tag.content + self._handleEndTag()

    def _handleStartTag(self):
        return " $event=startmedia "

    def _handleEndTag(self):
        return " <split/> "


@StrToXmlTag
def survey_handler(tag):
    surveys[tag.attributes['id']] = Survey(tag)
    return ""


class SurveyStartHandler:

    def __call__(self, tag):
        self.tag = XmlTag(tag)
        self.attrs = self.tag.attributes
        if self.tag.is_singular():
            return self._handle_start_tag() + self._handle_end_tag()
        return self._handle_start_tag() + self.tag.content + self._handle_end_tag()

    def _handle_start_tag(self):
        return " $event=startsurvey_{} ".format(self.tag.attributes['id'])

    def _handle_end_tag(self):
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
    "video": MediaHandler(),
    "audio": MediaHandler(),
    "survey": survey_handler,
    "startsurvey": SurveyStartHandler()
}
