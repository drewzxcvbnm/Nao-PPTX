import re
from xmltranslationexception import XmlTranslationException


class XmlTag:

    def __init__(self, tagAsStr):
        self.tag = tagAsStr
        self.str = tagAsStr

    def getTagName(self):
        tag = self.tag
        if ' ' in tag:
            return tag[1: tag.find(' ')]
        return re.sub("(<|>|/)", "", tag)

    def isSingular(self):
        return self.tag.count('<') == 1

    def isClosed(self):
        return self.tag[-2] == '/'

    def getAttributes(self):
        startTag = self.getStartTag()
        attrs = {}
        name = self.getTagName()
        tag = re.sub("(<|>|{})".format(name), "", startTag).strip("/").strip(" ")
        if tag == "":
            return attrs
        for attr in tag.split(' '):
            k, v = attr.split('=')
            start_search = v.find('"') + 1
            attrs[k] = v[start_search: v[start_search:].find('"') + 1]
        return attrs

    def getStartTag(self):
        fulltag = self.tag
        lbound = fulltag.find('<')
        rbound = fulltag.find('>')
        tag = fulltag[lbound:rbound + 1]
        return tag

    def getEndTag(self):
        fulltag = self.tag
        if fulltag.count('<') < 2:
            raise XmlTranslationException("Cannot extract end from:{}".format(fulltag))
        lbound = fulltag.rfind('<')
        rbound = fulltag.rfind('>')
        tag = fulltag[lbound:rbound + 1]
        return tag

    def getTagContent(self):
        fulltag = self.tag
        if fulltag.count('<') < 2:
            raise XmlTranslationException("Cannot extract content from:{}".format(fulltag))
        srbound = fulltag.find('>')
        elbound = fulltag.rfind('<')
        return fulltag[srbound + 1:elbound]

    def getChildrenTags(self):
        from xmlfinder import XmlFinder
        xmlFinder = XmlFinder()
        tags = []
        content = self.getTagContent()
        while content.find('<') != -1:
            l, r, t = xmlFinder.findXmlTag(content)
            tags.append(XmlTag(t))
            content = content[r + 1:]
        return tags

    def __repr__(self):
        if self.isSingular():
            return "'{}'".format(self.getStartTag())
        content = self.getTagContent()
        text = "..." if len(content) > 5 else content
        return "'{}{}{}'".format(self.getStartTag(), text, self.getEndTag())
