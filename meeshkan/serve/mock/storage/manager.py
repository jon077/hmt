import logging


from meeshkan.serve.mock.storage.entity import Entity
from meeshkan.serve.mock.storage.mock_data import MockData
from meeshkan.serve.utils.opanapi_utils import get_x
from openapi_typed_2 import OpenAPIObject

logger = logging.getLogger(__name__)


class StorageManager:
    def __init__(self):
        self._storages = dict()

    def add_mock(self, mockname: str, spec: OpenAPIObject):
        storage = MockData()
        self._storages[mockname] = storage
        if spec.components is not None and spec.components.schemas is not None:
            for name, schema in spec.components.schemas.items():
                if get_x(schema, "x-meeshkan-id-path") is not None:
                    storage.add_entity(Entity(name, schema))

        for entity, values in get_x(spec, "x-meeshkan-data", dict()).items():
            for val in values:
                storage.get_entity(entity).insert(entity, val)

    def __getitem__(self, mockname):
        return self._storages[mockname]

    def clear(self):
        for storage in self._storages.values():
            storage.clear()
        logger.debug("All storages cleared")


storage_manager = StorageManager()