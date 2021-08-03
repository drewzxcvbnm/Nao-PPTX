# coding=utf-8
import re

from xmlexceptions import XmlTranslationException


def cached_children(f):
    def wrapper(*args):
        self = args[0]
        if self.children is None:
            return f(*args)
        return self.children

    return wrapper


class XmlTag:

    def __init__(self, tag_as_str):
        self.tag = tag_as_str
        self.str = tag_as_str
        self.children = None

    @property
    def tag_name(self):
        tag = self.start_tag
        if ' ' in tag:
            return tag[1: tag.find(' ')]
        return re.sub("(<|>|/)", "", tag)

    def is_singular(self):
        return self.tag.count('<') == 1

    def is_closed(self):
        return self.tag[-2] == '/'

    @property
    def attributes(self):
        start_tag = self.start_tag
        attrs = {}
        name = self.tag_name
        tag = re.sub("(<|>|{})".format(name), "", start_tag).strip("/").strip(" ")
        if tag == "":
            return attrs
        for attr in tag.split(' '):
            k, v = attr.split('=')
            start_search = v.find('"') + 1
            attrs[k] = v[start_search: v[start_search:].find('"') + 1]
        return attrs

    @property
    def start_tag(self):
        fulltag = self.tag
        lbound = fulltag.find('<')
        rbound = fulltag.find('>')
        tag = fulltag[lbound:rbound + 1]
        return tag

    @property
    def end_tag(self):
        fulltag = self.tag
        if fulltag.count('<') < 2:
            raise XmlTranslationException("Cannot extract end from:{}".format(fulltag))
        lbound = fulltag.rfind('<')
        rbound = fulltag.rfind('>')
        tag = fulltag[lbound:rbound + 1]
        return tag

    @property
    def content(self):
        fulltag = self.tag
        if fulltag.count('<') < 2:
            raise XmlTranslationException("Cannot extract content from:{}".format(fulltag))
        srbound = fulltag.find('>')
        elbound = fulltag.rfind('<')
        return fulltag[srbound + 1:elbound]

    @property
    @cached_children
    def child_tags(self):
        from xmlfinder import XmlFinder
        xml_finder = XmlFinder()
        tags = []
        content = self.content
        while content.find('<') != -1:
            l, r, t = xml_finder.find_xml_tag(content)
            tags.append(XmlTag(t))
            content = content[r + 1:]
        return tags

    def get_child_tag(self, name):
        ch = self.child_tags
        res = [i for i in ch if i.tag_name == name]
        if len(res) == 0:
            return None
        elif len(res) == 1:
            return res[0]
        return res

    def get_child_tag_content(self, name):
        ch = self.get_child_tag(name)
        if ch is None:
            return None
        return ch.content

    def get_translated_tag_as_string(self):
        from xmltranslator import XmlTagService
        xml_tag_service = XmlTagService()
        if self.is_singular():
            return xml_tag_service.translate_tag(self.str)
        children = {t.str: t for t in self.child_tags}.values()
        content = self.content
        for child in children:
            content = content.replace(child.str, child.get_translated_tag_as_string())
        return xml_tag_service.translate_tag(self.start_tag + content + self.end_tag)

    def __repr__(self):
        if self.is_singular():
            return "'{}'".format(self.start_tag)
        content = self.content
        text = "..." if len(content) > 5 else content
        return "'{}{}{}'".format(self.start_tag, text, self.end_tag)
