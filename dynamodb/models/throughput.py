from dataclasses import dataclass
from datetime import datetime


@dataclass
class Throughput:
    last_increased: datetime
    last_decreased: datetime
    decreases_today: int
    read_capacity: int
    write_capacity: int

    def to_schema(self):
        schema = {
            'ReadCapacityUnits': self.read_capacity,
            'WriteCapacityUnits': self.write_capacity,
            'NumberOfDecreasesToday': self.decreases_today,
        }

        if self.last_increased:
            schema['LastIncreaseDateTime'] = self.last_increased

        if self.last_decreased:
            schema['LastDecreaseDateTime'] = self.last_decreased

        return schema
