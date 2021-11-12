import jsonpickle

from _webservice import _WebService
from args import ARGS
import json


class InetDependent:

    def __init__(self, return_value=None):
        self.return_value = return_value

    def __call__(self, func):
        def decorator(*args, **kwargs):
            if ARGS.no_inet:
                return self.return_value
            return func(*args, **kwargs)

        return decorator


class WebInterface:
    def __init__(self):
        pass  # empty init

    domain = 'www.tsinao.com'

    @classmethod
    @InetDependent(-1)
    def create_presentation(cls, name):
        return _WebService.json_post(cls.domain + '/create/presentation', json.dumps({"name": name}))

    @classmethod
    @InetDependent
    def create_survey(cls, survey, pid):
        json_data = json.loads(jsonpickle.encode(survey, unpicklable=False))
        json_data = json.dumps(json_data)
        remote_id = _WebService.json_post(cls.domain + '/presentation/{}/create/survey'.format(pid), json_data)
        survey.remote_id = remote_id

    @classmethod
    @InetDependent
    def open_survey(cls, survey):
        _WebService.get(cls.domain + '/open/survey/{}'.format(survey.remote_id))

    @classmethod
    @InetDependent("closed")
    def get_survey_status(cls, survey):
        resp = _WebService.get(cls.domain + '/survey/status/{}'.format(survey.remote_id))
        return json.loads(resp)['status']

    @classmethod
    @InetDependent
    def delete_presentation(cls, pid):
        _WebService.delete(cls.domain + '/delete/presentation/{}'.format(pid))

    @staticmethod
    @InetDependent
    def _safe_remove(json_map, field):
        if field in json_map:
            json_map.pop(field)
