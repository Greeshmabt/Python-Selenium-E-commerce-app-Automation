import pytest
import sys
import os
from selenium import webdriver



driver= None
# Add current directory to Python path so pageObjects can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def pytest_addoption(parser):
    parser.addoption("--browsername", action="store", default="chrome", help="browser selection")
    parser.addoption("--env", action="store", default="QA", help="Environment: QA or UAT")

@pytest.fixture(scope="function")
def browserInstance(request):
    global driver      #this is using the global driver
    browsername= request.config.getoption("--browsername")
    if browsername== "chrome":
        driver = webdriver.Chrome()
        driver.maximize_window()
    elif browsername== "firefox":
        driver = webdriver.Firefox()
    elif browsername == "edge":
        driver = webdriver.Edge()

    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver    #returing driver, before test shopping function execution
    driver.close()  #executes after test function exceution

@pytest.fixture(scope="function")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="function")
def base_urls(request):
    env= request.config.getoption("--env")
    return env

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            clean_nodeid = report.nodeid.replace("tests/", "")
            file_name = ("./reports/screenshots/" + clean_nodeid.replace("::", "_") + ".png")
            driver.get_screenshot_as_file(file_name)
            screenshot = driver.get_screenshot_as_base64()
            extra.append(pytest_html.extras.image(screenshot, ""))
            # if file_name:
            #     html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
            #            'onclick="window.open(this.src)" align="right"/></div>' % file_name

        report.extra = extra

def screenshot(filename):
    driver.get_screenshot_as_file(filename)