import logging

from tornado.httpserver import HTTPServer
from tornado.web import Application

from meeshkan.serve.admin.views import (
    RestMiddlewaresView,
    RestMiddlewareView,
    ScopeView,
    StorageView,
)
from meeshkan.serve.mock.rest import RestMiddlewareManager
from meeshkan.serve.mock.storage.manager import StorageManager

from ..mock.scope import Scope

logger = logging.getLogger(__name__)


def make_admin_app(
    scope: Scope,
    storage_manager: StorageManager,
    rest_middleware_manager: RestMiddlewareManager,
):
    storage_view_deps = dict(storage_manager=storage_manager)
    rest_middleware_deps = dict(rest_middleware_manager=rest_middleware_manager)
    scope_view_deps = dict(scope=scope)
    return Application(
        [
            (r"/admin/scope", ScopeView, scope_view_deps),
            (r"/admin/storage", StorageView, storage_view_deps),
            (
                r"/admin/middleware/rest/pregen",
                RestMiddlewaresView,
                rest_middleware_deps,
            ),
            (
                r"/admin/middleware/rest/pregen/(.+)",
                RestMiddlewareView,
                rest_middleware_deps,
            ),
        ]
    )


def start_admin(
    port: int,
    scope: Scope,
    storage_manager: StorageManager,
    rest_middleware_manager: RestMiddlewareManager,
):
    app = make_admin_app(scope, storage_manager, rest_middleware_manager)
    http_server = HTTPServer(app)
    http_server.listen(port)
    logger.info("- Admin   http://localhost:%s/admin", port)
