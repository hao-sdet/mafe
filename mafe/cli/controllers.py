from cement import Controller, ex
from mafe.utils import MafeClient


class BaseController(Controller):
    class Meta:
        label = 'base'

    def _default(self):
        self.app.args.print_help()

    @ex(
        help='list all connected devices',
        arguments=[
            ( [ '-g', '--group' ],
              { 'help' : 'list all devices belong to group',
                'action' : 'store',
                'dest' : 'group' } )
        ]
    )
    def devices(self):
        client = MafeClient()
        
        group = self.app.pargs.group
        
        opts = {}
        if group:
            opts['group'] = group

        client.send_command('devices', extra=opts)
        devices = client.data
        
        label = {
            'name': "NAME",
            'model': "MODEL",
            'state': "CURRENT STATE",
            'group': "GROUP",
            'selected': "CURRENT SELECTED",
        }

        data = []
        for device in devices:
            data.append(
                {
                    label['name']: device.name,
                    label['model']: device.model,
                    label['state']: device.state,
                    label['group']: device.group,
                    label['selected']: device.selected
                }
            )
        self.app.render(
            data, format='tabulate', headers='keys', tablefmt='simple'
        )
    
    @ex(
        help='select devices',
        arguments=[
            ( [ '-d', '--devices' ],
              { 'help' : 'list of devices, space separated',
                'nargs': "*",
                'type' : str,
                'action' : 'store',
                'dest' : 'devices' } ),
            ( [ '-g', '--group' ],
              { 'help' : 'group name',
                'action' : 'store',
                'dest' : 'group' } )
        ]
    )
    def select(self):
        client = MafeClient()
        devices = self.app.pargs.devices
        group = self.app.pargs.group

        opts = {'devices': devices, 'group': group}
        client.send_command('select', extra=opts)
    
    @ex(
        help='deselect devices',
        arguments=[
            ( [ '-d', '--devices' ],
              { 'help' : 'list of devices to remove, space separated',
                'nargs': "*",
                'type' : str,
                'action' : 'store',
                'dest' : 'devices' } ),
            ( [ '-g', '--group' ],
              { 'help' : 'group name',
                'action' : 'store',
                'dest' : 'group' } )
        ]
    )
    def deselect(self):
        client = MafeClient()
        devices = self.app.pargs.devices
        group = self.app.pargs.group

        opts = {'devices': devices, 'group': group}
        client.send_command('deselect', extra=opts)
        
    @ex(
        help='group devices by device name',
        arguments=[
            ( [ '-d', '--devices' ],
              { 'help' : 'list of devices, space separated',
                'nargs': "*",
                'type' : str,
                'action' : 'store',
                'dest' : 'devices' } ),
            ( [ '-g', '--group' ],
              { 'help' : 'group name',
                'action' : 'store',
                'dest' : 'group' } )
        ]
    )
    def group(self):
        client = MafeClient()
        devices = self.app.pargs.devices
        group = self.app.pargs.group

        opts = {'devices': devices, 'group': group}
        client.send_command('group', extra=opts)
        
    @ex(
        help='install apk file on selected devices',
        arguments=[
            ( [ '-a', '--apk' ],
              { 'help' : 'apk file path',
                'action' : 'store',
                'dest' : 'apk_file_path' } ),
        ]
    )
    def install(self):
        client = MafeClient()
        apk_file_path = self.app.pargs.apk_file_path

        opts = {'apk_file': apk_file_path}
        client.send_command('install', extra=opts)
        
    @ex(
        help='uninstall application from selected devices',
        arguments=[
            ( [ '-a', '--app' ],
              { 'help' : 'application package name (eg. com.my.app)',
                'action' : 'store',
                'dest' : 'app_package' } ),
        ]
    )
    def uninstall(self):
        client = MafeClient()
        app_package = self.app.pargs.app_package

        opts = {'app_package': app_package}
        client.send_command('uninstall', extra=opts)
    
    @ex(
        help='execute tests on selected devices',
        arguments=[
            ( [ '-t', '--tests' ],
              { 'help' : 'test files',
                'action' : 'store',
                'dest' : 'tests' } ),
        ]
    )
    def run(self):
        raise NotImplementedError

    @ex(
        help='build apk file from src',
        arguments=[
            ( [ '-s', '--src' ],
              { 'help' : 'application folder location',
                'action' : 'store',
                'dest' : 'src' } ),
            ( [ '-d', '--dest' ],
              { 'help' : 'application folder location',
                'action' : 'store',
                'dest' : 'dest' } ),
        ]
    )
    def build(self):
        raise NotImplementedError

    @ex(
        help='deploy with fastlane',
        arguments=[
            ( [ '-s', '--src' ],
              { 'help' : 'application folder location',
                'action' : 'store',
                'dest' : 'src' } ),
        ]
    )
    def deploy(self):
        raise NotImplementedError