import selenium
import pandas as pd

from pylatex import (Document, Section, Figure, Command)
from pylatex.utils import NoEscape
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from options import CREDENTIAL

FNAME_RULE = [
    '%s/%s.png',
    '%s/%s_open_issues.png',
    '%s/%s_closed_issues.png',
    '%s/%s_traffic.png'
]

IMAGEPATH = '../screenshots'

LATEX_OPTION = {'tmargin': '1cm', 'lmargin': '3cm'}


def get_license(driver, license_url):
    driver.get(license_url)

    try:
        raw_lines = driver.find_elements_by_css_selector(
            'div.blob-wrapper tbody tr td:nth-child(2)')
        lines = [el.text.strip() for el in raw_lines]
        return ' \n'.join(lines).replace(' \n \n', 'SUPERSUPER').replace(' \n', ' ').replace('SUPERSUPER', '\n')
    except:
        return 'None'


def generate_pdf(driver, url, fname_base):
    license_url = '%s/blob/master/LICENSE' % url
    license_txt = get_license(driver, license_url)

    doc = Document(geometry_options=LATEX_OPTION)
    doc.preamble.append(Command('title', fname_base))
    doc.append(NoEscape('\\maketitle'))
    with doc.create(Section('LICENSE')):
        doc.append(license_txt)
    with doc.create(Section('Web pages')):
        for fname_rule in FNAME_RULE:
            fname = fname_rule % (IMAGEPATH, fname_base)
            with doc.create(Figure(position='!htbp')) as fig:
                fig.add_image(fname, width=NoEscape('\\textwidth'))
    doc.generate_pdf('pdfs/%s' % fname_base,
                     clean_tex=False, compiler='pdflatex')


def prepare_for_github_credentials():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(10)

    print('Github login processing...')
    driver.get('https://github.com/login')
    driver.find_element_by_id('login_field').send_keys(CREDENTIAL['id'])
    driver.find_element_by_id('password').send_keys(CREDENTIAL['pw'])
    driver.find_element_by_name('commit').click()
    print('Done.')

    return driver


def __main():
    driver = prepare_for_github_credentials()

    df = pd.read_csv('url_list.csv')
    for url in tqdm(df['URL']):
        fname_base = url.split('/')[-1]
        generate_pdf(driver, url, fname_base)


if __name__ == '__main__':
    __main()
