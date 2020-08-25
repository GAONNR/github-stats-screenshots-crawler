import os
import glob
import argparse
import subprocess
import pandas as pd

from git import Repo
from options import CREDENTIAL


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def git_clone(url):
    git_url = ('//%s@github.com/' %
               CREDENTIAL['id']).join(url.split('//github.com/'))
    repo_name = url.split('/')[-1]
    Repo.clone_from(git_url, './repos/%s' % repo_name)
    print('Cloned %s.' % repo_name)


def _main(args):
    df = pd.read_csv('url_list.csv')

    if not args.script_only:
        for url in df['URL']:
            git_clone(url.strip())

    for reponame in glob.glob('./repos/*/'):
        with cd(reponame):
            subprocess.call(['bash', '../../git_commit_log.sh'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--script_only', action='store_true')
    args = parser.parse_args()
    _main(args)
