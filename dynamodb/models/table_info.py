from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, NoReturn

from .attribute import Attribute
from .billing import Billing
from .key import Key
from .secondary_index import SecondaryIndex
from .status import TableStatus
from .throughput import Throughput


@dataclass
class TableInfo:
    __slots__ = [
        'id',
        'arn',
        'count',
        'size_bytes',
        'tags',
        'created_at',
        'status',
        'throughput',
        'billing',
        'keys',
        'attributes',
        'secondary_indexes']

    id: str
    arn: str
    count: int
    size_bytes: int
    tags: dict
    created_at: datetime
    status: TableStatus
    throughput: Throughput
    billing: Billing
    keys: List[Key]
    attributes: List[Attribute]
    secondary_indexes: List[SecondaryIndex]

    def add_attribute(self, attribute: Attribute) -> NoReturn:
        if not self.attributes:
            self.attributes = []

        self.attributes.append(attribute)

    def add_key(self, key: Attribute) -> NoReturn:
        if not self.keys:
            self.keys = []

        self.keys.append(key)

    def add_tag(self, key: Any, val: Any) -> NoReturn:
        if not self.tags:
            self.tags = dict()

        self.tags[key] = val

    def add_secondary_index(self, index: SecondaryIndex) -> NoReturn:
        if not self.secondary_indexes:
            self.secondary_indexes = []

        self.secondary_indexes.append(index)

    def to_schema(self) -> dict:
        schema = {
            'TableStatus': self.status.value,
            'CreationDateTime': self.created_at,
            'TableSizeBytes': self.size_bytes,
            'ItemCount': self.count,
            'TableArn': self.arn,
            'TableId': self.id,
        }

        if self.attributes and len(self.attributes) > 0:
            schema['AttributeDefinitions'] = []
            for attr in self.attributes:
                schema['AttributeDefinitions'].append(attr.to_schema())

        if self.keys and len(self.keys) > 0:
            schema['KeySchema'] = []
            for key in self.keys:
                schema['KeySchema'].append(key.to_schema())

        if self.throughput:
            schema['ProvisionedThroughput'] = self.throughput.to_schema()

        if self.billing:
            schema['BillingModeSummary'] = self.billing.to_schema()

        if self.secondary_indexes and len(self.secondary_indexes) > 0:
            schema['GlobalSecondaryIndexes'] = []
            for index in self.secondary_indexes:
                schema['GlobalSecondaryIndexes'].append(index.to_schema())

        return schema


EMPTY_TABLE_INFO = TableInfo(None, None, None, None, None, None, None, None, None, None, None, None) # noqa
