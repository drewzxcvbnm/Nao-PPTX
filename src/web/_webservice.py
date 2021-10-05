import re
import httplib
from constants import DOMAIN_REGEX


class _WebService:

    def __init__(self):
        pass  # empty init

    @staticmethod
    def json_post(url, data):
        domain = re.findall(DOMAIN_REGEX, url)[0]
        hdr = {"content-type": "application/json"}
        conn = httplib.HTTPSConnection(domain)
        conn.request('POST', url.replace(domain, ""), data, hdr)
        response = conn.getresponse()
        return response.read()

    @staticmethod
    def get(url):
        domain = re.findall(".*?(?=/)", url)[0]
        conn = httplib.HTTPSConnection(domain)
        conn.request('GET', url.replace(domain, ""))
        response = conn.getresponse()
        return response.read()

    @staticmethod
    def delete(url):
        domain = re.findall(".*?(?=/)", url)[0]
        conn = httplib.HTTPSConnection(domain)
        conn.request('DELETE', url.replace(domain, ""))
        response = conn.getresponse()
        return response.read()
