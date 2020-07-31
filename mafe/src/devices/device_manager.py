import re
from mafe.devices import AndroidDevice
from mafe.services import AndroidCliService
from mafe.services import LocalShellCliService


def get_device_info_props(device_adb_id):
    acs = AndroidCliService(device_adb_id)
    props = {
        'name': 'ro.product.manufacturer',
        'model': 'ro.product.model',
        'version': 'ro.build.version.release'
    }
    pattern = re.compile(r'\[(.*?)\]: \[(.*?)\]$')
    for key, value in props.items():
        cmd = f'getprop {value}'
        output = acs.send_command(cmd)
        output.check_returncode()

        match = pattern.match(output)
        if match:
            props[key] = match.group(2)

    return props


class DeviceManager:
    def __init__(self):
        self._devices = []
        self._local_shell_service = LocalShellCliService()

    def _get_adb_devices_output(self):
        pattern = re.compile(r'^([0-9a-zA-Z]+)\s+(.+?)$')
        output = self._local_shell_service.send_command('adb devices')
        output.check_returncode()
        output = output.strip().split('\n')[1:]
        connected_devices = {}
        for line in output:
            match = pattern.match(line.strip())
            if match:
                id, state = match.group(1), match.group(2)
                connected_devices[id] = state

        return connected_devices 

    def _refesh(self):
        if not self._devices:
            self.derive_android_devices()
        else:
            adb_devices = self._get_adb_devices_output()
            for index, device in enumerate(self._devices):
                if device.udid in adb_devices:
                    device.state = adb_devices[device.udid]
                else:
                    del self._devices[index]

    def derive_android_devices(self):
        adb_devices = self._get_adb_devices_output()
        devices = []
        for id, status in adb_devices.items():
            info_props = get_device_info_props(id)
            device = AndroidDevice(
                id, info_props['name'],
                info_props['model'],
                info_props['version']
            )
            device.state = status
            devices.append(device)

        self._devices = devices
    
    def get_devices(self, selected=False ,**opts):
        self._refesh()
        devices = []
        if selected:
            for device in self._devices:
                if device.selected: devices.append(device)
        else:
            devices = self._devices
        
        return devices
