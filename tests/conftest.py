from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
driver = None


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome")
    parser.addoption("--env", action='store', default="env")


def pytest_configure(config):
    # set custom options only if none are provided from command line
    if not config.option.htmlpath:
        now = datetime.now()
        # create report target dir
        reports_dir = Path('folder/Path', now.strftime('%Y%m%d'))
        reports_dir.mkdir(parents=True, exist_ok=True)
        # custom report file
        report = reports_dir / f"report_{now.strftime('%H%M%S')}.html"
        # adjust plugin options
        config.option.htmlpath = report
        config.option.self_contained_html = True


@pytest.fixture(scope="class")
def browser_setup(request):
    global driver
    browser_name = request.config.getoption("browser_name")
    env = request.config.getoption("env")

    if browser_name == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--ignore-certificate-errors")
        driver = webdriver.Chrome(executable_path="exe/path", options=chrome_options)
        env_setup(env)

    elif browser_name == "firefox":
        driver = webdriver.Firefox(executable_path="exe/path")
        driver.maximize_window()
        env_setup(env)

    elif browser_name == "IE":
        driver = webdriver.Ie(executable_path="")
        driver.maximize_window()
        env_setup(env)

    request.cls.driver = driver
    yield
    driver.close()


def env_setup(env):
    if env == "test1":
        driver.get("environment1")

    elif env == "test2":
        driver.get("environment2")

    elif env == "test3":
        driver.get("environment3")


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
            loc = "Screenshot/path"
            now = datetime.now()
            file_name1 = now.strftime('_%m%d%Y--%H-%M-%S.png')

            file_name = loc + report.nodeid.replace("::", "_") + file_name1
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
        driver.get_screenshot_as_file(name)
