
import sys
import os


driver = None
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from Utils.logging_utils import LoggingUtils
from datetime import datetime

# Set up logger once per session
logger = LoggingUtils.setup_logger(f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")


def pytest_runtest_setup(item):
    logger.info(f"Starting test: {item.name}")




def pytest_addoption(parser):
    parser.addoption("--browsername", action="store", default="chrome", help="browser selection")
    parser.addoption("--browser", action="store", default=None, help="browser selection alias for GitHub Actions")
    parser.addoption("--env", action="store", default="QA", help="Environment: QA or UAT")


@pytest.fixture(scope="function")
def browserInstance(request):
    global driver

    # Check --browser first (GitHub), then fallback to --browsername (Jenkins)
    browsername = request.config.getoption("--browser") or request.config.getoption("--browsername") or os.environ.get(
        'BROWSER') or "chrome"
    browsername = browsername.lower()

    is_github_actions = os.environ.get('GITHUB_ACTIONS') == 'true'

    if browsername == "chrome":
        options = ChromeOptions()
        if is_github_actions:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

    elif browsername == "firefox":
        options = FirefoxOptions()
        if is_github_actions:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

    elif browsername == "edge":
        options = EdgeOptions()
        if is_github_actions:
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Edge(options=options)

    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="function")
def base_urls(request):
    return request.config.getoption("--env")


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            clean_nodeid = report.nodeid.replace("tests/", "")

            screenshot_dir = "./reports/screenshots/"
            os.makedirs(screenshot_dir, exist_ok=True)

            file_name = os.path.join(screenshot_dir, clean_nodeid.replace("::", "_") + ".png")
            driver.get_screenshot_as_file(file_name)

            screenshot = driver.get_screenshot_as_base64()
            extra.append(pytest_html.extras.image(screenshot, ""))

        report.extra = extra


def screenshot(filename):
    driver.get_screenshot_as_file(filename)
