import os
import pathlib


class AdbServiceException(Exception):
    pass


class LocalAdbService:
    def __init__(self, android_cli_service):
        self._android_cli_service = android_cli_service

    def shell(self, args):
        cmd = f'shell {args}'
        return self._android_cli_service.send_command(cmd)

    def install(self, apk_path):
        cmd = f'install -r {apk_path}'
        return self._android_cli_service.send_command(cmd)

    def uninstall(self, app_package):
        cmd = f'uninstall {app_package}'
        return self._android_cli_service.send_command(cmd)

    def push(self, src, dst):
        if pathlib.Path(src).is_file():
            cmd = f'push {src} {dst}'
        else:
            raise FileNotFoundError(f'Unable to find {src}')
        return self._android_cli_service.send_command(cmd)

    def pull(self, src, dst):
        if not os.access(dst, os.W_OK):
            raise OSError(f'Permission denied: {dst} is not accessable!')
        cmd = f'pull {src} {dst}'
        return self._android_cli_service.send_command(cmd)


class RemoteAdbService:
    pass