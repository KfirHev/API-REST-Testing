import os
import time
from datetime import datetime
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

# Global driver instance
driver = None

# Set up logging for the test framework
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--browser_type", action="store", default="chrome", help="Specify the browser: chrome, firefox, or edge"
    )
    parser.addoption(
        "--run_env", action="store", default="local", help="Specify the environment: local or docker"
    )


# Browser Options

def setup_browser_options(browser, run_env):
    options = None
    if browser == "chrome":
        options = ChromeOptions()
        if run_env == "docker":
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
        else:
            #options.add_argument("--headless")
            options.add_argument("--start-maximized")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--disable-autofill")
            options.add_argument("--disable-autocomplete")
    elif browser == "firefox":
        options = FirefoxOptions()
        options.headless = run_env == "docker"
    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument("start-maximized")
        if run_env == "docker":
            options.add_argument("headless")
            options.add_argument("--disable-gpu")
    return options


@pytest.fixture(scope='class')
def setup_browser(request):

    # Check if the test has the "use_browser" marker (most of the tests are API)
    if 'use_browser' not in request.node.keywords:
        # If the test doesn't have the marker, skip browser initialization
        yield
        return

    browser_name = request.config.getoption('browser_type')
    run_env = request.config.getoption('run_env')
    driver = None

    # Local or Docker Run
    if run_env == 'local':
        print('Running LOCAL')
        if browser_name == 'chrome':
            service = ChromeService(r"browserdriver/chromedriver130.exe")
            driver = webdriver.Chrome(service=service, options=setup_browser_options(browser_name, run_env))
        elif browser_name == 'firefox':
            service = FirefoxService("C:/browserdriver/geckodriver.exe")
            driver = webdriver.Firefox(service=service, options=setup_browser_options(browser_name, run_env))
        elif browser_name == 'edge':
            service = EdgeService("C:/browserdriver/msedgedriver.exe")
            driver = webdriver.Edge(service=service, options=setup_browser_options(browser_name, run_env))
    elif run_env == 'docker':
        print('Running in DOCKER')
        if browser_name in ['chrome', 'firefox', 'edge']:
            driver = webdriver.Remote(
                command_executor="http://localhost:4444",
                options=setup_browser_options(browser_name, run_env)
            )
    else:
        raise ValueError("You should choose a browser between chrome, firefox, or edge")

    driver.implicitly_wait(4)
    driver.get("http://localhost:8090/parabank/")
    request.cls.driver = driver

    yield
    driver.quit()


def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_dir = 'Reports'
    os.makedirs(report_dir, exist_ok=True)
    report_filename = os.path.join(report_dir, f"Report_{timestamp}.html")
    config.option.htmlpath = report_filename


def _capture_screenshot(file_path):
    try:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        base, ext = os.path.splitext(file_path)
        index = 1
        while os.path.exists(file_path):
            file_path = f"{base}_{index}{ext}"
            index += 1

        driver.get_screenshot_as_file(file_path)
        logger.info(f"Screenshot saved to {file_path}")
    except Exception as e:
        logger.error(f"Error capturing screenshot: {e}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when in ['call', 'setup']:
        if report.failed or (report.skipped and hasattr(report, 'wasxfail')):
            file_name = report.nodeid.replace("::", "_") + ".png"
            file_path = os.path.join("Reports", "Screenshots", file_name)
            _capture_screenshot(file_path)

            if os.path.exists(file_path):
                html = (
                        '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" '
                        'onclick="window.open(this.src)" align="right"/></div>' % file_path
                )
                extra.append(pytest_html.extras.html(html))
            report.extra = extra
