from enum import Enum, unique, auto

@unique
class PageType(Enum):
    OVERVIEW = auto()
    METRICS = auto()
    MANAGER = auto()
    INCREASE = auto()
