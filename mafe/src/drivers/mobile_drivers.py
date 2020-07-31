import logging
from appium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait


logger = logging.getLogger(__name__)


class MobileBaseDriver:
    def __init__(self, remote_url):
        self._driver = None
        self._remote_url = remote_url

    def _get_element_attribute(self, locator, attr, timeout=5):
        try:
            element = self.wait_until(
                condition=lambda m: self.get_element(locator),
                timeout=timeout
            )
            value = element.get_attribute(attr)
            return value
        except TimeoutException:
            logging.exception(f'No such element found {locator}')

    def open_application(self, app_opts):
        try:
            driver = webdriver.Remote(self._remote_url, app_opts)
        except WebDriverException as e:
            logger.exception(
                f'An exception occured, when trying to instantiate webdriver\n Exception:{e}'
            )
        else:
            self._driver = driver

    def close_application(self):
        self._driver.close_app()

    def terminate_application(self, app_package):
        return self._driver.terminate_app(app_package)

    def send_text(self, locator, text):
        return self._driver.find_element(*locator).send_keys(text)

    def get_text(self, locator):
        return self._get_element_attribute(locator, 'text').lower()

    def get_element(self, locator):
        return self._driver.find_element(*locator)

    def get_all_elements(self, locator):
        return self._driver.find_elements(*locator)

    def is_element_present(self, locator):
        return len(self.get_all_elements(locator)) > 0

    def click_element(self, locator, timeout=5):
        try:
            self.wait_until(
                condition=lambda m: self.get_element(locator),
                timeout=timeout
            ).click()
        except TimeoutException as e:
            logging.exception(f'Failed to click\nException{e}')

    def wait_until(self, condition, timeout=5):
        return WebDriverWait(self._driver, timeout).until(condition)

    def wait_until_not(self, condition, timeout=5):
        return WebDriverWait(self._driver, timeout).until_not(condition)

    def close(self):
        return self._driver.close()

    def quit(self):
        return self._driver.quit()


class AndroidMobileDriver(MobileBaseDriver):
    def __init__(self, remote_url, desired_capabilities):
        super().__init__(remote_url, desired_capabilities)