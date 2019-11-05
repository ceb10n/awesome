from enum import Enum


class AttributeType(Enum):
    BINARY = 'B'
    BOOLEAN = 'BOOL'
    NUMBER = 'N'
    STRING = 'S'
    SET_BINARY = 'BS'
    SET_NUMBER = 'NS'
    SET_STRING = 'SS'
