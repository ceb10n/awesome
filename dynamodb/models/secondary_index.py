from dataclasses import dataclass
from typing import List

from .index_status import IndexStatus
from .key import Key
from .projection import Projection
from .throughput import Throughput


@dataclass
class SecondaryIndex:
    name: str
    arn: str
    backfilling: bool
    size_bytes: int
    count: int
    projection: Projection
    index_status: IndexStatus
    throughput: Throughput
    keys: List[Key]

    def to_schema(self):
        schema = {
            'IndexName': self.name,
            'IndexStatus': self.index_status.value,
            'IndexSizeBytes': self.size_bytes,
            'ItemCount': self.count,
            'IndexArn': self.arn
        }

        if self.backfilling:
            schema['Backfilling'] = self.backfilling

        if self.projection:
            schema['Projection'] = self.projection.to_schema()

        if self.throughput:
            schema['ProvisionedThroughput'] = self.throughput.to_schema()

        if self.keys and len(self.keys) > 0:
            schema['KeySchema'] = []
            for key in self.keys:
                schema['KeySchema'].append(key.to_schema())

        return schema
