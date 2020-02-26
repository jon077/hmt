from meeshkan.server import make_admin_app
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from meeshkan.server.server.rest import rest_middleware_manager

import pytest
import json


@pytest.fixture
def app():
    return make_admin_app()

@pytest.fixture(autouse=True)
def setup():
    yield True
    rest_middleware_manager.clear()

@pytest.mark.gen_test
def test_admin_server_middleware(http_client, base_url):
    req = HTTPRequest(base_url+'/admin/middleware/rest/pregen')
    response = yield http_client.fetch(req)
    assert response.code == 200
    assert json.loads(response.body) == []
    req = HTTPRequest(base_url+'/admin/middleware/rest/pregen/https://foo.bar.com/api/v2', method="POST", body='')
    response = yield http_client.fetch(req)
    assert response.code == 200
    req = HTTPRequest(base_url+'/admin/middleware/rest/pregen/https://foo.bar.com/api/v2', method="POST", body='')
    response = yield http_client.fetch(req)
    assert response.code == 200
    req = HTTPRequest(base_url+'/admin/middleware/rest/pregen/111', method="POST", body='')
    response = yield http_client.fetch(req)
    assert response.code == 200
    req = HTTPRequest(base_url+'/admin/middleware/rest/pregen')
    response = yield http_client.fetch(req)
    assert response.code == 200
    assert len(json.loads(response.body)) == 2
    assert 'https://foo.bar.com/api/v2' in json.loads(response.body)
    assert '111' in json.loads(response.body)