# Mafe
Command line interface tool for iOS and Android tester to communicate with mobile devices. It can be used to automate tedious tasks such as installing, uninstalling, starting and stopping applications on your devices

## Requirements
Python 3.6 and above

## Installation
From Source
```
git clone https://github.com/rlespace/mafe.git
pip install -e mafe
```

## Usage
```
$ mafe
usage: mafe [-h] [-d] [-q]
            {build,deploy,deselect,devices,group,install,run,select,uninstall}
            ...

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           full application debug mode
  -q, --quiet           suppress all console output

sub-commands:
  {build,deploy,deselect,devices,group,install,run,select,uninstall}
    build               build apk file from src
    deploy              deploy with fastlane
    deselect            deselect devices
    devices             list all connected devices
    group               group devices by device name
    install             install apk file on selected devices
    run                 execute tests on selected devices
    select              select devices
    uninstall           uninstall application from selected devices
```