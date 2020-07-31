from mafe.enums import Platforms, DeviceStates
from mafe.services import (
    AppiumService,
    AndroidCliService,
    LocalAdbService
)

class BaseDevice:
    def __init__(self, udid, name, model, version):
        self.udid = udid
        self.name = name
        self.model = model
        self.version = version
        self._state = None
        self._group = None
        self._selected = False
    
    @property
    def info(self):
        return {
            'udid': self.udid, 'name': self.name,
            'model': self.model, 'state': self.state,
            'selected': self.selected
        }
    
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, value):
        self._selected = value
    

class AndroidDevice(BaseDevice):
    def __init__(self, udid, name, model, version):
        super().__init__(udid, name, model, version)
        self._adb_service = LocalAdbService(AndroidCliService(self.udid))
        self._appium_service = AppiumService(
            platform=Platforms.ANDROID,
            desired_capabilities=
            {
                'udid': self.udid,
                'deviceName': self.udid,
                'platformName': 'Android',
                'version': self.version,
                'automationName': 'uiAutomator2',
                'newCommandTimeout': 3600,
                'orientation': 'PORTRAIT'
            }
        ).start()

    def __del__(self):
        if self._appium_service:
            self._appium_service.stop()
        
    def start_application(self, app_package, app_activity):
        return self._appium_service.driver.open_application(
            {'appPackage': app_package, 'appActivity': app_activity}
        )
    
    def stop_application(self, app_package):
        return self._appium_service.driver.terminate_app(app_package)

    def install_application(self, apk_file_path):
        return self._adb_service.install(apk_file_path)

    def uninstall_application(self, app_package):
        return self._adb_service.uninstall(app_package) 


class IOSDevice(BaseDevice):
    pass

