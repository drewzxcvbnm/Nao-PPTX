from webservice import WebService
import json


class WebInterface:
    domain = 'www.tsinao.com'

    @classmethod
    def create_presentation(cls, name):
        return WebService.json_post(cls.domain + '/create/presentation', json.dumps({"name": name}))
