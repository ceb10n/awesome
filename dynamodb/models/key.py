from dataclasses import dataclass

from .key_type import KeyType


@dataclass
class Key:
    name: str
    key_type: KeyType

    def to_schema(self):
        return {
            'AttributeName': self.name,
            'KeyType': self.key_type.value}
