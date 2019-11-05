from enum import Enum


class TableStatus(Enum):
    CREATING = 'CREATING'
    UPDATING = 'UPDATING'
    DELETING = 'DELETING'
    ACTIVE = 'ACTIVE'
