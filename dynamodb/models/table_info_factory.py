from .attribute_definition_factory import AttributeDefinitionFactory
from .billing_type import BillingType
from .billing import Billing
from .index_status import IndexStatus
from .key_type import KeyType
from .key import Key
from .projection_type import ProjectionType
from .projection import Projection
from .secondary_index import SecondaryIndex
from .status import TableStatus
from .table_info import EMPTY_TABLE_INFO
from .throughput import Throughput
from .throughput_factory import ThroughputFactory


class TableInfoFactory:

    def __init__(self):
        self._info = None
        self._attr_factory = AttributeDefinitionFactory()
        self._throughput_factory = ThroughputFactory()

    def create(self, described_table):
        self._info = EMPTY_TABLE_INFO
        self._info.status = TableStatus(described_table['TableStatus'])
        self._info.created_at = described_table['CreationDateTime']
        self._info.count = described_table['ItemCount']
        self._info.arn = described_table['TableArn']
        self._info.id = described_table['TableId']
        self._info.size_bytes = described_table['TableSizeBytes']
        self._info.attributes = \
            self._attr_factory.create(described_table)
        self._set_keys(described_table['KeySchema'])
        self._info.throughput = \
            self._throughput_factory.create(
                described_table['ProvisionedThroughput'])

        if 'BillingModeSummary' in described_table:
            self._set_billing(described_table['BillingModeSummary'])

        if 'GlobalSecondaryIndexes' in described_table:
            self._set_secondary_indexes(
                described_table['GlobalSecondaryIndexes'])

        return self._info

    def _set_keys(self, keys):
        for key in keys:
            self._info.add_key(
                Key(
                    key['AttributeName'],
                    KeyType(key['KeyType'])))

    def _set_billing(self, billing):
        self._info.billing = Billing(
            billing['LastUpdateToPayPerRequestDateTime'],
            BillingType(billing['BillingMode']))

    def _set_secondary_indexes(self, indexes):
        for index in indexes:
            projection = None
            throughput = None
            keys = None
            backfilling = None

            last_increased = None
            last_decreased = None

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
                keys = []
                for key in index['KeySchema']:
                    keys.append(
                        Key(
                            key['AttributeName'],
                            KeyType(key['KeyType'])))

            if 'ProvisionedThroughput' in index:

                if 'LastIncreaseDateTime' in index['ProvisionedThroughput']:
                    last_increased = \
                        index['ProvisionedThroughput']['LastIncreaseDateTime']

                if 'LastDecreaseDateTime' in index['ProvisionedThroughput']:
                    last_decreased = \
                        index['ProvisionedThroughput']['LastDecreaseDateTime']

                throughput = Throughput(
                    last_increased,
                    last_decreased,
                    index['ProvisionedThroughput']['NumberOfDecreasesToday'],
                    index['ProvisionedThroughput']['ReadCapacityUnits'],
                    index['ProvisionedThroughput']['WriteCapacityUnits'])

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
