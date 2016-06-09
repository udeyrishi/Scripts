#!/usr/bin/env python3

"""
Clone a GitHub repo via SSH without specifying the complete link, because #lazy.
"""

from argparse import ArgumentParser
from subprocess import run
from sys import exit
from urllib.error import HTTPError
from urllib.request import urlopen

import json

DEFAULT_GIT_BIN = '/usr/local/bin/git'
DEFAULT_USER_NAME = 'udeyrishi'
GITHUB_SSH_FORMAT = 'git@github.com:{0}/{1}.git'
GITHUB_REPOS_API_FORMAT = 'https://api.github.com/users/{0}/repos'


def get_repo_link(user_name, repo_name):
    return GITHUB_SSH_FORMAT.format(user_name, repo_name)


def get_repos(user_name):
    http_get_link = GITHUB_REPOS_API_FORMAT.format(user_name)
    repos_response = json.loads(urlopen(http_get_link).read().decode("utf-8"))
    return [repo['name'] for repo in repos_response]


def get_closest_repo_link(user_name, repo_name_substring):
    repos = get_repos(user_name)
    match = None
    for repo in repos:
        if repo.lower().find(repo_name_substring.lower()) >= 0:
            if match is None:
                match = repo
            else:
                raise ValueError('Multiple repos found with substring ' + repo_name_substring)

    if match is None:
        raise ValueError('No repose found with substring ' + repo_name_substring)

    return get_repo_link(user_name, match)


def get_args():
    argument_parser = ArgumentParser()
    argument_parser.add_argument('repo', help='the repo\'s name')
    argument_parser.add_argument('-u', '--user', default=DEFAULT_USER_NAME,
                                  help='the GitHub username to use. Default=' + DEFAULT_USER_NAME)
    argument_parser.add_argument('-g', '--git', default=DEFAULT_GIT_BIN,
                                  help='the path to the git binary. Default=' + DEFAULT_GIT_BIN)
    argument_parser.add_argument('-s', '--substring', action='store_true',
                                  help='try to perform a substring comparison with the user\'s repos ' +
                                  'to find a unique match, and clone that one.')
    return argument_parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    try:
        if args.substring:
            repo_link = get_closest_repo_link(args.user, args.repo)
        else:
            repo_link = get_repo_link(args.user, args.repo)

        exit_code = run([args.git, "clone", repo_link]).returncode
    except (ValueError, HTTPError) as e:
        print(str(e))
        exit_code = -1

    exit(exit_code)
