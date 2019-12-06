import time
import argparse
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from options import CREDENTIAL

parser = argparse.ArgumentParser()
parser.add_argument('--no_permission', action='store_true')


def prepare_for_github_credentials():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_options=chrome_options)

    print('Github login processing...')
    driver.get('https://github.com/login')
    driver.find_element_by_id('login_field').send_keys(CREDENTIAL['id'])
    driver.find_element_by_id('password').send_keys(CREDENTIAL['pw'])
    driver.find_element_by_name('commit').click()
    time.sleep(4)
    print('Done.')

    return driver


def get_fullpage_shot(driver, url):
    print('Accessing %s...' % url)
    driver.get(url)
    time.sleep(2)

    body = driver.find_element_by_tag_name('body')
    window_height = body.size['height']
    print(window_height)
    print('Capturing...')
    driver.set_window_size(1920, window_height)  # the trick
    time.sleep(2)
    driver.save_screenshot("screenshot1.png")
    print('Done.')


def __main():
    args = parser.parse_args()
    print(args)
    driver = prepare_for_github_credentials()
    get_fullpage_shot(
        driver, 'https://github.com/nlpcl-lab/TEA-corpus-project')
    driver.quit()


if __name__ == '__main__':
    __main()
