import requests
from mafe.enums import Platforms
from mafe.drivers import AndroidMobileDriver


def url_ok(url):
    r = requests.head(url)
    return r.status_code == 200


class DriverFactory:

    @staticmethod
    def get_mobile_driver(platform, remote_url, **opts):
        if not url_ok(remote_url):
            raise(
                'Could not connect to {0}'.format(remote_url)
            )
        if platform == Platforms.ANDROID:
            driver = AndroidMobileDriver(remote_url)
        else:
            raise(
                '{0} platform is not supported'.format(platform)
            )

        return driver

