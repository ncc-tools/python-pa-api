"""Tests authentication"""

from tests.test_helpers import *

def test_get_all_jobtemplates():
    api = mock_api_response(
        token='123', status=200,
        body=gen_jobtemplates_payload([
            {'sref': 'jobTemplates/1', 'name': 'test 1', 'type': 'Single'},
            {'sref': 'jobTemplates/2', 'name': 'test 2', 'type': 'Single'}
        ]))
    jobtemplates = api.get_all_jobtemplates()
    assert len(jobtemplates) == 2, "Parsed jobtemplates isn't the right size"
    assert jobtemplates[0]['name'] == 'test 1'
    assert jobtemplates[1]['name'] == 'test 2'

def test_get_testruns_for_jobtemplate():
    api = mock_api_response(
        token='123', status=200,
        body=gen_testruns_payload([
            {'url': 'http://site.com/first-testrun'},
            {'url': 'http://site.com/second-testrun'}
        ]))
    testruns = api.get_testruns_for_jobtemplate('jobTemplates/123')
    assert len(testruns) == 2, "Parsed testruns isn't the right size"
    assert testruns[0]['url'] == 'http://site.com/first-testrun'
    assert testruns[1]['url'] == 'http://site.com/second-testrun'

def test_get_pageobjects_for_testrun():
    api = mock_api_response(
        token='123', status=200,
        body=gen_pageobjects_payload([
            {'url': 'http://site.com/first-object'},
            {'url': 'http://site.com/second-object'}
        ]))
    objects = api.get_pageobjects_for_testrun('testRuns/123')
    assert len(objects) == 2, "Parsed objects isn't the right size"
    assert objects[0]['url'] == 'http://site.com/first-object'
    assert objects[1]['url'] == 'http://site.com/second-object'

def test_create_job_template():
    api = mock_api_response(
        token='123', status=200,
        body=json.dumps({ "meta": [], "results": { "jobTemplateUri": "jobTemplates/1" } }).encode()
    )
    objects = api.create_job_template({})
    assert objects['jobTemplateUri'] == 'jobTemplates/1'

def test_create_job():
    api = mock_api_response(
        token='123', status=200,
        body=json.dumps({ "meta": [], "results": { "jobUri": "jobs/1" } }).encode()
    )
    objects = api.create_job_template({})
    assert objects['jobUri'] == 'jobs/1'
