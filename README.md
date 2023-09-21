# William ChromeWebdriver Manager

![](https://img.shields.io/badge/python-%3E%3D3.7-brightgreen)
![](https://img.shields.io/badge/License-MIT-blue)
![](https://img.shields.io/badge/version-0.0.3-yellowgreen)

**Chrome115版本以后的webdriver chrome驱动自动下载**

**selenium4.11以后更新了官方自动下载驱动的方法，但速度感觉有点慢，此库可以用在selenium3.141.0版本之前的版本使用**

_Automatically download Chrome WebDriver for Chrome versions 115 and above._

_After Selenium 4.11, the official WebDriver provides an automatic download method. However, it may be relatively slow. This library can be used for versions prior to Selenium 3.141.0 to provide faster WebDriver downloads._

**安装 Installation:**
```bash
pip install william-chromedriver-manager
```
**使用 Usage:**
```python
from selenium import webdriver
from william_chromedriver_manager.core import get_local_webdriver_path

driver = webdriver.Chrome(executable_path=get_local_webdriver_path())
driver.get("https://www.baidu.com")
driver.close()
```
**get_local_webdriver_path方法会返回一个本地下载好的驱动路径，已经在mac intel芯片以及win10上测试。**

_The get_local_webdriver_path method will return the path to the locally downloaded WebDriver. It has been tested on Mac with Intel chips and Windows 10._

#### 打个广告
我在慕课网上有两门自动化测试课程，感兴趣的小伙伴可以看看

[Python+Requests零基础系统掌握接口自动化测试](https://coding.imooc.com/class/629.html)

[Selenium3+Pytest+Allure全流程实战自动化测试](https://coding.imooc.com/class/592.html)
