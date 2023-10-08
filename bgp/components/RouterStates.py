from enum import Enum

class RouterStates(Enum):
    OFFLINE = "OFFLINE"
    CONNECT = "CONNECT"
    IDLE = "IDLE" 
    ACTIVE = "ACTIVE"
    OPENSENT = "OPENSENT"
    OPENCONFIRM = "OPENCONFIRM"
    ESTABLISHED = "ESTABLISHED"