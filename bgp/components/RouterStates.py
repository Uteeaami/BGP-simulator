from enum import Enum

class RouterStates(Enum):
    OFFLINE = "OFFLINE"
    IDLE = "IDLE"
    CONNECTING = "CONNECTING"
    ACTIVE = "ACTIVE"