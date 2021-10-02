# coding=utf-8
from naoxml.xmlexceptions import XmlTranslationException
from naoxml.xmltag import XmlTag
from naoxml.xmlfinder import XmlFinder
from survey.survey import Survey
from constants import EVENT_ARG_DELIMITER

animationNamespace = None


class DoHandler:

    def __init__(self, event_map):
        self.events = event_map

    def __call__(self, tag):
        self.attrs = tag.attributes
        if "behaviour" in self.attrs.keys():
            return self._handle_start_behavior()
        if tag.is_singular():
            return self._handle_start_tag() + self._handle_end_tag()
        return self._handle_start_tag() + tag.content + self._handle_end_tag()

    def _handle_start_behavior(self):
        return self.events['behaviour'].to_string(self.attrs["behavior"])

    def _handle_start_tag(self):
        given_path = self.attrs["animation"]
        if given_path is None:
            raise TypeError("animation path is None")
        path = given_path if animationNamespace is None else animationNamespace + given_path
        return "^start({}) ".format(path)

    def _handle_end_tag(self):
        given_path = self.attrs["animation"]
        if given_path is None:
            raise TypeError("animation path is None")
        path = given_path if animationNamespace is None else animationNamespace + given_path
        return " ^wait({}) ".format(path)


def next_handler(tag, events):
    return events['next'].to_string()


def pause_handler(tag):
    attrs = tag.attributes
    return " \\pau={}\\ ".format(attrs.get('time', 100))


def emph_handler(tag):
    attrs = tag.attributes
    if "word" not in attrs.keys():
        raise XmlTranslationException("Emph tag. Missing 'word' attribute")
    if "pos" not in attrs.keys():
        raise XmlTranslationException("Emph tag. Missing 'pos' attribute")
    return " \\emph={}\\ {} ".format(attrs["pos"], attrs["word"])


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

    def __init__(self):
        pass  # empty init

    def __call__(self, tag):
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

    def __init__(self):
        pass  # empty init

    def __call__(self, tag):
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

    def __init__(self):
        pass  # empty init

    def __call__(self, tag):
        self.attrs = tag.attributes
        if tag.is_singular():
            return self._handle_start_tag()
        return self._handle_start_tag() + tag.content + self._handle_end_tag()

    def _handle_start_tag(self):
        speed = self.attrs["speed"]
        return " \\rspd={}\\ ".format(speed)

    def _handle_end_tag(self):
        return " \\rspd=100\\ "


def rst_handler(tag):
    return " \\rst\\ "


class MediaHandler:

    def __init__(self, event_map):
        self.events = event_map

    def __call__(self, tag):
        self.attrs = tag.attributes
        if tag.is_singular():
            return self.events['startmedia'].to_string() + '<split/> '
        return self._handle_start_tag() + tag.content + self._handle_end_tag()

    def _handle_start_tag(self):
        return self.events['startmedia'].to_string()

    def _handle_end_tag(self):
        return " <split/> "


def survey_handler(tag, presentation):
    presentation.surveys[tag.attributes['id']] = Survey(tag)
    return ""


class SurveyStartHandler:

    def __init__(self, event_map):
        self.events = event_map

    def __call__(self, tag):
        self.tag = XmlTag(tag)
        self.attrs = self.tag.attributes
        if self.tag.is_singular():
            return self._handle_start_tag() + self._handle_end_tag()
        return self._handle_start_tag() + self.tag.content + self._handle_end_tag()

    def _handle_start_tag(self):
        return self.events['startsurvey'].to_string()

    def _handle_end_tag(self):
        return " <split/> "


class XmlTranslator:

    def __init__(self, presentation):
        self.xml_finder = XmlFinder()
        self.presentation = presentation
        self.xmltags = {
            "do": DoHandler(presentation.event_map),
            "next": next_handler,
            "pause": pause_handler,
            "emph": emph_handler,
            "set": set_handler,
            "rspd": RspdHandler(),
            "vol": VolHandler(),
            "rmode": RmodeHandler(),
            "rst": rst_handler,
            "video": MediaHandler(presentation.event_map),
            "audio": MediaHandler(presentation.event_map),
            "survey": lambda t: survey_handler(t, presentation),
            "startsurvey": SurveyStartHandler(presentation.event_map)
        }

    def process(self, text):
        r = XmlTag(self.get_translated_tag_as_string(XmlTag(self._xmlwrap(text))))
        if r.name == "temptag":
            return r.content
        return r.str

    def get_translated_tag_as_string(self, xmltag):
        if xmltag.is_singular():
            return self.translate_tag(xmltag.str)
        children = {t.str: t for t in xmltag.child_tags}.values()
        content = xmltag.content
        for child in children:
            content = content.replace(child.str, self.get_translated_tag_as_string(child))
        return self.translate_tag(xmltag.start_tag + content + xmltag.end_tag)

    def translate_tag(self, tag):
        tag = XmlTag(tag)
        name = tag.name
        if name not in self.xmltags.keys():
            return tag.str
        return self.xmltags[name](tag)

    @staticmethod
    def _xmlwrap(text):
        if text[0] == '<':
            return text
        return "<temptag>" + text + "</temptag>"
