import logging
import socketio


logger = logging.getLogger(__name__)


DEFAULT_MAFE_PORT = 5210


class MafeClient:
    def __init__(self, host='127.0.0.1', port=DEFAULT_MAFE_PORT):
        self._ip = host
        self._port = port
        self._data = None
        self._client = socketio.Client(logger=logger)
        self._client.connect(f'http://{self._ip}:{self._port}')
        # self._client.on('message', handler=self._message_handler)

    def __del__(self):
        self.close()

    @property
    def data(self):
        return self._data

    @property
    def is_connected(self):
        return self._client.connected

    def send_command(self, command, **extra):
        self._client.emit(command, data=extra)
        
    def disconnect(self):
        if self.is_connected:
            self._client.disconnect()

    def close(self):
        self.disconnect()
        self._client = None

    
