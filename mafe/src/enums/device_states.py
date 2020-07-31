from enum import Enum


class DeviceStates(Enum):
    CONNECTING = 'connecting'
    CONNECTED = 'connected'
    DISCONNECTED = 'disconnected'