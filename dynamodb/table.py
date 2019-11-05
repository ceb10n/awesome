from dataclasses import dataclass, field
from typing import Any
from .models import Attribute, AttributeType, Billing, BillingType, TableInfo, SecondaryIndex, IndexStatus, EMPTY_TABLE_INFO, Throughput, TableStatus, Key, KeyType, ProjectionType, Projection
from .exceptions import NotConnectedError, TableDoesNotExistError


@dataclass
class Table:
    name: str
    connection: Any = field(init=False)
    info: TableInfo = field(init=False)

    def __post_init__(self):
        self.info = EMPTY_TABLE_INFO

    def to_schema(self) -> dict:
        schema = {
            'Table': {
                'TableName': self.name,
                **self.info.to_schema()
            }
        }

        return schema

    def connect(self, connection=None):
        if connection:
            self.connection = connection

        if self.connection:
            described_table = self.connection.describe_table(
                TableName=self.name)
            import pprint
            pprint.pprint(described_table)
            self._exists = True
            self._connected = True
            self._set_table_info(described_table['Table'])
            self._set_tags()

    def _set_table_info(self, table_info):
        self.info.status = TableStatus(table_info['TableStatus'])
        self.info.created_at = table_info['CreationDateTime']
        self.info.count = table_info['ItemCount']
        self.info.arn = table_info['TableArn']
        self.info.id = table_info['TableId']
        self.info.size_bytes = table_info['TableSizeBytes']
        self._set_attrs(table_info['AttributeDefinitions'])
        self._set_keys(table_info['KeySchema'])
        self._set_throughput(table_info['ProvisionedThroughput'])

        if 'BillingModeSummary' in table_info:
            self._set_billing(table_info['BillingModeSummary'])

        if 'GlobalSecondaryIndexes' in table_info:
            self._set_secondary_indexes(table_info['GlobalSecondaryIndexes'])

    def _set_attrs(self, attrs):
        for attr in attrs:
            self.info.add_attribute(
                Attribute(
                    attr['AttributeName'],
                    AttributeType(attr['AttributeType']),
                    None))

    def _set_keys(self, keys):
        for key in keys:
            self.info.add_key(
                Key(
                    key['AttributeName'],
                    KeyType(key['KeyType'])))

    def _set_throughput(self, throughput):
        last_increased = None
        last_decreased = None

        if 'LastIncreaseDateTime' in throughput:
            last_increased = throughput['LastIncreaseDateTime']

        if 'LastDecreaseDateTime' in throughput:
            last_decreased = throughput['LastDecreaseDateTime']

        self.info.throughput = Throughput(
            last_increased,
            last_decreased,
            throughput['NumberOfDecreasesToday'],
            throughput['ReadCapacityUnits'],
            throughput['WriteCapacityUnits'])

    def _set_billing(self, billing):
        self.info.billing = Billing(
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
                    non_keys = [attr for attr in index['Projection']['NonKeyAttributes']]
                projection = Projection(
                    ProjectionType(index['Projection']['ProjectionType']),
                    non_keys
                )

            if 'KeySchema' in index:
                keys = []
                for key in index['KeySchema']:
                    keys.append(
                        Key(
                            key['AttributeName'],
                            KeyType(key['KeyType'])))

            if 'ProvisionedThroughput' in index:

                if 'LastIncreaseDateTime' in index['ProvisionedThroughput']:
                    last_increased = index['ProvisionedThroughput']['LastIncreaseDateTime']

                if 'LastDecreaseDateTime' in index['ProvisionedThroughput']:
                    last_decreased = index['ProvisionedThroughput']['LastDecreaseDateTime']

                throughput = Throughput(
                    last_increased,
                    last_decreased,
                    index['ProvisionedThroughput']['NumberOfDecreasesToday'],
                    index['ProvisionedThroughput']['ReadCapacityUnits'],
                    index['ProvisionedThroughput']['WriteCapacityUnits'])

            self.info.add_secondary_index(
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

    def _set_tags(self):
        if not self._exists:
            raise TableDoesNotExistError(
                f'Table {self.name} does not exist yet')

        if not self._connected:
            raise NotConnectedError(
                f'Table {self.name} is not connected')

        response = self.connection.list_tags_of_resource(
            ResourceArn=self.info.arn)

        for tag in response['Tags']:
            self.info.add_tag(tag['Key'], tag['Value'])
