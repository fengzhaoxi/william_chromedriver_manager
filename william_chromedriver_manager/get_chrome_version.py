#! /usr/bin/python3
# coding=utf-8
# @Time: 2023/9/20 10:43
# @Author: Feng Zhaoxi

import re
import os
import sys


class ChromeType(object):
    GOOGLE = 'google-chrome'
    CHROMIUM = 'chromium'
    MSEDGE = 'edge'


class OSType(object):
    LINUX = "linux"
    MAC = "mac"
    WIN = "win"


def linux_browser_apps_to_cmd(*apps: str) -> str:
    ignore_errors_cmd_part = ' 2>/dev/null' if os.getenv('WDM_LOG_LEVEL') == '0' else ''
    return ' || '.join(list(map(lambda i: f'{i} --version{ignore_errors_cmd_part}', apps)))


def os_name():
    pl = sys.platform
    if pl == "linux" or pl == "linux2":
        return OSType.LINUX
    elif pl == "darwin":
        return OSType.MAC
    elif pl == "win32":
        return OSType.WIN


def chrome_version(browser_type=ChromeType.GOOGLE):  # google-chrome
    pattern = r'\d+\.\d+\.\d+'

    cmd_mapping = {
        ChromeType.GOOGLE: {
            OSType.LINUX: linux_browser_apps_to_cmd('google-chrome', 'google-chrome-stable'),
            OSType.MAC: r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version',
            OSType.WIN: r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
        }

    }

    cmd = cmd_mapping[browser_type][os_name()]
    version = None
    with os.popen(cmd) as stream:
        stdout = stream.read()
        version = re.search(pattern, stdout)

    if not version:
        raise ValueError(f'Could not get version for Chrome with this command: {cmd}')
    current_version = version.group(0)
    return current_version
