from enum import Enum


class IndexStatus(Enum):
    CREATING = 'CREATING'
    UPDATING = 'UPDATING'
    DELETING = 'DELETING'
    ACTIVE = 'ACTIVE'
