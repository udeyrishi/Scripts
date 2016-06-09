#!/usr/bin/env python3

"""
Clone a GitHub repo via SSH without specifying the complete link, because #lazy.
"""

from argparse import ArgumentParser
from subprocess import run
from sys import exit

DEFAULT_GIT_BIN = '/usr/local/bin/git'
DEFAULT_USER_NAME = 'udeyrishi'

def get_repo_link(user_name, repo_name):
    return 'git@github.com:{0}/{1}.git'.format(user_name, repo_name)

def get_args():
    argument_parser = ArgumentParser()
    argument_parser.add_argument('repo', help='the repo\'s name')
    argument_parser.add_argument('-u', '--user', default=DEFAULT_USER_NAME,
                                  help='the GitHub username to use. Default=' + DEFAULT_USER_NAME)
    argument_parser.add_argument('-g', '--git', default=DEFAULT_GIT_BIN,
                                  help='the path to the git binary. Default=' + DEFAULT_GIT_BIN)
    return argument_parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    exit_code = run([args.git, "clone", get_repo_link(args.user, args.repo)]).returncode
    exit(exit_code)
