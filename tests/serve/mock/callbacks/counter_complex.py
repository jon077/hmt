from hmt.serve.mock.callbacks import callback


@callback("api.com", "post", "/counter")
def counter_callback_post(request_body, response_body, storage):
    if "set" in request_body:
        storage["called"] = request_body["set"]
    else:
        storage["called"] = storage.get("called", 0) + 1
    response_body["count"] = storage["called"]
    return response_body


@callback("api.com", "get", "/text_counter", format="text")
def counter_callback_get(query, response_body, storage, response_headers):
    if "set" in query:
        storage.default["called"] = query["set"]
    else:
        storage.default["called"] = storage.default.get("called", 0) + 1
    response_headers["x-hmt-counter"] = storage.default["called"]
    return "{} {} times".format(response_body, storage.default["called"])


@callback("petstore.swagger.io", "post", "/v1/pets", format="text")
def echo_callback(request_body):
    return request_body
