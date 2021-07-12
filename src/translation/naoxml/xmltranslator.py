from xmlparsingexception import XmlParsingException
from xmltag import XmlTag

xmltags = {}


def StrToXmlTag(function):
    def wrapper(tagAsStr):
        tag = XmlTag(tagAsStr)
        function(tag)

    return wrapper


class XmlTagService:

    def translateTag(self, fulltag):
        name = self.getTagName(fulltag)
        if name not in xmltags.keys():
            raise XmlParsingException("Cannot translate tag {}:{}".format(name, fulltag))
        return xmltags[name](fulltag)


class DoHandler:

    @StrToXmlTag
    def __call__(self, tag):
        self.attrs = tag.getAttributes()
        if tag.str.count('<') == 1:
            return self._handleStartTag()
        return self._handleStartTag() + tag.getTagContent() + self._handleEndTag()

    def _handleStartTag(self):
        return "^start({}) ".format(self.attrs["animation"])

    def _handleEndTag(self):
        return " ^wait({}) ".format(self.attrs["animation"])


def nextHandler(tag):
    return " $event=next "


@StrToXmlTag
def pauseHandler(tag):
    attrs = tag.getAttributes()
    return " \\pau={}\\ ".format(attrs.get('time', 100))


xmltags = {
    "do": DoHandler(),
    "next": nextHandler,
    "pause": pauseHandler,
}
