import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from test_helpers import WebDriverFactory, BlueOriginHelpers, BlueOriginUrls, BlueOriginLocators


class TestBlueOriginPositive:
    """Positive test scenarios for Blue Origin career website"""

    # BrowserStack configuration
    BSTACK_USER = os.getenv("BSTACK_USER")
    BSTACK_KEY = os.getenv("BSTACK_KEY")
    BSTACK_URL = None
    if BSTACK_USER and BSTACK_KEY:
        BSTACK_URL = f"https://{BSTACK_USER}:{BSTACK_KEY}@hub-cloud.browserstack.com/wd/hub"

    # BrowserStack capabilities templates
    BSTACK_CAPABILITIES = {
        "chrome": {
            "browserName": "chrome",
            "browserVersion": "latest",
            "os": "Windows",
            "osVersion": "11"
        },
        "firefox": {
            "browserName": "firefox",
            "browserVersion": "latest",
            "os": "Windows",
            "osVersion": "11"
        },
        "edge": {
            "browserName": "MicrosoftEdge",
            "browserVersion": "latest",
            "os": "Windows",
            "osVersion": "11"
        }
    }
    # Common bstack:options for all browsers
    BSTACK_COMMON_OPTIONS = {
        "buildName": "browserstack-BlueOrigin-Positive-Tests-v2",
        "projectName": "Blue Origin Testing",
        "sessionName": "Generic Positive Test" # Will be overridden
    }

    @pytest.fixture(autouse=True)
    def setup_method(self, request):
        """Setup method executed before each test"""
        # Check if we should use BrowserStack (environment variable)
        use_browserstack = os.getenv('USE_BROWSERSTACK', 'false').lower() == 'true'

        # Get browser name from pytest parameter
        browser_name = getattr(request.node, 'callspec', None)
        if browser_name and hasattr(browser_name, 'params'):
            self.browser_name = browser_name.params.get('browser', 'chrome')
        else:
            self.browser_name = 'chrome'

        # Get test name for BrowserStack session naming
        test_name = request.node.name

        if use_browserstack:
            if not self.BSTACK_URL:
                pytest.skip("BrowserStack credentials (BSTACK_USER, BSTACK_KEY) are not set in environment variables.")
            else:
                self.driver = self._get_browserstack_driver(self.browser_name, test_name)
        else:
            self.driver = WebDriverFactory.get_driver(self.browser_name)

        self.helpers = BlueOriginHelpers(self.driver)
        yield
        # Teardown
        if hasattr(self, 'driver'):
            self.driver.quit()

    def _get_browserstack_driver(self, browser_name, test_name):
        """Create BrowserStack driver with specified browser"""
        if browser_name == 'chrome':
            options = webdriver.ChromeOptions()
        elif browser_name == 'firefox':
            options = webdriver.FirefoxOptions()
        elif browser_name == 'edge':
            options = webdriver.EdgeOptions()
        else:
            options = webdriver.ChromeOptions()  # Fallback to Chrome

        # Set browser-specific capabilities
        browser_caps = self.BSTACK_CAPABILITIES.get(browser_name, self.BSTACK_CAPABILITIES['chrome'])
        options.browser_version = browser_caps.get("browserVersion")
        options.platform_name = f'{browser_caps.get("os")} {browser_caps.get("osVersion")}'

        # Set BrowserStack options
        bstack_options = self.BSTACK_COMMON_OPTIONS.copy()
        bstack_options['sessionName'] = f"Positive Test: {test_name} - {browser_name}"
        options.set_capability('bstack:options', bstack_options)
        driver = webdriver.Remote(command_executor=self.BSTACK_URL, options=options)
        # Using explicit waits is a better practice than a global implicit wait.
        # driver.implicitly_wait(10)
        return driver

    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_tc_p_001_navigation_back_to_search(self, browser):
        """TC_P_001: Verify navigation back to original search system via job details page"""
        wait = WebDriverWait(self.driver, 20)  # Increased timeout for remote execution

        # Step 1: Open careers search page
        self.driver.get(BlueOriginUrls.CAREERS_SEARCH_URL)
        self.helpers.handle_cookie_consent()

        # Step 2: Click the first job listing with specific class
        # Wait for the job listing to be present and clickable
        first_job = wait.until(lambda d: self.helpers.find_first_job_listing())
        assert first_job is not None, "First job listing not found with any selector"

        self.helpers.click_element_safely(first_job)

        # Wait for the job details page to load by checking for the navigation button
        wait.until(EC.element_to_be_clickable(BlueOriginLocators.SEARCH_FOR_JOBS_BUTTON))

        # Step 3: Find and click "Search for Jobs" button
        navigation_success = self.helpers.navigate_to_search_jobs()
        assert navigation_success, "Search for Jobs button not found"

        # Step 4: Verify the redirected URL
        try:
            wait.until(EC.url_to_be(BlueOriginUrls.CAREERS_SEARCH_URL))
        except TimeoutException:
            # Let the assertion below provide a more detailed error message
            pass

        current_url = self.driver.current_url
        expected_url = BlueOriginUrls.CAREERS_SEARCH_URL
        assert current_url == expected_url, f"Expected exact URL {expected_url}, got: {current_url}"

    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_tc_p_002_keyword_search_functionality(self, browser):
        """TC_P_002: Verify keyword search functionality"""
        wait = WebDriverWait(self.driver, 20)

        # Step 1: Open careers search page
        self.driver.get(BlueOriginUrls.CAREERS_SEARCH_URL)
        self.helpers.handle_cookie_consent()

        # Step 2: Find the specific search input and enter "software"
        search_success = self.helpers.search_for_keyword("software")
        assert search_success, "Search input field not found"

        # Step 3: Check and save results count
        # Wait for the results count to appear
        wait.until(EC.presence_of_element_located(BlueOriginLocators.RESULTS_COUNT))
        results_count = self.helpers.get_search_results_count()
        assert results_count > 0, f"No search results found. Count: {results_count}"

        # Step 4: Check relevance of first 5 results
        relevant_count, job_listings = self.helpers.check_keyword_relevance_in_results("software", 5)
        assert relevant_count > 0, f"No 'software' keyword found in top 5 results. Relevant count: {relevant_count}"

    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_tc_p_003_search_results_consistency(self, browser):
        """TC_P_003: Verify consistency of search results across systems"""
        wait = WebDriverWait(self.driver, 20)

        # Step 1: Run the search to get a baseline count
        self.driver.get(BlueOriginUrls.CAREERS_SEARCH_URL)
        self.helpers.handle_cookie_consent()

        search_success = self.helpers.search_for_keyword("software")
        assert search_success, "Search input field not found"

        wait.until(EC.presence_of_element_located(BlueOriginLocators.RESULTS_COUNT))
        original_count = self.helpers.get_search_results_count()
        assert original_count > 0, f"No search results found. Count: {original_count}"

        # Step 2: Click on the first result to navigate away
        _, job_listings = self.helpers.check_keyword_relevance_in_results("software", 1)
        if job_listings:
            self.helpers.click_element_safely(job_listings[0])
        else:
            pytest.fail("Could not find a job listing to click.")

        # Step 3: Navigate back to the search page
        wait.until(EC.element_to_be_clickable(BlueOriginLocators.SEARCH_FOR_JOBS_BUTTON))
        navigation_success = self.helpers.navigate_to_search_jobs()
        assert navigation_success, "Neither Search for Jobs button nor logo link found"

        # Step 4: Perform the search again in the "new" system
        wait.until(EC.element_to_be_clickable(BlueOriginLocators.KEYWORD_SEARCH_INPUT))
        search_success = self.helpers.search_with_new_system("software")
        assert search_success, "Keyword search input not found"

        # Step 5: Get results count from the new system
        wait.until(EC.presence_of_element_located(BlueOriginLocators.JOB_FOUND_TEXT))
        new_results_count = self.helpers.get_new_system_results_count()
        assert new_results_count > 0, "Job found text element not found"

        # Step 6: Compare results
        print(f"Original search results count (TC_P_002): {original_count}")
        print(f"New search results count (TC_P_003): {new_results_count}")

        assert original_count == new_results_count, f"Results count mismatch: {original_count} vs {new_results_count}"

    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_tc_p_004_blue_origin_career_button_navigation(self, browser):
        """TC_P_004: Verify navigation behavior of "Blue Origin Career" logo button"""
        wait = WebDriverWait(self.driver, 20)

        # Step 1: Open careers search page
        self.driver.get(BlueOriginUrls.CAREERS_SEARCH_URL)

        # Handle cookie consent with improved error handling
        try:
            self.helpers.handle_cookie_consent()
        except Exception as e:
            print(f"Cookie consent handling failed, but continuing test: {e}")

        # Step 2: Locate the specific Blue Origin Career logo in header
        header_logo = wait.until(lambda d: self.helpers.find_header_logo())
        assert header_logo is not None, "Blue Origin Career header logo not found"

        # Step 3: Click the header logo
        current_url_before = self.driver.current_url
        self.helpers.click_element_safely(header_logo)

        # Wait for the URL to change
        try:
            wait.until_not(EC.url_to_be(current_url_before))
        except TimeoutException:
            pytest.fail("URL did not change after clicking the header logo.")

        # Step 4: Verify navigation behavior
        current_url_after = self.driver.current_url

        # The logo should navigate to the home page, not necessarily careers
        # It should navigate away from the /search page to a base URL.
        is_base_url = (current_url_after == BlueOriginUrls.BASE_URL or
                       current_url_after == BlueOriginUrls.BASE_URL + "/" or
                       current_url_after == BlueOriginUrls.CAREERS_URL)

        url_matches = is_base_url
        assert url_matches, f"Expected navigation to Blue Origin home page, got: {current_url_after}"

        # Verify URL changed from the search page
        assert current_url_after != current_url_before, f"URL did not change after clicking logo. Still on: {current_url_after}"

        # Ensure we're not on search page anymore
        assert "/search" not in current_url_after, f"Should not be on search page after clicking logo, got: {current_url_after}"

        # Step 5: Verify we're on a valid Blue Origin page
        content_found = self.helpers.verify_blue_origin_content()
        assert content_found, f"Blue Origin content not found on target page. URL: {current_url_after}, Page title: {self.driver.title}"

    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_tc_p_005_keyboard_accessibility(self, browser):
        """TC_P_005: Verify keyboard accessibility to job search"""
        wait = WebDriverWait(self.driver, 20)
        max_tabs = 15
        keyboard_tabs = 10

        # Step 1: Open careers page (no mouse use)
        self.driver.get(BlueOriginUrls.CAREERS_URL)
        self.helpers.handle_cookie_consent()
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # Step 2: Use Tab key to focus page elements and find "Search Jobs" link/button
        search_job_found = self.helpers.navigate_with_keyboard(max_tabs=max_tabs)
        assert search_job_found, "Search Jobs link not found via keyboard navigation"

        # Step 3: Press Enter to activate
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.RETURN).perform()

        # Step 4: Verify transition to job search page
        try:
            wait.until(EC.url_contains("search"))
        except TimeoutException:
            pytest.fail("URL did not navigate to a search page after pressing Enter.")

        current_url_after = self.driver.current_url
        assert "search" in current_url_after, f"Expected 'search' in URL, got: {current_url_after}"

        # Step 5: Confirm keyboard usability on new page
        search_input_found = self.helpers.find_search_input_with_keyboard(max_tabs=keyboard_tabs)
        assert search_input_found, "Search input field not accessible via keyboard"

        # Step 6: Test typing in search field
        actions.send_keys("test").perform()

        focused_element = self.driver.switch_to.active_element
        input_value = focused_element.get_attribute("value") or ""
        assert "test" in input_value.lower(), f"Keyboard input 'test' not found in search field. Actual value: '{input_value}'"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
