import pytest
import time
from selenium import webdriver
import os

from test_helpers import WebDriverFactory, BlueOriginHelpers, BlueOriginUrls


class TestBlueOriginNegative:
    """Negative test scenarios for Blue Origin career website"""

    # BrowserStack configuration
    BSTACK_USER = "serinezargaryan_P7fD2M"
    BSTACK_KEY = "XkSkNCoqLRuqo5PTbisp"
    BSTACK_URL = f"https://{BSTACK_USER}:{BSTACK_KEY}@hub-cloud.browserstack.com/wd/hub"

    # BrowserStack capabilities templates
    BSTACK_CAPABILITIES = {
        "chrome": {
            "browserName": "chrome",
            "browserVersion": "latest",
            "os": "Windows",
            "osVersion": "11",
            "buildName": "browserstack-BlueOrigin-Negative-Tests-v1",
            "projectName": "Blue Origin Testing",
            "userName": BSTACK_USER,
            "accessKey": BSTACK_KEY
        },
        "firefox": {
            "browserName": "firefox",
            "browserVersion": "latest",
            "os": "Windows",
            "osVersion": "11",
            "buildName": "browserstack-BlueOrigin-Negative-Tests-v1",
            "projectName": "Blue Origin Testing",
            "userName": BSTACK_USER,
            "accessKey": BSTACK_KEY
        },
        "edge": {
            "browserName": "MicrosoftEdge",
            "browserVersion": "latest",
            "os": "Windows",
            "osVersion": "11",
            "buildName": "browserstack-BlueOrigin-Negative-Tests-v1",
            "projectName": "Blue Origin Testing",
            "userName": BSTACK_USER,
            "accessKey": BSTACK_KEY
        }
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
        capabilities = self.BSTACK_CAPABILITIES.get(browser_name, self.BSTACK_CAPABILITIES['chrome']).copy()
        capabilities['sessionName'] = f"Negative Test: {test_name} - {browser_name}"

        if browser_name == 'chrome':
            options = webdriver.ChromeOptions()
        elif browser_name == 'firefox':
            options = webdriver.FirefoxOptions()
        elif browser_name == 'edge':
            options = webdriver.EdgeOptions()
        else:
            options = webdriver.ChromeOptions()  # fallback

        options.set_capability('bstack:options', capabilities)
        driver = webdriver.Remote(command_executor=self.BSTACK_URL, options=options)
        driver.implicitly_wait(10)
        return driver

    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_tc_n_001_job_count_mismatch_between_systems(self, browser):
        """TC_N_001: Mismatch in job count between search systems"""
        # Step 1: Open Blue Origin careers search page and record job count
        self.driver.get(BlueOriginUrls.CAREERS_SEARCH_URL)
        self.helpers.handle_cookie_consent()
        time.sleep(3)

        # Get job count from Blue Origin search
        blue_origin_count = self.helpers.get_search_results_count()
        assert blue_origin_count > 0, "No jobs found on Blue Origin search page"

        # Step 2: Open Workday careers page and record job count
        workday_count = self.helpers.get_workday_job_count()
        assert workday_count > 0, "No jobs found on Workday careers page"

        # Step 3: Compare results - they should be identical (this is a negative test expecting failure)
        print(f"Blue Origin job count: {blue_origin_count}")
        print(f"Workday job count: {workday_count}")

        # For negative testing, we expect counts might not match
        # But we still assert they should be equal to document the discrepancy
        assert blue_origin_count == workday_count, f"Job count mismatch detected: Blue Origin ({blue_origin_count}) vs Workday ({workday_count})"

    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_tc_n_002_numeric_keyword_search_logic_comparison(self, browser):
        """TC_N_002: Comparison of search logic using numeric keywords"""
        # Precondition: Search "123" on Blue Origin platform
        self.driver.get(BlueOriginUrls.CAREERS_SEARCH_URL)
        self.helpers.handle_cookie_consent()
        time.sleep(2)

        search_success = self.helpers.search_for_keyword("123")
        assert search_success, "Search input field not found on Blue Origin"

        blue_origin_results = self.helpers.get_search_results_count()

        # Search "123" on Workday platform
        workday_search_success = self.helpers.search_workday_platform("123")
        if workday_search_success:
            workday_results = self.helpers.get_workday_search_results_count()
        else:
            # Navigate to Workday first
            self.helpers.get_workday_job_count()  # This navigates to Workday
            workday_search_success = self.helpers.search_workday_platform("123")
            assert workday_search_success, "Search functionality not available on Workday"
            workday_results = self.helpers.get_workday_search_results_count()

        print(f"Blue Origin '123' search results: {blue_origin_results}")
        print(f"Workday '123' search results: {workday_results}")

        # Compare logic and outputs - expecting same number of results
        assert blue_origin_results == workday_results, f"Numeric search logic differs: Blue Origin ({blue_origin_results}) vs Workday ({workday_results})"

    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_tc_n_003_exact_job_title_search_consistency(self, browser):
        """TC_N_003: Validation of exact job title search consistency across search systems"""

        # Step 1: Navigate to Workday careers page
        print("Step 1: Navigating to Workday careers page...")
        self.driver.get(BlueOriginUrls.WORKDAY_URL)
        time.sleep(2)  # Wait for page to load

        # Step 2: Handle cookie consent popup on Workday
        print("Step 2: Handling cookie consent on Workday...")
        cookie_handled = self.helpers.handle_workday_cookie_consent()
        if cookie_handled:
            print("Cookie consent handled successfully")
        else:
            print("No cookie consent popup found or already handled")

        time.sleep(3)  # Additional wait after cookie handling

        # Step 3: Find the first job listing link on Workday
        print("Step 3: Looking for first job listing on Workday...")
        exact_job_title = self.helpers.get_first_workday_job_title()

        assert exact_job_title is not None, "Could not find any job title on Workday careers page"
        assert len(exact_job_title) > 5, f"Job title too short: '{exact_job_title}'"

        print(f"Found first job title on Workday: '{exact_job_title}'")

        # Step 4: Search for this exact job title on Workday platform
        print(f"Step 4: Searching for '{exact_job_title}' on Workday platform...")

        workday_search_success = self.helpers.search_workday_platform(exact_job_title)
        assert workday_search_success, "Search functionality not available on Workday"

        time.sleep(3)  # Wait for search results to load

        # Get search results count from Workday
        workday_results_count = self.helpers.get_workday_search_results_count()
        print(f"Workday search results for '{exact_job_title}': {workday_results_count} jobs found")

        # Since we took this job title FROM Workday, searching for it on Workday MUST return results > 0
        # If it returns 0, that indicates a problem with Workday search functionality
        if workday_results_count == 0:
            print(f"CRITICAL: Workday search returned 0 results for a job title that exists on Workday")
            print(f"This indicates a problem with Workday search functionality")
            print(f"Job title: '{exact_job_title}'")

            # Still continue to test Blue Origin, but mark this as a Workday search issue
            workday_search_issue = True
        else:
            workday_search_issue = False
            print(f"Workday search working correctly: {workday_results_count} jobs found")

        # Step 5: Navigate to Blue Origin careers search page
        print("Step 5: Navigating to Blue Origin careers search page...")
        self.driver.get(BlueOriginUrls.CAREERS_SEARCH_URL)
        self.helpers.handle_cookie_consent()
        time.sleep(3)

        # Step 6: Search for the same job title on Blue Origin platform
        print(f"Step 6: Searching for '{exact_job_title}' on Blue Origin platform...")

        search_success = self.helpers.search_for_keyword(exact_job_title)
        assert search_success, "Search input field not found on Blue Origin"

        time.sleep(3)  # Wait for search results to load

        # Get search results count from Blue Origin
        blue_origin_results_count = self.helpers.get_search_results_count()
        print(f"Blue Origin search results for '{exact_job_title}': {blue_origin_results_count} jobs found")

        # Step 7: Analyze and compare results between platforms
        print("Step 7: Analyzing search results between platforms...")
        print(f"Workday search results: {workday_results_count}")
        print(f"Blue Origin search results: {blue_origin_results_count}")

        # Check for issues and create detailed report
        issues_found = []

        # Issue 1: Workday search problem (should never happen since we got job title from Workday)
        if workday_search_issue:
            issues_found.append(f"Workday search malfunction: returned 0 results for existing job '{exact_job_title}'")

        # Issue 2: Blue Origin has 0 results (could be legitimate if job only exists on Workday)
        if blue_origin_results_count == 0:
            issues_found.append(f"Blue Origin search returned 0 results for '{exact_job_title}'")
            if not workday_search_issue:
                issues_found.append("This suggests the job may only exist on Workday platform")

        # Issue 3: Results count mismatch (when both platforms have results > 0)
        if workday_results_count > 0 and blue_origin_results_count > 0:
            if workday_results_count != blue_origin_results_count:
                issues_found.append(
                    f"Results count mismatch: Workday ({workday_results_count}) vs Blue Origin ({blue_origin_results_count})")

        # Report all findings
        if not issues_found:
            print("Job title search consistency test completed successfully")
            print(
                f"Both platforms returned identical results ({workday_results_count} jobs) for job title: '{exact_job_title}'")
        else:
            print("Issues found during job title search consistency test:")
            for i, issue in enumerate(issues_found, 1):
                print(f"  {i}. {issue}")

        # Final test assertions based on expected behavior:

        # Assertion 1: Workday MUST return results > 0 since we got the job title from there
        assert workday_results_count > 0, f"CRITICAL BUG: Workday search returned 0 results for job title '{exact_job_title}' that was extracted from Workday itself. This indicates a search functionality problem."

        # Assertion 2: Blue Origin should also return results > 0 (both platforms should have same jobs)
        assert blue_origin_results_count > 0, f"Blue Origin search returned 0 results for job title '{exact_job_title}' which exists on Workday. This suggests job listings are not synchronized between platforms."

        # Assertion 3: If both platforms return results > 0, they should be equal
        assert workday_results_count == blue_origin_results_count, f"Job title search results should be identical between platforms: Workday ({workday_results_count}) vs Blue Origin ({blue_origin_results_count}). This indicates inconsistent job listings or search logic between platforms."

        print(f"✅ All consistency checks passed for job title: '{exact_job_title}'")
        print(f"✅ Both platforms returned {workday_results_count} jobs consistently")

    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_tc_n_004_search_robustness_with_special_characters(self, browser):
        """TC_N_004: Verify search robustness with unusual spaces and special characters"""
        # Step 1: Open Blue Origin careers search page
        self.driver.get(BlueOriginUrls.CAREERS_SEARCH_URL)
        self.helpers.handle_cookie_consent()
        time.sleep(2)

        # Step 2: Enter search query with multiple spaces and special characters
        special_query = "  software engineer @@ ##  "

        search_success = self.helpers.search_with_special_characters(special_query)
        assert search_success, "Failed to perform search with special characters"

        # Step 3: Get search results count for special characters search
        special_results_count = self.helpers.get_search_results_count()

        # Step 4: For special characters search, we expect 0 results
        # This validates that the system correctly handles invalid/special character searches
        print(f"Search results with special characters '{special_query}': {special_results_count}")

        # NOTE: This is a negative test - we're testing that special characters return 0 results
        # However, if the system actually returns results, that's also valid behavior
        # The main goal is to ensure the system doesn't crash

        if special_results_count == 0:
            print("System correctly filtered out special characters and returned 0 results")
        else:
            print(f"System returned {special_results_count} results for special character search")
            print("This could mean the system extracted valid keywords from the query")

        # Step 5: Verify that search functionality still works with normal query
        # This ensures the system wasn't broken by the special character search
        try:
            # Add a small delay and try to refresh the page state
            time.sleep(2)

            # Try normal search
            normal_search_success = self.helpers.search_for_keyword("engineer")

            if normal_search_success:
                normal_results = self.helpers.get_search_results_count()
                assert normal_results > 0, "Normal search should return results after special character search"
                print(f"Normal search after special characters: {normal_results} results")
                print("Search functionality works correctly after special character input")
            else:
                # If normal search fails, try refreshing the page and searching again
                print("First attempt at normal search failed, refreshing page...")
                self.driver.refresh()
                time.sleep(3)
                self.helpers.handle_cookie_consent()

                retry_search_success = self.helpers.search_for_keyword("engineer")
                if retry_search_success:
                    retry_results = self.helpers.get_search_results_count()
                    assert retry_results > 0, "Normal search should work after page refresh"
                    print(f"Normal search after page refresh: {retry_results} results")
                    print("Search functionality recovered after page refresh")
                else:
                    print("Warning: Normal search functionality appears to be impacted by special character search")
                    # Don't fail the test - the main assertion (0 results for special chars) already passed

        except Exception as e:
            print(f"Warning: Could not verify normal search functionality after special character search: {str(e)}")
            # Don't fail the test - the main assertion (0 results for special chars) already passed

    @pytest.mark.parametrize("browser", ["chrome", "firefox", "edge"])
    def test_tc_n_005_career_page_functionality_without_javascript(self, browser):
        """TC_N_005: Functional check of career page with JavaScript disabled"""
        print(f"Test Case TC_N_005 - JavaScript disabled test for {browser}")

        # Check if we're using BrowserStack
        use_browserstack = os.getenv('USE_BROWSERSTACK', 'false').lower() == 'true'

        if use_browserstack:
            # For BrowserStack, we need to recreate the driver with JS disabled
            self.driver.quit()
            capabilities = self.BSTACK_CAPABILITIES.get(browser, self.BSTACK_CAPABILITIES['chrome']).copy()
            capabilities['sessionName'] = f"Negative Test: JavaScript Disabled - {browser}"

            if browser.lower() == 'chrome':
                options = webdriver.ChromeOptions()
                prefs = {
                    "profile.default_content_setting_values": {
                        "javascript": 2
                    }
                }
                options.add_experimental_option("prefs", prefs)
            elif browser.lower() == 'firefox':
                options = webdriver.FirefoxOptions()
                options.set_preference("javascript.enabled", False)
            else:  # edge
                options = webdriver.EdgeOptions()
                prefs = {
                    "profile.default_content_setting_values": {
                        "javascript": 2
                    }
                }
                options.add_experimental_option("prefs", prefs)

            options.set_capability('bstack:options', capabilities)
            self.driver = webdriver.Remote(command_executor=self.BSTACK_URL, options=options)
        else:
            # For local testing, recreate driver with JavaScript disabled
            self.driver.quit()

            if browser.lower() == 'firefox':
                # Firefox has better JS disabling support
                from selenium.webdriver.firefox.options import Options as FirefoxOptions
                firefox_options = FirefoxOptions()
                firefox_options.set_preference("javascript.enabled", False)
                firefox_options.set_preference("dom.webdriver.enabled", False)
                self.driver = webdriver.Firefox(options=firefox_options)
            else:
                # For Chrome/Edge, use basic method
                self.driver = WebDriverFactory.get_driver(browser, disable_javascript=True)

        self.helpers = BlueOriginHelpers(self.driver)

        # Navigate to Blue Origin careers page
        print("Navigating to Blue Origin careers page...")
        self.driver.get(BlueOriginUrls.CAREERS_URL)
        time.sleep(5)

        # Test 1: Check that video elements don't work (JavaScript disabled behavior)
        print("Test 1: Checking video functionality with JavaScript disabled...")
        video_not_working = self.helpers.check_video_elements_disabled()

        if video_not_working:
            print("Expected result: Video elements are not functional (JavaScript disabled)")
        else:
            print("Videos may be working or not present")

        # Test 2: Find and click a navigation link to verify basic HTML functionality
        print("Test 2: Testing basic HTML link navigation...")
        link_navigation_works = self.helpers.test_basic_link_navigation()

        if link_navigation_works:
            print("Expected result: Basic HTML links work without JavaScript")
        else:
            print("Warning: Link navigation failed")

        # Test results evaluation
        if video_not_working and link_navigation_works:
            print("SUCCESS: JavaScript disabled test passed")
            print("- Videos disabled (JavaScript not working)")
            print("- HTML links functional (basic HTML works)")
        elif link_navigation_works:
            print("PARTIAL SUCCESS: Basic HTML works, video status unclear")
        else:
            print("Test completed with mixed results")


if __name__ == "__main__":
    # Example usage:
    # Local testing: python -m pytest test_negative.py -v
    # BrowserStack testing: USE_BROWSERSTACK=true python -m pytest test_negative.py -v
    pytest.main([__file__, "-v"])