import os
import time
from getpass import getpass
from string import Template
import functools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from pprint import pprint


def timer(origin_func):
    @functools.wraps(origin_func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        results = origin_func(*args, **kwargs)
        end_time = round(time.time() - start_time)
        print(f'total cost of time: {end_time} seconds.')
        return results
    return wrapper


class Crawler:
    def __init__(self, url, browser=None):
        self.url = url
        self.browser = browser
        while True:
            # use the pre-defined value or let the user to input it from the console.
            self.user_defined_browser = (
                    self.browser or
                    input('preferred browser?(default:phantomjs)\n(press enter to go for the default...) ')
            )
            # go for phantomjs browser which is the default.
            if self.user_defined_browser in ('phantomjs', ''):
                # set the chrome webdriver executable depends on the OS.
                self.executable = (lambda: 'phantomjs' if os.sys.platform == 'linux' else 'phantomjs.exe')()
                self.driver = webdriver.PhantomJS(
                    service_args=['--ignore-ssl-errors=true'],
                    executable_path=os.path.join(os.path.abspath('.'), self.executable),
                )
                self.driver.set_window_size(1024, 768)
                break
            # go for chrome browser
            elif self.user_defined_browser == 'chrome':
                # set the chrome webdriver executable depends on the OS.
                self.executable = (lambda: 'chromedriver' if os.sys.platform == 'linux' else 'chromedriver.exe')()
                self.options = webdriver.ChromeOptions()
                self.options.add_argument('--headless')
                self.options.add_argument('--allow-running-insecure-content')
                self.options.add_argument('--allow-insecure-localhost')
                self.options.add_argument('--ignore-certificate-errors')
                # self.options.add_argument('--no-sandbox')
                self.options.add_argument('--window-size=1024,768')
                self.options.add_argument('--reduce-security-for-testing')
                # self.options.add_argument('--sync-allow-insecure-xmpp-connection')

                self.capabilities = webdriver.DesiredCapabilities.CHROME.copy()
                self.capabilities['acceptSslCerts'] = True
                self.capabilities['acceptInsecureCerts'] = True

                self.driver = webdriver.Chrome(
                    chrome_options=self.options,
                    executable_path=os.path.join(os.path.abspath('.'), self.executable),
                    desired_capabilities=self.capabilities,
                )
                break
            # or go for firefox browser.
            elif self.user_defined_browser == 'firefox':
                # set the firefox webdriver executable depends on the OS.
                self.executable = (lambda: 'geckodriver' if os.sys.platform == 'linux' else 'geckodriver32.exe')()
                self.options = webdriver.FirefoxOptions()
                # self.options.add_argument('--no-sandbox')
                # self.options.add_argument('--window-size=1420,1080')
                # self.options.add_argument('--headless')
                # self.options.add_argument('--disable-gpu')
                self.options.add_argument('--ignore-certificate-errors')

                self.capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
                self.capabilities['acceptSslCerts'] = True
                self.capabilities['acceptInsecureCerts'] = True

                self.driver = webdriver.Firefox(
                    executable_path=os.path.join(os.path.abspath('.'), self.executable),
                    firefox_options=self.options,
                    desired_capabilities=self.capabilities,
                )
                break
            else:
                print("choose either 'firefox' or 'chrome'...\n")

    def __enter__(self):
        print('<<< starting browser... >>>')
        # if calling the Class with a url parameter, do the "get url " method.
        if self.url:
            self.driver.get(self.url)
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()
        print('<<< closing browser... >>>')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.url})'


if __name__ == '__main__':
    url = 'https://www.google.com/'
    with Crawler(url, 'chrome') as d:
        i = d.find_element_by_name('q')
        i.send_keys('python')
        i.send_keys(Keys.RETURN)
        d.get_screenshot_as_file(os.path.join(os.path.abspath('.'), '000.png'))
        soup = BeautifulSoup(d.page_source, 'lxml')
        x = soup.find('div', attrs={'id': 'rso'}).find_all('div', 'g')
        pprint([print(i.find('h3', 'r').text, i.find('h3', 'r').find('a').get('href')) for i in x])
