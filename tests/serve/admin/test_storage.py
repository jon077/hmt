import pytest
from openapi_typed_2 import convert_to_OpenAPIObject
from tornado.httpclient import HTTPClientError, HTTPRequest

from hmt.serve.admin import make_admin_app
from hmt.serve.mock.scope import Scope
from hmt.serve.mock.specs import OpenAPISpecification
from tests.util import spec_dict

scope = Scope()


@pytest.fixture
def app(mock_data_store, rest_middleware_manager):
    return make_admin_app(scope, mock_data_store, rest_middleware_manager)


@pytest.fixture(autouse=True)
def setup():
    yield True
    scope.clear()


@pytest.mark.gen_test
def test_storage(mock_data_store, http_client, base_url):
    schema = {"$ref": "#/components/schemas/item"}

    components = {
        "schemas": {
            "item": {
                "type": "object",
                "required": ["foo", "baz"],
                "x-hmt-id-path": "itemId",
                "properties": {
                    "foo": {"type": "number"},
                    "bar": {"type": "string"},
                    "itemId": {"type": "string"},
                },
            }
        }
    }

    spec = spec_dict(
        path="/items/{id}", response_schema=schema, components=components, method="get"
    )
    spec["paths"]["/items/{id}"]["x-hmt-entity"] = "item"
    spec["paths"]["/items/{id}"]["get"]["x-hmt-operation"] = "read"
    spec["x-hmt-data"] = {"item": [{"foo": 10, "bar": "val", "itemId": "id123"}]}
    spec = convert_to_OpenAPIObject(spec)

    mock_data_store.add_mock(OpenAPISpecification(spec, "items"))

    req = HTTPRequest(base_url + "/admin/storage", method="DELETE")
    response = yield http_client.fetch(req)
    assert response.code == 200

    assert 0 == len(mock_data_store["items"].item)

    req = HTTPRequest(base_url + "/admin/storage/reset", method="POST", body="")
    response = yield http_client.fetch(req)
    assert response.code == 200

    assert 1 == len(mock_data_store["items"].item)

    with pytest.raises(HTTPClientError):
        req = HTTPRequest(base_url + "/admin/storage/reset", method="DELETE")
        response = yield http_client.fetch(req)

    assert 1 == len(mock_data_store["items"].item)
