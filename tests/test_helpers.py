"""A collection of helpers to test the PA API library"""

from contextlib import contextmanager
import json
from urllib3.response import HTTPResponse

from paapi.paapi import PaApi

class MockPoolmanager:
    """
    Mocks urllib3's PoolManager
    """
    RETURN = 1
    RAISE = 2
    EVAL = 3

    _next_response = None
    _next_action = RETURN

    def __init__(self, next_response, next_action):
        self._next_response = next_response
        self._next_action = next_action

    @staticmethod
    def return_next(body=None, headers=None, status=0):
        """
        Returns the given value at the next request() call.
        """
        response = HTTPResponse(body=body, headers=headers, status=status)
        return MockPoolmanager(response, MockPoolmanager.RETURN)

    @staticmethod
    def raise_next(value):
        """
        Raises the given value at the next request() call.
        """
        return MockPoolmanager(value, MockPoolmanager.RAISE)

    @staticmethod
    def eval_next(callback):
        """
        Evaluates callback at the next request() call and returns its return value.
        """
        return MockPoolmanager(callback, MockPoolmanager.EVAL)

    def request(self, method, url, fields, headers):
        """
        Mock and HTTP request
        """
        if self._next_action == self.RETURN:
            return self._next_response
        elif self._next_action == self.RAISE:
            raise self._next_response
        elif self._next_action == self.EVAL:
            return self._next_response(method, url, fields, headers)

class MockPaAuth():
    token = None

    def __init__(self, token):
        self.token = token

    @contextmanager
    def authenticate(self):
        yield(self.token)

def mock_api_response(token='abc', realm='123', status=0, body=None, headers=None):
    auth = MockPaAuth(token)
    http = MockPoolmanager.return_next(body=body, status=status, headers=headers)
    return PaApi(auth, realm, poolmanager=http)

def _api_response_json(results):
    response = {
        'meta': {
            'paginationTotalResults': len(results),
            'response_in_sec': 0.1
        },
        'results': results
    }
    return json.dumps(response).encode()

def gen_jobtemplates_payload(data):
    results = []
    for jobtemplate_info in data:
        results.append({
            'sref': jobtemplate_info['sref'],
            'type': jobtemplate_info['type'],
            'name': jobtemplate_info['name'],
            'description': '',
            'browsers': [
                'browsers/ff'
            ],
            'urls': [
                'http://www.google.com'
            ],
            'createdBy': 'Bill Shakespeare',
            'capture': False,
            'notifyEmail': False,
            'advanced': {
                'inactivityTimeout': None
            },
            'meta': {},
            'deviceProfile': None,
            'networkSpeed': {
                'networkSpeedUri': 'networkSpeeds/1',
                'meta': {
                    'downloadKbps': 2010,
                    'uploadKbps': 190,
                    'latency': 0,
                    'packetLossRate': 0
                }
            }
        })
    return _api_response_json(results)

def gen_testruns_payload(data):
    results = []
    for datum in data:
        results.append({
            'pageTitle': 'thing',
            'url': datum['url'],
            'browserUri': 'browsers/ff',
            'dataStartDuration': 0.051,
            'renderStart': 0.696,
            'domLoad': 0.67,
            'onLoad': 2.128,
            'visuallyComplete': 6.2,
            'downloadDuration': 2.238,
            'pageSize': 388641,
            'speedIndex': 1100,
            'resultCode': 1,
            'objectCount': 18,
            'severity': 'Site OK',
            'ranAt': '2017-02-07T17:11:25+00:00',
            'sref': 'testRuns/432570',
            'jobUri': 'jobs/81637',
            'objectsUri': 'objects?testRun=testRuns%2F432570'
        })
    return _api_response_json(results)

def gen_pageobjects_payload(data):
    results = []
    for datum in data:
        results.append({
            'url': datum['url'],
            'mimeType': 'text/html',
            'result': 200,
            'requestHeaderSize': 292,
            'responseHeaderSize': 278,
            'transmittedSize': 100,
            'uncompressedSize': 100,
            'offsetDuration': 0,
            'blockDuration': None,
            'dnsDuration': 0.002,
            'connectDuration': 0.018,
            'sslDuration': 0,
            'sendDuration': None,
            'dataStartDuration': 0.032,
            'receiveTimeDuration': 0,
            'cacheDuration': None,
            'networkDuration': 0.052,
            'ttfbDuration': 0.052,
            'downloadDuration': 0.052,
            'responseBodyChecksum': 'b5560e55556db6b8e08415865116b94fcef64e2b',
            'sref': 'objects/17794272',
            'testRunUri': 'testRuns/432559'
        })
    return _api_response_json(results)
