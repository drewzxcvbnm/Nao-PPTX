from xml.xmltags import XmlTranslator, XmlParsingException


class XmlParser:

    def __init__(self):
        self.xmlTranslator = XmlTranslator()

    def parse(self, text):
        self.text = text
        while self.text.find('<') != -1:
            start_lbound, start_rbound, startTag = self._findTag(self.text)
            if self._isSingular(startTag):
                r = self.xmlTranslator.translate(startTag)
                self._replace(start_lbound, start_rbound, r)
                continue
            end_lbound, end_rbound, endTag = self._findTag(self.text[start_rbound+1:])
            if endTag == '':
                raise XmlParsingException("Missing closing tag for {}".format(startTag))
            if endTag[1] != '/':
                raise XmlParsingException("Closing tag {} does not contain '/'".format(endTag))
            r = self.xmlTranslator.translate(self.text[start_lbound:end_rbound+1])
            self._replace(start_lbound, end_rbound, r)



    def _findTag(self, text):
        lbound = text.find('<')
        rbound = text.find('>')
        tag = self.text[lbound:rbound+1]
        if tag.count('<') > 1:
            raise ParserException("Tag '{}' contains '<' withing itself.".format(startTag))
        return (lbound, rbound, tag)

    def _replace(self, lbound, rbound, replacement):
        self.text = self.text[:lbound] + replacement + self.text[rbound+1:]
            

    def _isSingular(self, tag):
        return tag[-2] == '/'


class SlideTranslationSystem:

    parsers = [XmlParser()]

    @staticmethod
    def translate(slideText):
        for parser in SlideTranslationSystem.parsers:
            slideText = parser.parse(slideText)
        return slideText 

