#!/usr/bin/env python3

from setuptools import setup, find_packages
from setuptools.command.install import install


VERSION = '0.0.1'


f = open('README.md', 'r', encoding='utf-8', errors='ignore')
LONG_DESCRIPTION = f.read()
f.close()


class MafeInstall(install):
    def run(self):
        install.run(self)
        pass


setup(
    name='mafe',
    version=VERSION,
    description='An automation framework for mobile application testing',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Ryan Le',
    author_email='contact@rlespace.com',
    url='https://github.com/rlespace/mafe',
    license='MIT',
    install_requires=[
        'cement==3.0.2',
        'requests==2.31.0',
        'tabulate==0.8.7',
        'python-socketio==4.6.0'
    ],
    package_dir={
        'mafe.enums': 'mafe/src/enums',
        'mafe.devices': 'mafe/src/devices',
        'mafe.drivers': 'mafe/src/drivers',
        'mafe.services': 'mafe/src/services'
    },
    packages=[
        'mafe',
        'mafe.utils',
        'mafe.enums',
        'mafe.devices',
        'mafe.drivers',
        'mafe.services'
    ],
    entry_points="""
        [console_scripts]
        mafe = mafe.cli.app:main
    """,
    include_package_data=True,
    cmdclass={'install': MafeInstall}
)



