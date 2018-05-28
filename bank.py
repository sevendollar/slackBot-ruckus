import os
import time
from getpass import getpass
import functools
from string import Template
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
                    input('preferred browser?(default:chrome)\n(press enter to go for the default...) ')
            )

            # go for chrome browser which is the default.
            if self.user_defined_browser in ('chrome', ''):
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


# returns a dict of interest rate data that comes from the Taiwan bank web page.
def interest_rate(currency=None, intent=None):
    intent = None if intent == '' else intent
    currency = currency is not None and currency.upper() or None
    url = 'http://rate.bot.com.tw/xrt?Lang=zh-TW'  # taiwan bank

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    rate_lst = {
        i.find('div', 'hidden-phone').text.strip()[-4:-1]:  # currency
            (
                i.find('td', 'rate-content-sight').text.replace('-', ''),  # bank buy, user sell rate
                i.find('td', 'rate-content-sight').find_next('td').text.replace('-', ''),  # bank sell, user buy rate
                i.find('div', 'hidden-phone').text.strip().split(' ')[0],  # currency in chinese
            )
        for i in soup.find('table').find('tbody').find_all('tr')}
    rate_lst.update({'time': soup.find('span', {'class': 'time'}).text})
    return rate_lst.get(currency, rate_lst) if intent is None else (
        rate_lst.get(currency)[1] if rate_lst.get(currency) and intent == 'buy' else (
            rate_lst.get(currency)[0] if rate_lst.get(currency) and intent == 'sell' else 'unknown'))


# returns a string of table of all interest rates which comes from interest_rate().
def interest_rate_table():
    i_rate = interest_rate()
    time = i_rate.pop('time')

    currency_max_length = max(len(key) for key in i_rate.keys()) + 1
    buy_max_length = max(len(key[1]) for key in i_rate.values()) + 1
    sell_max_length = max(len(key[0]) for key in i_rate.values()) + 1

    currency_column = 'curr'.ljust(currency_max_length)
    buy_column = 'buy'.rjust(buy_max_length)
    sell_column = 'sell'.ljust(sell_max_length)

    r = f'{time}\n\n{currency_column}|{buy_column} | {sell_column}\n'
    x = ''.join([f'{key.ljust(currency_max_length)}|{value[1].rjust(buy_max_length)} | {value[0].ljust(buy_max_length)}({value[-1]})\n'\
     for key, value in i_rate.items() if value[0]])

    return r + x


#  TODO: interest rate converter

if __name__ == '__main__':
    pass
    # country = Template('$country').substitute(country=input('what currency of country do your want to look up?'))
    # intent = Template('$intent').substitute(intent=input('buy or sell?'))

