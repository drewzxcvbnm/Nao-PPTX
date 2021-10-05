class XmlTranslationException(Exception):
    pass


class XmlValidationException(Exception):

    def __init__(self, msg):
        self.message = msg
