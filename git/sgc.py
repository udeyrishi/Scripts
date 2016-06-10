#!/usr/bin/env python3

"""
Smart Git Clone: Clone a GitHub repo via SSH without specifying the complete link, because #lazy.
"""

from argparse import ArgumentParser
from subprocess import run
from sys import exit
from urllib.error import HTTPError
from urllib.request import urlopen

import json

# See: https://help.github.com/articles/creating-an-access-token-for-command-line-use/
# The token should have 'repo' access
DEFAULT_GITHUB_TOKEN = None
DEFAULT_USER_NAME = None
DEFAULT_GIT_BIN = '/usr/local/bin/git'


def is_none_or_empty(string):
    return string is None or string.strip() == ''


def get_all_repo_apis(user_name, github_token):
    apis = []
    if not is_none_or_empty(user_name):
        apis.append('https://api.github.com/users/{0}/repos'.format(user_name))

    if not is_none_or_empty(user_name) and not is_none_or_empty(github_token):
        base_format = 'https://api.github.com/user/repos?access_token={0}&affiliation={1}'
        apis += [base_format.format(github_token, 'organization_member'),
                 base_format.format(github_token, 'owner'),
                 base_format.format(github_token, 'collaborator')]

    return apis


def http_get_json(url):
    return json.loads(urlopen(url).read().decode('utf-8'))


def get_repos_gen(user_name, github_token):
    apis = get_all_repo_apis(user_name, github_token)
    for api in apis:
        yield http_get_json(api)


def get_repo(user_name, github_token, repo):
    repo_api = 'https://api.github.com/repos/{0}/{1}?access_token={2}'.format(user_name, repo, github_token)
    return http_get_json(repo_api)


def get_closest_repo_link(user_name, github_token, repo_name_substring):
    match = None
    try:
        match = get_repo(user_name, github_token, repo_name_substring)
    except HTTPError as e:
        repos_gen = get_repos_gen(user_name, github_token)
        for repos_list in repos_gen:
            for repo in repos_list:
                if repo['name'].lower().find(repo_name_substring.lower()) >= 0:
                    if match is None:
                        match = repo
                    elif match['full_name'] != repo['full_name']:
                        raise ValueError('Multiple repos found with substring ' + repo_name_substring)

        if match is None:
            raise ValueError('No repos found with substring ' + repo_name_substring)

    return 'git@github.com:{0}.git'.format(match['full_name'])


def get_args():
    argument_parser = ArgumentParser()
    argument_parser.add_argument('repo', help='the repo\'s name, partial or exact')
    argument_parser.add_argument('-u', '--user', default=DEFAULT_USER_NAME,
                                  help='the GitHub username to use. Default=' + DEFAULT_USER_NAME)
    argument_parser.add_argument('-g', '--git', default=DEFAULT_GIT_BIN,
                                  help='the path to the git binary. Default=' + DEFAULT_GIT_BIN)
    argument_parser.add_argument('-t', '--token', default=DEFAULT_GITHUB_TOKEN,
                                  help='the GitHub token to use for accessing private repos. If none ' +
                                  'provided, or if the default is None/empty, only public repos are used. ' +
                                  'Default=' + DEFAULT_GITHUB_TOKEN)
    return argument_parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    try:
        repo_link = get_closest_repo_link(args.user, args.token, args.repo)
        exit_code = run([args.git, "clone", repo_link]).returncode
    except (ValueError, HTTPError) as e:
        print(str(e))
        exit_code = -1

    exit(exit_code)
