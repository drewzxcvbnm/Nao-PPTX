
xmltags = {
    "do" : DoHandler(),
    "do" : DoHandler(),
}

class XmlParsingException(Exception):
    pass


class XmlTranslator:

    def translateTag(self, tag):
        name = self._getTagName(tag)
        if name not in xmltags.keys():
            raise XmlParsingException("Cannot translate tag {}:{}".format(name, tag))
        


    def _getTagName(self, tag):
        return tag[1:max(tag.find(' '),tag.find('>')]

class DoHandler:

    def __call__(self, tag):
        pass

def nextHandler(tag):
    return "$event=next"
    
