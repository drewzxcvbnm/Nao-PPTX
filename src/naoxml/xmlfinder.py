from xmlexceptions import XmlTranslationException
from xmltag import XmlTag


def catchError(message, arg):
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

    def findXmlTag(self, text):
        self.text = text
        while self.text.find('<') != -1:
            tagFinder = self._getTagFinder(self.text)
            l1, r1, stag = next(tagFinder)
            if self._isSingular(stag):
                return l1, r1, stag
            l2, r2, etag = self._getEndTag(stag, tagFinder)
            tag = self.text[l1:r2 + 1]
            return l1, r2, tag

    @catchError("Error finding end tag for:", 1)
    def _getEndTag(self, stag, tagFinder):
        stagName = XmlTag(stag).tag_name
        numToFind = 1
        l, r, tag = None, None, None
        while numToFind > 0:
            l, r, tag = next(tagFinder)
            if self._isValidEndTag(stag, tag):
                numToFind -= 1
            elif XmlTag(tag).tag_name == stagName and not self._isSingular(tag):
                numToFind += 1
        return l, r, tag

    def _getTagFinder(self, text):
        texti = 0
        while text.find('<') != -1:
            l, r, t = self._findTag(text)
            text = text[r + 1:]
            yield l + texti, r + texti, t
            texti += r + 1

    def _replace(self, lbound, rbound, replacement):
        self.text = self.text[:lbound] + replacement + self.text[rbound + 1:]

    def _findTag(self, text):
        lbound = text.find('<')
        rbound = text.find('>')
        tag = text[lbound:rbound + 1]
        if tag.count('<') > 1:
            raise XmlTranslationException("Tag '{}' contains '<' within itself.".format(tag))
        return (lbound, rbound, tag)

    def _isSingular(self, tag):
        return tag[-2] == '/'

    def _isValidEndTag(self, startTag, endTag):
        startName = XmlTag(startTag).tag_name
        endName = XmlTag(endTag).tag_name
        return startName == endName and endTag[1] == '/'
