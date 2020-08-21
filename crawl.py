import time
import argparse
import selenium
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from options import CREDENTIAL


parser = argparse.ArgumentParser()
parser.add_argument('--no_permission', action='store_true')
parser.add_argument('--timeout', type=int, default=10)
ARGS = parser.parse_args()


def get_number_from_page(driver, selector):
    try:
        return int(WebDriverWait(driver, ARGS.timeout)
                   .until(
                       EC.presence_of_element_located(
                           (By.CSS_SELECTOR, selector)))
                   .get_attribute('innerText'))
    except selenium.common.exceptions.TimeoutException:
        return int(WebDriverWait(driver, ARGS.timeout * 12)
                   .until(
                       EC.presence_of_element_located(
                           (By.CSS_SELECTOR, selector)))
                   .get_attribute('innerText'))
    except ValueError:
        time.sleep(2)
        return int(WebDriverWait(driver, ARGS.timeout)
                   .until(
                       EC.presence_of_element_located(
                           (By.CSS_SELECTOR, selector)))
                   .get_attribute('innerText'))


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

        self.watches = get_number_from_page(
            driver, 'ul.pagehead-actions li:nth-child(1) a.social-count')
        self.stars = get_number_from_page(
            driver, 'ul.pagehead-actions li:nth-child(2) a.social-count')
        self.forks = get_number_from_page(
            driver, 'ul.pagehead-actions li:nth-child(3) a.social-count')
        self.commits = get_number_from_page(
            driver, '.js-details-container.Details ul.list-style-none span strong')
        self.branches = get_number_from_page(
            driver, '.file-navigation .flex-self-center a:nth-child(1) strong')
        if len(driver.find_elements_by_css_selector('.BorderGrid .BorderGrid-row:nth-child(2) h2.h4 span.Counter')) > 0:
            self.releases = get_number_from_page(
                driver, '.BorderGrid .BorderGrid-row:nth-child(2) h2.h4 span.Counter')
        if len(driver.find_elements_by_css_selector('.BorderGrid .BorderGrid-row')) < 6:
            self.contributors = 1
        else:
            self.contributors = get_number_from_page(
                driver, '.BorderGrid .BorderGrid-row:nth-child(5) h2.h4 span.Counter')

    def __update_from_issues(self, driver, url):
        print('Getting stats from issues...')
        driver.get(url)

        try:
            open_issues = int(WebDriverWait(driver, ARGS.timeout)
                              .until(
                                  EC.presence_of_element_located(
                                      (By.CSS_SELECTOR,
                                       '#js-issues-toolbar div.table-list-header a:nth-child(1)')))
                              .get_attribute('innerText').strip().split('Open')[0])
            closed_issues = int(WebDriverWait(driver, ARGS.timeout)
                                .until(
                                    EC.presence_of_element_located(
                                        (By.CSS_SELECTOR,
                                         '#js-issues-toolbar div.table-list-header a:nth-child(1)')))
                                .get_attribute('innerText').strip().split('Closed')[0])
            self.issues = open_issues + closed_issues
        except selenium.common.exceptions.TimeoutException:
            self.issues = 0

    def __update_from_traffic(self, driver, url):
        print('Getting stats from traffic...')
        driver.get(url)

        try:
            self.clones = get_number_from_page(
                driver, '#js-clones-graph span.clones')
        except ValueError:
            self.clones = 0
        try:
            self.visitors = get_number_from_page(
                driver, '#js-visitors-graph span.visits')
        except ValueError:
            self.visitors = 0
        try:
            self.visitors_unique = get_number_from_page(
                driver, '#js-visitors-graph span.uniques')
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


def prepare_for_github_credentials(timeout):
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(timeout)

    print('Github login processing...')
    driver.get('https://github.com/login')
    driver.find_element_by_id('login_field').send_keys(CREDENTIAL['id'])
    driver.find_element_by_id('password').send_keys(CREDENTIAL['pw'])
    driver.find_element_by_name('commit').click()
    print('Done.')

    return driver


def get_fullpage_shot(driver, fname):
    body = driver.find_element_by_tag_name('body')
    window_height = body.size['height']
    driver.set_window_size(1920, window_height)  # the trick

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
    driver = prepare_for_github_credentials(ARGS.timeout)

    df = pd.read_csv('url_list.csv')
    res = [get_repo_stat(driver, url.strip(), ARGS.no_permission)
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
