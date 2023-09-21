from setuptools import setup, find_packages

setup(
    name='william_chromedriver_manager',
    version='0.0.2',
    description='根据Chrome浏览器版本下载对应的webdriver',
    author='ZhaoXi Feng',
    author_email='fengzx120@gmail.com',
    url='https://gitee.com/fengzx120/william-chrome-driver-manager',
    packages=find_packages(),
    install_requires=[
        'requests',
        'tqdm',
    ],
)
