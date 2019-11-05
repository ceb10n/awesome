from dataclasses import dataclass
from typing import List

from .projection_type import ProjectionType


@dataclass
class Projection:
    projection_type: ProjectionType
    non_key_attributes: List[str]

    def to_schema(self) -> dict:
        schema = {
            'ProjectionType': self.projection_type.value}

        if self.non_key_attributes:
            schema['NonKeyAttributes'] = [attr for attr in self.non_key_attributes]

        return schema
