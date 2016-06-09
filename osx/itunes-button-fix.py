#!/usr/local/bin/python3

"""
OS X, by default, opens up iTunes if the play/pause button of your headphones is pressed. Stop (or
resume) this service, so that other apps can potentially listen to these events.
"""

import os
import sys

def print_error_args(program_name):
    print('Usage: {0} <stop/resume>'.format(program_name))

def main():
    if len(sys.argv) < 2:
        print_error_args(sys.argv[0])
        return

    if sys.argv[1] == 'resume':
        os.system('launchctl load -w /System/Library/LaunchAgents/com.apple.rcd.plist')
    elif sys.argv[1] == 'stop':
        os.system('launchctl unload -w /System/Library/LaunchAgents/com.apple.rcd.plist')
    else:
        print_error_args(sys.argv[0])


if __name__ == '__main__':
    main()
