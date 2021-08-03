from xmlexceptions import XmlTranslationException
from xmltag import XmlTag


def catch_error(message, arg):
    def decorator(function):
        def inner(*args, **kwargs):
            a = None
            if isinstance(arg, int):
                a = args[arg]
            else:
                a = kwargs[arg]
            try:
                r = function(*args, **kwargs)
            except Exception as e:
                raise XmlTranslationException(message + str(a))
            return r

        return inner

    return decorator


class XmlFinder:

    def __init__(self):
        pass

    def find_xml_tag(self, text):
        self.text = text
        while self.text.find('<') != -1:
            tag_finder = self._get_tag_finder(self.text)
            l1, r1, stag = next(tag_finder)
            if self._is_singular(stag):
                return l1, r1, stag
            l2, r2, etag = self._get_end_tag(stag, tag_finder)
            tag = self.text[l1:r2 + 1]
            return l1, r2, tag

    @catch_error("Error finding end tag for:", 1)
    def _get_end_tag(self, stag, tag_finder):
        stag_name = XmlTag(stag).tag_name
        num_to_find = 1
        l, r, tag = None, None, None
        while num_to_find > 0:
            l, r, tag = next(tag_finder)
            if self._is_valid_end_tag(stag, tag):
                num_to_find -= 1
            elif XmlTag(tag).tag_name == stag_name and not self._is_singular(tag):
                num_to_find += 1
        return l, r, tag

    def _get_tag_finder(self, text):
        texti = 0
        while text.find('<') != -1:
            l, r, t = self._find_tag(text)
            text = text[r + 1:]
            yield l + texti, r + texti, t
            texti += r + 1

    def _replace(self, lbound, rbound, replacement):
        self.text = self.text[:lbound] + replacement + self.text[rbound + 1:]

    def _find_tag(self, text):
        lbound = text.find('<')
        rbound = text.find('>')
        tag = text[lbound:rbound + 1]
        if tag.count('<') > 1:
            raise XmlTranslationException("Tag '{}' contains '<' within itself.".format(tag))
        return (lbound, rbound, tag)

    def _is_singular(self, tag):
        return tag[-2] == '/'

    def _is_valid_end_tag(self, start_tag, end_tag):
        start_name = XmlTag(start_tag).tag_name
        end_name = XmlTag(end_tag).tag_name
        return start_name == end_name and end_tag[1] == '/'
