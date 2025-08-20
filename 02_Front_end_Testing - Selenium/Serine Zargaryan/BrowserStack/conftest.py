import pytest
import os
from pathlib import Path


def pytest_addoption(parser):
    """Add command-line options for pytest"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox", "edge"],
        help="Browser to run tests on (default: chrome)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--parallel",
        action="store",
        type=int,
        default=1,
        help="Number of parallel processes to run tests (default: 1)"
    )
    # Add --env option
    parser.addoption(
        "--env",
        action="store",
        default="browserstack",
        choices=["local", "browserstack"],
        help="Environment to run tests: local or browserstack (default: browserstack)"
    )


@pytest.fixture(scope="session")
def test_config(request):
    """Provide test configuration object"""
    return {
        "browser": request.config.getoption("--browser"),
        "headless": request.config.getoption("--headless"),
        "parallel": request.config.getoption("--parallel"),
        "env": request.config.getoption("--env"),  # ДОБАВЛЯЕМ env
        "base_url": "https://www.blueorigin.com",
        "timeout": 30,
        "implicit_wait": 10
    }



@pytest.fixture(scope="session")
def env(request):
    """Get the environment from command line argument"""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def test_environment(request):
    """Get test environment configuration"""
    env = request.config.getoption("--env")
    return {
        "environment": env,
        "is_browserstack": env.lower() == "browserstack",
        "is_local": env.lower() == "local"
    }


def pytest_configure(config):
    """Configure pytest with custom markers and setup"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "smoke: marks tests as smoke tests (critical functionality)"
    )
    config.addinivalue_line(
        "markers", "regression: marks tests as regression tests (full test suite)"
    )
    config.addinivalue_line(
        "markers", "negative: marks tests as negative test cases"
    )
    config.addinivalue_line(
        "markers", "positive: marks tests as positive test cases"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running (>30 seconds)"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    # Add browserstack marker
    config.addinivalue_line(
        "markers", "browserstack: marks tests that run on BrowserStack"
    )

    # Create test reports directory if it doesn't exist
    reports_dir = Path("test_reports")
    reports_dir.mkdir(exist_ok=True)

    # Set up logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(reports_dir / "test_execution.log"),
            logging.StreamHandler()
        ]
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names and organize tests"""
    # Get environment from command line argument
    env = config.getoption("--env")

    for item in items:
        # Add markers based on test file names
        if "negative" in item.nodeid.lower():
            item.add_marker(pytest.mark.negative)
        elif "positive" in item.nodeid.lower():
            item.add_marker(pytest.mark.positive)

        # Add markers based on test case IDs in test names
        test_name_lower = item.name.lower()
        if "tc_p_" in test_name_lower:
            item.add_marker(pytest.mark.positive)
        elif "tc_n_" in test_name_lower:
            item.add_marker(pytest.mark.negative)

        # Add markers based on environment
        if env.lower() == "browserstack":
            item.add_marker(pytest.mark.browserstack)

        # Add smoke test markers for critical test cases
        smoke_test_patterns = [
            "navigation", "search_functionality", "keyboard_accessibility"
        ]
        if any(pattern in test_name_lower for pattern in smoke_test_patterns):
            item.add_marker(pytest.mark.smoke)

        # Add slow marker for tests that might take longer
        slow_test_patterns = [
            "consistency", "javascript_disabled", "robustness"
        ]
        if any(pattern in test_name_lower for pattern in slow_test_patterns):
            item.add_marker(pytest.mark.slow)

        # Add integration marker for cross-system tests
        integration_patterns = [
            "mismatch", "comparison", "consistency"
        ]
        if any(pattern in test_name_lower for pattern in integration_patterns):
            item.add_marker(pytest.mark.integration)


def pytest_runtest_setup(item):
    """Run setup for each test item"""
    # Skip slow tests if running in smoke test mode
    if "smoke" in item.config.getoption("-m", default="") and item.get_closest_marker("slow"):
        pytest.skip("Skipping slow test in smoke test run")


def pytest_sessionstart(session):
    """Called after the Session object has been created"""
    # Get command-line options
    env = session.config.getoption("--env")
    browser = session.config.getoption("--browser")

    print("\n" + "=" * 80)
    print("BLUE ORIGIN CAREER WEBSITE AUTOMATION TEST SUITE")
    print("=" * 80)
    print(f"Environment: {env.upper()}")
    print(f"Browser: {browser.upper()}")
    print("Execution Mode: Direct Test Execution")
    print(f"Parallel processes: {session.config.getoption('--parallel')}")
    print("=" * 80 + "\n")


def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished"""
    print("\n" + "=" * 80)
    print("TEST EXECUTION COMPLETED")
    print(f"Exit status: {exitstatus}")
    print("=" * 80 + "\n")


def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "Blue Origin Career Website Test Report"


@pytest.fixture(autouse=True)
def test_environment_info(request):
    """Automatically capture test environment information"""
    test_info = {
        "test_name": request.node.name,
        "python_version": os.sys.version,
        "platform": os.name,
        "environment": request.config.getoption("--env"),  # add env
        "browser": request.config.getoption("--browser")
    }

    # Log test start
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Starting test: {test_info['test_name']} on {test_info['environment']}")

    yield test_info

    # Log test completion
    logger.info(f"Completed test: {test_info['test_name']}")


# Pytest hooks for better error handling
def pytest_runtest_makereport(item, call):
    """Customize test report generation"""
    if call.when == "call":
        # Add extra information to test reports
        item.user_properties.append(("browser", item.config.getoption("--browser")))
        item.user_properties.append(("environment", item.config.getoption("--env")))  # add env
        item.user_properties.append(("test_type", "automation"))


# Custom assertion helpers
def assert_url_contains(driver, expected_substring, timeout=10):
    """Custom assertion to check if URL contains expected substring"""
    from selenium.webdriver.support.ui import WebDriverWait

    def url_contains(driver):
        return expected_substring in driver.current_url

    try:
        WebDriverWait(driver, timeout).until(url_contains)
        return True
    except:
        current_url = driver.current_url
        raise AssertionError(
            f"Expected URL to contain '{expected_substring}', but got: '{current_url}'"
        )


# Add custom assertion to pytest namespace
pytest.assert_url_contains = assert_url_contains