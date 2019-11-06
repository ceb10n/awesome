from dataclasses import dataclass, field
from typing import Any

from .models import EMPTY_TABLE_INFO, TableInfo, TableInfoFactory
from .exceptions import NotConnectedError, TableDoesNotExistError


@dataclass
class Table:
    name: str
    connection: Any = field(init=False)
    info: TableInfo = field(init=False)
    _described_table: dict = field(init=False)

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
            self._described_table = self.connection.describe_table(
                TableName=self.name)
            self._exists = True
            self._connected = True
            self.info = TableInfoFactory().create(self._described_table['Table'])
            self._set_tags()

    def dump(self):
        if not self._exists:
            raise TableDoesNotExistError(
                f'Table {self.name} does not exist yet')

        if not self._connected:
            raise NotConnectedError(
                f'Table {self.name} is not connected')

        response = self.connection.scan(
            TableName=self.name,
            Select='ALL_ATTRIBUTES')
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = self.connection.scan(
                TableName=self.name,
                Select='ALL_ATTRIBUTES',
                ExclusiveStartKey=response['LastEvaluatedKey'])

            data.extend(response['Items'])

        return data

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
