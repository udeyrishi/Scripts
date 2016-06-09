#!/usr/bin/env python

import argparse
from os import system

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('installer', help='The path to the installer .app')
    parser.add_argument('volume', help='The volume name')
    args = parser.parse_args()
    installer_path = args.installer
    volume = args.volume

    system('sudo {0}/Contents/Resources/createinstallmedia --volume /Volumes/{1} --applicationpath {0} --nointeraction'.format(installer_path, volume))