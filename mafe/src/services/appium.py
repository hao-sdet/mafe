import json
import time
import logging
import subprocess
from mafe.enums.platforms import Platforms
from mafe.drivers import DriverFactory


logger = logging.getLogger(__name__)


DEFAULT_APPIUM_HOST = '127.0.0.1'
DEFAULT_APPIUM_PORT = 4723


class AppiumServiceException(Exception):
    pass


class AppiumService:
    def __init__(self, platform, desired_capabilities):
        self.__appium_server_proc = None
        self._driver = None
        self._host = DEFAULT_APPIUM_HOST
        self._port = next(DEFAULT_APPIUM_PORT)
        self._remote_url = f'http://{self._host}:{self._port}/wd/hub'
        self._desired_capabilities = desired_capabilities

        self._df = DriverFactory()
        self._driver = self._df.get_mobile_driver(platform, self._remote_url)

    @property
    def driver(self):
        self._driver

    def start(self):
        try:
            current_time = time.strftime('%Y_%m_%d_%H_%M_%S')
            self.args_list = [
                'appium',
                '--relaxed-security',
                '--log', f'/tmp/appium_{current_time}.log',
                '--local-timezone',
                '--log-no-colors',
                '--port', str(self._port),
                '--default-capabilities', json.dumps(self._desired_capabilities)
            ]
            self.stop()
            self.__appium_server_proc = subprocess.Popen(
                self.args_list,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
        except Exception as e:
            logger.exception(
                f'An exception occured, when trying to start appium server\nException: {e}'
            )
        finally:
            return self

    def stop(self):
        if self.driver:
            self.driver.close_application()
            self.driver.quit()
        
        if self.__appium_server_proc.poll() is None:
            self.__appium_server_proc.kill()

        self.__appium_server_proc = None
