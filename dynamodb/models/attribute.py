from dataclasses import dataclass
from typing import Any

from .attribute_type import AttributeType


@dataclass
class Attribute:
    name: str
    attr_type: AttributeType
    value: Any

    def to_schema(self):
        return {
            'AttributeName': self.name,
            'AttributeType': self.attr_type.value
        }
