import subprocess
import logging


class CliServiceException(Exception):
    pass


class LocalShellCliService:
    def send_command(self, cmd):
        proc = subprocess.run(
            cmd.split(' '), encoding='utf-8',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if proc.returncode == 0:
            return proc.stdout
        else:
            raise CliServiceException(proc.stderr)


class AndroidCliService:
    def __init__(self, adb_device_id):
        self.id = adb_device_id

    def send_command(self, cmd, non_blocking=False):
        command = ['adb', '-s', self.id]
        command.extend(cmd.split())
        try:
            proc = subprocess.Popen(
                command, encoding='utf-8',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            if non_blocking:
                logging.debug(f'command: {command}')
                return proc

            (output, error) = proc.communicate()
            logging.debug(f'command: {command},'
                          f' return code: {proc.returncode},'
                          f' stdout: {repr(output)},'
                          f' stderr: {repr(error)}')
            if proc.returncode != 0:
                err = f'Error: {error}, code: {proc.returncode}'
                raise CliServiceException(err)
            else:
                return output
        except subprocess.CalledProcessError as e:
            msg = (
                f'Error: {e.output}, code: {e.returncode}'
            )
            raise CliServiceException(
                f'Failed to execute command: {command}\n {msg}'
            )