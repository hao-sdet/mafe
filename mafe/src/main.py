import socketio
import eventlet

from mafe.devices import DeviceManager


HOST = '127.0.0.1'
DEFAULT_PORT = 5210


sio = socketio.Server()
app = socketio.WSGIApp(sio)


dm = DeviceManager()
dm.derive_android_devices()


@sio.event
def connect(sid):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.event
def devices(sid, data):
    devices = dm.get_devices()
    
    resps = []
    for device in devices:
        resps.append(device.info)
    
    sio.emit('message', resps)

@sio.event
def select(sid, data):
    devices = dm.get_devices()
    for device in devices:
        if (device.udid in data['devices'] or 
                device.group == data['group']):
            device.selected = True
        else:
            device.selected = False

@sio.event
def deselect(sid, data):
    devices = dm.get_devices()
    for device in devices:
        if (device.udid in data['devices'] or 
                device.group == data['group']):
            device.selected = False

@sio.event
def group(sid, data):
    devices = dm.get_devices()
    for device in devices:
        if device.udid in data['devices']:
            device.group = data['group']

@sio.event
def install(sid, data):
    devices = dm.get_devices()
    for device in devices:
        if device.selected:
            device.install_application(data['apk_file'])

@sio.event
def uninstall(sid, data):
    devices = dm.get_devices()
    for device in devices:
        if device.selected:
            device.uninstall_application(data['app_package'])

@sio.event
def start(sid, data):
    devices = dm.get_devices()
    for device in devices:
        if device.selected:
            device.start_application(
                data['app_package'], data['app_activity']
            )

@sio.event
def stop(sid, data):
    devices = dm.get_devices()
    for device in devices:
        if device.selected:
            device.stop_application(data['app_package'])


if __name__ == '__main__':
    eventlet.wsgi.server(
        eventlet.listen((HOST, DEFAULT_PORT)), app
    )










