from datetime import datetime
from typing import List

from .attribute import Attribute
from .attribute_definition_factory import AttributeDefinitionFactory
from .billing import Billing
from .billing_factory import BillingFactory
from .index_status import IndexStatus
from .key import Key
from .key_factory import KeyFactory
from .projection_type import ProjectionType
from .projection import Projection
from .secondary_index import SecondaryIndex
from .status import TableStatus
from .table_info import EMPTY_TABLE_INFO
from .throughput import Throughput
from .throughput_factory import ThroughputFactory


class TableInfoFactory:

    def __init__(self):
        self._described_table = {}
        self._info = None
        self._attr_factory = AttributeDefinitionFactory()
        self._throughput_factory = ThroughputFactory()
        self._key_factory = KeyFactory()
        self._billing_factory = BillingFactory()

    def create(self, described_table):
        self._described_table = described_table

        self._info = EMPTY_TABLE_INFO
        self._info.status = self._get_table_status()
        self._info.created_at = self._get_creation_time()
        self._info.count = self._get_item_count()
        self._info.arn = self._get_arn()
        self._info.id = self._get_id()
        self._info.size_bytes = self._get_size_bytes()
        self._info.attributes = self._get_attrs()
        self._info.keys = self._get_keys()
        self._info.throughput = self._get_throughput()
        self._info.billing = self._get_billing()

        if 'GlobalSecondaryIndexes' in described_table:
            self._set_secondary_indexes(
                described_table['GlobalSecondaryIndexes'])

        return self._info

    def _get_table_status(self) -> TableStatus:
        return TableStatus(
            self._described_table['TableStatus'])

    def _get_creation_time(self) -> datetime:
        return self._described_table['CreationDateTime']

    def _get_item_count(self) -> int:
        return self._described_table['ItemCount']

    def _get_arn(self) -> str:
        return self._described_table['TableArn']

    def _get_id(self) -> str:
        return self._described_table['TableId']

    def _get_size_bytes(self) -> int:
        return self._described_table['TableSizeBytes']

    def _get_attrs(self) -> List[Attribute]:
        return self._attr_factory.create(self._described_table)

    def _get_keys(self) -> List[Key]:
        return self._key_factory.create(self._described_table)

    def _get_throughput(self) -> Throughput:
        return self._throughput_factory.create(
            self._described_table)

    def _get_billing(self) -> Billing:
        return self._billing_factory.create(self._described_table)

    def _set_secondary_indexes(self, indexes):
        for index in indexes:
            projection = None
            throughput = None
            keys = None
            backfilling = None

            if 'Backfilling' in index:
                backfilling = index['Backfilling']

            if 'Projection' in index:
                non_keys = None

                if 'NonKeyAttributes' in index['Projection']:
                    p = index['Projection']
                    non_keys = [attr for attr in p['NonKeyAttributes']]

                projection = Projection(
                    ProjectionType(index['Projection']['ProjectionType']),
                    non_keys)

            if 'KeySchema' in index:
                keys = self._key_factory.create(index)

            if 'ProvisionedThroughput' in index:
                throughput = self._throughput_factory.create(index)

            self._info.add_secondary_index(
                SecondaryIndex(
                    index['IndexName'],
                    index['IndexArn'],
                    backfilling,
                    index['IndexSizeBytes'],
                    index['ItemCount'],
                    projection,
                    IndexStatus(index['IndexStatus']),
                    throughput,
                    keys))
