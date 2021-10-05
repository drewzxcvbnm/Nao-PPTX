from naoxml.xmlexceptions import XmlValidationException
from general import flatlist


class XmlTagValidator:

    def __init__(self):
        pass   # empty init

    @classmethod
    def validate(cls, xmltag, mandatory_fields):
        for field in mandatory_fields:
            cls._validate_field(xmltag, field)

    @classmethod
    def _validate_field(cls, xmltag, field):
        field_path = field.split('.')
        tag = [xmltag]
        for f in field_path:
            ch = flatlist(cls._get_children_from_tag(tag, f))
            if any(elem is None for elem in ch):
                raise XmlValidationException('[{}]: Tag {} is missing field'.format(field, tag[0].name))
            tag = ch

    @classmethod
    def _get_children_from_tag(cls, tag, field):
        if isinstance(tag, list):
            return [cls._get_children_from_tag(t, field) for t in tag]
        return [tag.get_child_tag(field)]
