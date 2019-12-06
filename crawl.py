import time
import argparse
import selenium
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from options import CREDENTIAL

parser = argparse.ArgumentParser()
parser.add_argument('--no_permission', action='store_true')
parser.add_argument('--timeout', type=int, default=4)
ARGS = parser.parse_args()

MUST_VISITS = [
    '%s',
    '%s/issues',
    '%s/issues?q=is%3Aissue+is%3Aclosed',
    '%s/graphs/traffic'
]


class Stat:
    def __init__(self):
        self.watches = 0
        self.stars = 0
        self.forks = 0
        self.issues = 0
        self.commits = 0
        self.branches = 0
        self.releases = 0
        self.contributors = 0
        self.clones = 0
        self.visitors = 0
        self.visitors_unique = 0

    def __update_from_main(self, driver, url):
        print('Getting stats from main...')
        driver.get(url)
        time.sleep(ARGS.timeout)

        self.watches = int(driver.find_element_by_css_selector(
            'ul.pagehead-actions li:nth-child(1) a.social-count').get_attribute('innerHTML'))
        self.stars = int(driver.find_element_by_css_selector(
            'ul.pagehead-actions li:nth-child(2) a.social-count').get_attribute('innerHTML'))
        self.forks = int(driver.find_element_by_css_selector(
            'ul.pagehead-actions li:nth-child(3) a.social-count').get_attribute('innerHTML'))
        self.commits = int(driver.find_element_by_css_selector(
            'ul.numbers-summary li:nth-child(1) span.num').text)
        self.branches = int(driver.find_element_by_css_selector(
            'ul.numbers-summary li:nth-child(2) span.num').text)
        self.releases = int(driver.find_element_by_css_selector(
            'ul.numbers-summary li:nth-child(4) span.num').text)
        if len(driver.find_elements_by_css_selector('ul.numbers-summary li')) < 7:
            self.contributors = int(driver.find_element_by_css_selector(
                'ul.numbers-summary li:nth-child(5) span.num').text)
        else:
            self.contributors = int(driver.find_element_by_css_selector(
                'ul.numbers-summary li:nth-child(6) span.num').text)

    def __update_from_issues(self, driver, url):
        print('Getting stats from issues...')
        driver.get(url)
        time.sleep(ARGS.timeout)
        try:
            open_issues = int(driver.find_element_by_css_selector(
                '#js-issues-toolbar div.table-list-header a:nth-child(1)').text.strip().split('Open')[0])
            closed_issues = int(driver.find_element_by_css_selector(
                '#js-issues-toolbar div.table-list-header a:nth-child(1)').text.strip().split('Closed')[0])
            self.issues = open_issues + closed_issues
        except selenium.common.exceptions.NoSuchElementException:
            self.issues = 0

    def __update_from_traffic(self, driver, url):
        print('Getting stats from traffic...')
        driver.get(url)
        time.sleep(ARGS.timeout)

        try:
            self.clones = int(
                driver.find_element_by_css_selector(
                    '#js-clones-graph span.clones').text)
        except ValueError:
            self.clones = 0
        try:
            self.visitors = int(
                driver.find_element_by_css_selector(
                    '#js-visitors-graph span.visits').text)
        except ValueError:
            self.visitors = 0
        try:
            self.visitors_unique = int(
                driver.find_element_by_css_selector(
                    '#js-visitors-graph span.uniques').text)
        except ValueError:
            self.visitors_unique = 0

    def update(self, driver, url):
        fname_base = url.split('/')[-1]

        # Watches / Stars / Forks / Commits / Branches / Releases / Contributors
        self.__update_from_main(driver, url)
        get_fullpage_shot(driver, '%s.png' % fname_base)

        self.__update_from_issues(driver, '%s/issues' % url)
        get_fullpage_shot(driver, '%s_open_issues.png' % fname_base)
        driver.get('%s/issues?q=is%%3Aissue+is%%3Aclosed' % url)
        get_fullpage_shot(driver, '%s_closed_issues.png' % fname_base)

    def update_perm(self, driver, url):
        fname_base = url.split('/')[-1]

        self.__update_from_traffic(driver, '%s/graphs/traffic' % url)
        get_fullpage_shot(driver, '%s_traffic.png' % fname_base)


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
    time.sleep(ARGS.timeout)
    print('Done.')

    return driver


def get_fullpage_shot(driver, fname):
    body = driver.find_element_by_tag_name('body')
    window_height = body.size['height']
    driver.set_window_size(1920, window_height)  # the trick
    time.sleep(ARGS.timeout)

    driver.save_screenshot('screenshots/%s' % fname)


def get_repo_stat(driver, url, no_perm):
    print('Accessing %s...' % url)

    repo_stat = Stat()

    repo_stat.update(driver, url)
    if not no_perm:
        repo_stat.update_perm(driver, url)

    print('Done.')
    return repo_stat


def __main():
    driver = prepare_for_github_credentials()

    df = pd.read_csv('url_list.csv')
    res = [get_repo_stat(driver, url, ARGS.no_permission)
           for url in df['URL']]
    driver.quit()

    df['Watches'] = [stat.watches for stat in res]
    df['Stars'] = [stat.stars for stat in res]
    df['Forks'] = [stat.forks for stat in res]
    df['Issues'] = [stat.issues for stat in res]
    df['Commits'] = [stat.commits for stat in res]
    df['Branches'] = [stat.branches for stat in res]
    df['Releases'] = [stat.releases for stat in res]
    df['Contributors'] = [stat.contributors for stat in res]
    df['Clones'] = [stat.clones for stat in res]
    df['Visitors'] = [stat.visitors for stat in res]
    df['Visitors(unique)'] = [stat.visitors_unique for stat in res]

    df.to_csv('result.csv')


if __name__ == '__main__':
    __main()
