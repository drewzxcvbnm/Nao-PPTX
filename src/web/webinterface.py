import jsonpickle

from _webservice import _WebService
import json


class WebInterface:
    def __init__(self):
        pass  # empty init

    domain = 'www.tsinao.com'

    @classmethod
    def create_presentation(cls, name):
        return _WebService.json_post(cls.domain + '/create/presentation', json.dumps({"name": name}))

    @classmethod
    def create_survey(cls, survey, pid):
        json_data = json.loads(jsonpickle.encode(survey, unpicklable=False))
        json_data = json.dumps(json_data)
        remote_id = _WebService.json_post(cls.domain + '/presentation/{}/create/survey'.format(pid), json_data)
        survey.remote_id = remote_id

    @classmethod
    def open_survey(cls, survey):
        _WebService.get(cls.domain + '/open/survey/{}'.format(survey.remote_id))

    @classmethod
    def get_survey_status(cls, survey):
        resp = _WebService.get(cls.domain + '/survey/status/{}'.format(survey.remote_id))
        return json.loads(resp)['status']

    @staticmethod
    def _safe_remove(json_map, field):
        if field in json_map:
            json_map.pop(field)
