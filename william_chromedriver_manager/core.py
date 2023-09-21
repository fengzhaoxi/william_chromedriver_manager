#! /usr/bin/python3
# coding=utf-8
# @Time: 2023/9/20 10:02
# @Author: Feng Zhaoxi

import os
import platform
import zipfile
import shutil

import requests
from tqdm import tqdm

from .get_chrome_version import chrome_version
from .logger import log


def sep(path, add_sep_before=False, add_sep_after=False):
    all_path = os.sep.join(path)
    if add_sep_before:
        all_path = os.sep + all_path
    if add_sep_after:
        all_path = all_path + os.sep
    return all_path


def get_platform_and_bit():
    operating_system = platform.system()
    architecture = platform.architecture()[0]

    if operating_system == "Linux":
        return "linux64"
    elif operating_system == "Darwin":
        processor = platform.processor()
        if 'arm' in processor.lower():
            return "mac-arm64"
        else:
            return "mac-x64"
    elif operating_system == "Windows":
        if architecture == "64bit":
            return "win64"
        else:
            return "win32"


def webdriver_url():
    res = requests.get("https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json")
    versions = res.json()["versions"]
    local_version = chrome_version()
    match_version = next(
        (version["downloads"]["chromedriver"] for version in versions if local_version in version["version"]), None)
    platform_name = get_platform_and_bit()
    return next((chromedriver["url"] for chromedriver in match_version if chromedriver["platform"] == platform_name),
                None)


def unzip_driver_zip_package(extract_path, zip_file_path):
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            filename = os.path.basename(member)
            if not filename:
                continue

            # 构建解压后的文件路径
            target_path = os.path.join(extract_path, filename)

            # 解压文件到目标路径
            with zip_ref.open(member) as source, open(target_path, "wb") as target:
                shutil.copyfileobj(source, target)
            if "win" not in get_platform_and_bit():
                os.chmod(target_path, 0o755)


def chromedriver_executable_path(extract_path):
    if "win" in get_platform_and_bit():
        return sep([extract_path, "chromedriver.exe"])
    else:
        return sep([extract_path, "chromedriver"])


def local_webdriver_path():
    driver_dir = os.path.expanduser("~/.cdm")
    driver_dir = driver_dir + sep([get_platform_and_bit(), chrome_version()], add_sep_before=True)
    driver_file_path = driver_dir + sep([chrome_version() + "_" + get_platform_and_bit() + ".zip"], add_sep_before=True)
    return driver_dir, driver_file_path


def download_driver_to_cache():
    url = webdriver_url()
    driver_dir, driver_file_path = local_webdriver_path()
    os.makedirs(driver_dir, exist_ok=True)
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("Content-Length", 0))
    progress_bar = tqdm(total=total_size, unit="B", unit_scale=True, ncols=80)
    if response.status_code == 200:
        with open(driver_file_path, "wb") as file:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
                progress_bar.update(len(data))
        progress_bar.close()
        log("下载完成")
        unzip_driver_zip_package(driver_dir, driver_file_path)
    else:
        log("驱动下载失败")


def get_local_webdriver_path():
    log("========= william ChromeDriverManager =========")
    current_chrome_version = chrome_version()
    log("当前Chrome的版本为:" + str(current_chrome_version) + ",将根据您浏览器的版本下载对应的webdriver")
    driver_dir, driver_file_path = local_webdriver_path()
    if os.path.exists(driver_file_path):
        log(f"webdriver驱动已存在，Chrome版本{chrome_version()}，压缩包存放路径{driver_file_path}")
    else:
        download_driver_to_cache()
    return chromedriver_executable_path(driver_dir)


if __name__ == '__main__':
    get_local_webdriver_path()
