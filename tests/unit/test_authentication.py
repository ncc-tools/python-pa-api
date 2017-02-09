"""Tests authentication"""

import pytest
import time
from urllib3.response import HTTPResponse

from paapi.paapi import PaAuth, AuthenticationError
from tests.test_helpers import MockPoolmanager

def test_can_authenticate():
    http = MockPoolmanager.return_next(
        status=200,
        body=b'{"access_token":"123456ffceedd","token_type":"Bearer","expires_in":43200}')
    auth = PaAuth('foo', 'bar', poolmanager=http)
    with auth.authenticate() as token:
        assert token == "123456ffceedd", "token wasn't read from response"

def test_failing_authentication_raises_error():
    http = MockPoolmanager.return_next(
        status=403,
        body=b'{"error":"access_denied","error_description":"Invalid username or password"}')
    auth = PaAuth('foo', 'bar', poolmanager=http)
    with pytest.raises(AuthenticationError):
        with auth.authenticate():
            pass

def test_broken_authentication_service_raises_exception():
    http = MockPoolmanager.return_next(status=500, body=b'Server dead')
    auth = PaAuth('foo', 'bar', poolmanager=http)
    with pytest.raises(Exception):
        with auth.authenticate():
            pass

def test_doesnt_reauthenticate_when_token_valid():
    token = '1'
    http = MockPoolmanager.eval_next(
        lambda method, url, fields, headers: HTTPResponse(
            status=200,
            body=('{"access_token":"%s","token_type":"Bearer","expires_in":43200}' % (token,)).encode()))
    auth = PaAuth('foo', 'bar', poolmanager=http)
    with auth.authenticate() as read_token:
        assert read_token == '1'
    token = '2'
    with auth.authenticate() as read_token:
        assert read_token == '1', "Non-expired token was renewed when it didn't need to"

def test_reauthenticates_when_token_times_out():
    token = '1'
    http = MockPoolmanager.eval_next(
        lambda method, url, fields, headers: HTTPResponse(
            status=200,
            body=('{"access_token":"%s","token_type":"Bearer","expires_in":1}' % (token,)).encode()))
    auth = PaAuth('foo', 'bar', poolmanager=http)
    with auth.authenticate() as read_token:
        assert read_token == '1'
    time.sleep(2)
    token = '2'
    with auth.authenticate() as read_token:
        assert read_token == '2', "Expired token was not renewed"
