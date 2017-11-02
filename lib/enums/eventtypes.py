from enum import Enum, unique

@unique
class EventType(Enum):
    UNKNOWN = -1
    DEL = 0
    NEW = 1
