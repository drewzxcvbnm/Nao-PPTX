from xmlexceptions import XmlTranslationException
from xmltag import XmlTag
from survey.survey import Survey, surveys

animationNamespace = None


def str_to_xml_tag(function):
    def wrapper(tag_as_str):
        tag = XmlTag(tag_as_str)
        return function(tag)

    return wrapper


class XmlTagService:

    def translate_tag(self, tag):
        tag = XmlTag(tag)
        name = tag.name
        if name not in xmltags.keys():
            return tag.str
        return xmltags[name](tag.str)


class DoHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.attributes
        if tag.is_singular() == 1:
            return self._handle_start_tag() + self._handle_end_tag()
        return self._handle_start_tag() + tag.content + self._handle_end_tag()

    def _handle_start_tag(self):
        given_path = self.attrs["animation"]
        path = given_path if animationNamespace is None else animationNamespace + given_path
        return "^start({}) ".format(path)

    def _handle_end_tag(self):
        given_path = self.attrs["animation"]
        path = given_path if animationNamespace is None else animationNamespace + given_path
        return " ^wait({}) ".format(path)


def next_handler(tag):
    return " $event=next "


@str_to_xml_tag
def pause_handler(tag):
    attrs = tag.attributes
    return " \\pau={}\\ ".format(attrs.get('time', 100))


@str_to_xml_tag
def emph_handler(tag):
    attrs = tag.attributes
    if "word" not in attrs.keys():
        raise XmlTranslationException("Emph tag. Missing 'word' attribute")
    if "pos" not in attrs.keys():
        raise XmlTranslationException("Emph tag. Missing 'pos' attribute")
    return " \\emph={}\\ {} ".format(attrs["pos"], attrs["word"])


@str_to_xml_tag
def set_handler(tag):
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
            return self._handle_start_tag()
        return self._handle_start_tag() + tag.content + self._handle_end_tag()

    def _handle_start_tag(self):
        mode = self.attrs["mode"]
        return " \\readmode={}\\ ".format(mode)

    def _handle_end_tag(self):
        return " \\readmode=sent\\ "


class VolHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.attributes
        if tag.is_singular():
            return self._handle_start_tag()
        return self._handle_start_tag() + tag.content + self._handle_end_tag()

    def _handle_start_tag(self):
        value = self.attrs["value"]
        return " \\vol={}\\ ".format(value)

    def _handle_end_tag(self):
        return " \\vol=100\\ "


class RspdHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.attributes
        if tag.is_singular():
            return self._handle_start_tag()
        return self._handle_start_tag() + tag.content + self._handle_end_tag()

    def _handle_start_tag(self):
        speed = self.attrs["speed"]
        return " \\rspd={}\\ ".format(speed)

    def _handle_end_tag(self):
        return " \\rspd=100\\ "


@str_to_xml_tag
def rst_handler(tag):
    return " \\rst\\ "


class MediaHandler:

    def __call__(self, tag):
        tag = XmlTag(tag)
        self.attrs = tag.attributes
        if tag.is_singular():
            return " $event=startmedia <split/> "
        return self._handle_start_tag() + tag.content + self._handle_end_tag()

    def _handle_start_tag(self):
        return " $event=startmedia "

    def _handle_end_tag(self):
        return " <split/> "


@str_to_xml_tag
def survey_handler(tag):
    surveys[tag.attributes['id']] = Survey(tag)
    return ""


class SurveyStartHandler:

    def __init__(self):
        pass

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
    "next": next_handler,
    "pause": pause_handler,
    "emph": emph_handler,
    "set": set_handler,
    "rspd": RspdHandler(),
    "vol": VolHandler(),
    "rmode": RmodeHandler(),
    "rst": rst_handler,
    "video": MediaHandler(),
    "audio": MediaHandler(),
    "survey": survey_handler,
    "startsurvey": SurveyStartHandler()
}
