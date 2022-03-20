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

    domain = 'tsinao.com'

    @staticmethod
    @InetDependent(-1)
    def create_presentation(name):
        return _WebService.json_post(WebInterface.domain + '/create/presentation', json.dumps({"name": name}))

    @staticmethod
    @InetDependent()
    def create_survey(survey, pid):
        json_data = json.loads(jsonpickle.encode(survey, unpicklable=False))
        json_data = json.dumps(json_data)
        remote_id = _WebService.json_post(WebInterface.domain + '/presentation/{}/create/survey'.format(pid), json_data)
        survey.remote_id = remote_id

    @staticmethod
    @InetDependent()
    def open_survey(survey):
        _WebService.get(WebInterface.domain + '/open/survey/{}'.format(survey.remote_id))

    @staticmethod
    @InetDependent("closed")
    def get_survey_status(survey):
        resp = _WebService.get(WebInterface.domain + '/survey/status/{}'.format(survey.remote_id))
        return json.loads(resp)['status']

    @staticmethod
    @InetDependent()
    def delete_presentation(pid):
        _WebService.delete(WebInterface.domain + '/delete/presentation/{}'.format(pid))

    @staticmethod
    @InetDependent()
    def _safe_remove(json_map, field):
        if field in json_map:
            json_map.pop(field)
