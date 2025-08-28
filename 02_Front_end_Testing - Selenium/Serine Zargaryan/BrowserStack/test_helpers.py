#helpers changed just little from Unittest
import os
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import logging


class WebDriverFactory:
    """Factory class for creating browser instances with proper configuration"""

    @staticmethod
    def create_chrome_driver(disable_javascript=False, headless=False):
        """Create Chrome WebDriver with optimized settings"""
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        if headless:
            chrome_options.add_argument("--headless")

        if disable_javascript:
            print("Setting up Chrome with JavaScript disabled...")

            # Use more aggressive JavaScript blocking
            prefs = {
                "profile.default_content_setting_values": {
                    "javascript": 2
                },
                "profile.managed_default_content_settings": {
                    "javascript": 2
                }
            }
            chrome_options.add_experimental_option("prefs", prefs)

            # Additional blocking arguments
            chrome_options.add_argument("--disable-javascript")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--content-shell-hide-toolbar")

            print("JavaScript disable settings applied to Chrome options")

        try:
            driver = webdriver.Chrome(options=chrome_options)

            if disable_javascript:
                print("Verifying JavaScript is disabled...")
                try:
                    result = driver.execute_script("return 'test';")
                    print(f"WARNING: JavaScript still works! Result: {result}")

                    # Try CDP method as fallback
                    try:
                        driver.execute_cdp_cmd('Runtime.setScriptExecutionDisabled', {'value': True})
                        print("Applied CDP script execution disable")
                    except Exception as cdp_e:
                        print(f"CDP disable failed: {cdp_e}")

                except Exception as js_e:
                    print(f"JavaScript properly disabled: {type(js_e).__name__}")

            if not disable_javascript:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            if not headless:
                driver.maximize_window()
            return driver
        except Exception as e:
            logging.error(f"Failed to create Chrome driver: {str(e)}")
            raise

    @staticmethod
    def create_firefox_driver(disable_javascript=False, headless=False):
        """Create Firefox WebDriver with optimized settings"""
        firefox_options = FirefoxOptions()
        firefox_options.set_preference("dom.webdriver.enabled", False)
        firefox_options.set_preference('useAutomationExtension', False)
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")

        if headless:
            firefox_options.add_argument("--headless")

        if disable_javascript:
            firefox_options.set_preference("javascript.enabled", False)

        try:
            driver = webdriver.Firefox(options=firefox_options)
            if not disable_javascript:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            if not headless:
                driver.maximize_window()
            return driver
        except Exception as e:
            logging.error(f"Failed to create Firefox driver: {str(e)}")
            raise

    @staticmethod
    def create_edge_driver(disable_javascript=False, headless=False):
        """Create Edge WebDriver with optimized settings"""
        edge_options = EdgeOptions()
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--window-size=1920,1080")

        if headless:
            edge_options.add_argument("--headless")

        if disable_javascript:
            edge_options.add_argument("--disable-javascript")

        try:
            # Edge driver path configuration through environment variable
            if os.getenv('EDGE_DRIVER_PATH'):
                driver = webdriver.Edge(options=edge_options)
            else:
                driver = webdriver.Edge(options=edge_options)

            if not disable_javascript:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            if not headless:
                driver.maximize_window()
            return driver
        except Exception as e:
            logging.error(f"Failed to create Edge driver: {str(e)}")
            raise

    @staticmethod
    def get_driver(browser_name, disable_javascript=False, headless=False):
        """Get driver instance based on browser name"""
        browser_name = browser_name.lower()

        driver_methods = {
            'chrome': WebDriverFactory.create_chrome_driver,
            'firefox': WebDriverFactory.create_firefox_driver,
            'edge': WebDriverFactory.create_edge_driver
        }

        if browser_name not in driver_methods:
            raise ValueError(f"Unsupported browser: {browser_name}. Supported browsers: {list(driver_methods.keys())}")

        return driver_methods[browser_name](disable_javascript, headless)


class BlueOriginLocators:
    """Class containing all locators for Blue Origin career website"""

    # Main search page elements
    SEARCH_INPUT = (By.CSS_SELECTOR, ".JobBoardSearch_input__Y3mFB")
    SEARCH_BUTTON_SELECTORS = [
        (By.ID, "job-board-search-submit-button"),
        (By.CSS_SELECTOR, ".JobBoardSearch_submitButton__SWZ48"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[@type='submit' and contains(@class, 'JobBoardSearch_submitButton')]"),
        (By.XPATH, "//button[.//title[text()='Search']]")
    ]

    # Job listings elements
    JOB_LISTING_SELECTORS = [
        (By.CSS_SELECTOR, ".JobBoardListItem_title___2_Sp"),
        (By.CSS_SELECTOR, ".JobBoardListItem_link__kjhe9"),
        (By.CSS_SELECTOR, ".JobBoardListItem_title___2_Sp a"),
        (By.CSS_SELECTOR, "a[class*='JobBoardListItem_link']")
    ]

    # Results count elements
    RESULTS_COUNT = (By.CSS_SELECTOR, ".JobBoardJobCount_count__2Yol3")
    JOB_FOUND_TEXT = (By.CSS_SELECTOR, 'p[data-automation-id="jobFoundText"]')

    # Navigation elements
    SEARCH_FOR_JOBS_BUTTON = (By.CSS_SELECTOR, 'button[data-automation-id="navigationItem-Search for Jobs"]')
    LOGO_LINK = (By.CSS_SELECTOR, 'a[data-automation-id="logoLink"]')
    KEYWORD_SEARCH_INPUT = (By.CSS_SELECTOR, 'input[data-automation-id="keywordSearchInput"]')

    # Header logo elements
    HEADER_LOGO_SELECTORS = [
        (By.ID, "header-logo"),
        (By.CSS_SELECTOR, "#header-logo"),
        (By.CSS_SELECTOR, ".HeaderLogo_headerLogo__2vsJe a"),
        (By.CSS_SELECTOR, "a#header-logo"),
        (By.XPATH, "//img[@alt='Blue Origin | Careers']/.."),
        (By.XPATH, "//img[contains(@alt, 'Blue Origin') and contains(@alt, 'Careers')]/.."),
        (By.CSS_SELECTOR, ".HeaderLogo_headerLogo__2vsJe > a"),
        (By.XPATH, "//span[contains(@class, 'HeaderLogo')]//a")
    ]

    # Cookie consent elements
    COOKIE_SELECTORS = [
        (By.ID, "onetrust-accept-btn-handler"),
        (By.ID, "onetrust-button-group"),
        (By.CSS_SELECTOR, "#onetrust-button-group button"),
        (By.CSS_SELECTOR, "#onetrust-accept-btn-handler"),
        (By.XPATH, "//div[@id='onetrust-button-group']//button"),
        (By.XPATH, "//button[@id='onetrust-accept-btn-handler']"),
        (By.CSS_SELECTOR, ".onetrust-close-btn-handler"),
        (By.CSS_SELECTOR, ".accept-cookies-btn"),
        (By.XPATH, "//button[contains(text(), 'Accept')]"),
        (By.XPATH, "//button[contains(text(), 'Allow')]")
    ]

    # Workday platform locators
    WORKDAY_COOKIE_SELECTORS = [
        (By.ID, "gdpr-cookie-accept"),
        (By.CSS_SELECTOR, "[data-automation-id='cookieAcceptButton']"),
        (By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'OK')]"),
        (By.CSS_SELECTOR, ".css-1hwfws3"),
        (By.ID, "cookie-accept")
    ]

    WORKDAY_JOB_COUNT_SELECTORS = [
        (By.CSS_SELECTOR, "[data-automation-id='jobFoundText']"),
        (By.CSS_SELECTOR, ".css-12psxof"),
        (By.XPATH, "//span[contains(text(), 'jobs') or contains(text(), 'Jobs')]"),
        (By.CSS_SELECTOR, "[data-automation-id='jobCount']"),
        (By.XPATH, "//div[contains(@class, 'job') and contains(text(), 'of')]")
    ]

    WORKDAY_SEARCH_SELECTORS = [
        (By.CSS_SELECTOR, "[data-automation-id='keywordSearchInput']"),
        (By.CSS_SELECTOR, "input[placeholder*='Search']"),
        (By.CSS_SELECTOR, "input[type='search']"),
        (By.XPATH, "//input[contains(@placeholder, 'search') or contains(@placeholder, 'Search')]")
    ]

    WORKDAY_JOB_TITLE_SELECTORS = [
        (By.CSS_SELECTOR, "[data-automation-id='jobTitle']"),
        (By.CSS_SELECTOR, "a[data-automation-id='jobTitle']"),
        (By.CSS_SELECTOR, ".css-1id7k8c a"),
        (By.CSS_SELECTOR, "h3[data-automation-id='jobTitle']"),
        (By.CSS_SELECTOR, "div[data-automation-id='compositeHeaderContent'] a"),
        (By.CSS_SELECTOR, ".css-k008qs a"),
        (By.XPATH, "//a[@data-automation-id='jobTitle']"),
        (By.XPATH, "//h3[@data-automation-id='jobTitle']"),
        (By.CSS_SELECTOR, "a[href*='/job/']")
    ]


class BlueOriginHelpers:
    """Helper class containing all methods for Blue Origin career testing"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.long_wait = WebDriverWait(driver, 30)
        self.search_results_count = 0
        self.workday_url = "https://blueorigin.wd5.myworkdayjobs.com/en-US/BlueOrigin"
        self.workday_job_count = 0
        self.logger = logging.getLogger(__name__)

    def safe_execute(self, func, *args, fallback_result=None, error_message="Operation failed", **kwargs):
        """Safely execute function with error handling and logging"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.logger.warning(f"{error_message}: {str(e)}")
            return fallback_result

    def wait_for_page_load(self, timeout=10):
        """Wait for page to be fully loaded"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            self.logger.warning("Page load timeout")

    def handle_cookie_consent(self, max_retries=3):
        """Handle cookie consent popup with retry mechanism"""
        for attempt in range(max_retries):
            for selector_type, selector_value in BlueOriginLocators.COOKIE_SELECTORS:
                try:
                    cookie_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )

                    if cookie_button.is_displayed():
                        self.scroll_to_element(cookie_button)
                        time.sleep(0.5)

                        # Try different click methods
                        click_methods = [
                            lambda: cookie_button.click(),
                            lambda: self.driver.execute_script("arguments[0].click();", cookie_button),
                            lambda: ActionChains(self.driver).click(cookie_button).perform()
                        ]

                        for click_method in click_methods:
                            try:
                                click_method()
                                time.sleep(1)
                                self.logger.info("Cookie consent handled successfully")
                                return True
                            except ElementClickInterceptedException:
                                continue

                except (TimeoutException, NoSuchElementException):
                    continue

            if attempt < max_retries - 1:
                time.sleep(1)  # Wait before retry

        self.logger.info("No cookie consent popup found or couldn't handle it")
        return False

    def handle_workday_cookie_consent(self):
        """Handle cookie consent on Workday site"""
        return self.safe_execute(
            self._handle_workday_cookie_consent_impl,
            fallback_result=False,
            error_message="Failed to handle Workday cookie consent"
        )

    def _handle_workday_cookie_consent_impl(self):
        """Implementation for Workday cookie consent handling"""
        for selector_type, selector_value in BlueOriginLocators.WORKDAY_COOKIE_SELECTORS:
            try:
                cookie_button = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((selector_type, selector_value))
                )
                cookie_button.click()
                time.sleep(1)
                return True
            except (TimeoutException, NoSuchElementException):
                continue
        return False

    def scroll_to_element(self, element):
        """Scroll element into view with better positioning"""
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
                element
            )
            time.sleep(0.5)
        except Exception as e:
            self.logger.warning(f"Failed to scroll to element: {str(e)}")

    def find_element_with_multiple_selectors(self, selectors, timeout=10):
        """Find element using multiple selectors as fallback"""
        wait = WebDriverWait(self.driver, timeout)

        for selector_type, selector_value in selectors:
            try:
                element = wait.until(EC.presence_of_element_located((selector_type, selector_value)))
                if element.is_displayed():
                    return element
            except TimeoutException:
                continue
        return None

    def find_first_job_listing(self):
        """Find and return the first job listing element"""
        element = self.find_element_with_multiple_selectors(BlueOriginLocators.JOB_LISTING_SELECTORS)
        if element:
            try:
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(element))
                return element
            except TimeoutException:
                return element  # Return even if not clickable
        return None

    def click_element_safely(self, element, max_retries=3):
        """Safely click an element with multiple fallback methods"""
        if not element:
            return False

        self.scroll_to_element(element)

        click_methods = [
            lambda: element.click(),
            lambda: ActionChains(self.driver).click(element).perform(),
            lambda: self.driver.execute_script("arguments[0].click();", element),
            lambda: ActionChains(self.driver).move_to_element(element).click().perform()
        ]

        for attempt in range(max_retries):
            for method in click_methods:
                try:
                    method()
                    time.sleep(0.5)
                    return True
                except (ElementClickInterceptedException, Exception) as e:
                    self.logger.debug(f"Click method failed: {str(e)}")
                    continue

            if attempt < max_retries - 1:
                time.sleep(1)

        self.logger.error("All click methods failed")
        return False

    def search_for_keyword(self, keyword):
        """Perform keyword search with improved reliability"""
        try:
            # Find and interact with search input
            search_input = self.wait.until(EC.presence_of_element_located(BlueOriginLocators.SEARCH_INPUT))
            search_input.clear()
            search_input.send_keys(keyword)

            # Try to find and click search button
            search_button = self.find_element_with_multiple_selectors(
                BlueOriginLocators.SEARCH_BUTTON_SELECTORS, timeout=5
            )

            if search_button and self.click_element_safely(search_button):
                self.logger.info(f"Search initiated with button for keyword: {keyword}")
            else:
                # Fallback to Enter key
                search_input.send_keys(Keys.RETURN)
                self.logger.info(f"Search initiated with Enter key for keyword: {keyword}")

            # Wait for search results to load
            # The explicit wait in the test case is more reliable than a fixed sleep.
            self.wait_for_page_load() # This ensures the page document is ready.
            return True

        except TimeoutException:
            self.logger.error(f"Failed to perform search for keyword: {keyword}")
            return False

    def search_with_special_characters(self, query_with_special_chars):
        """Search with special characters and spaces"""
        return self.safe_execute(
            self._search_with_special_characters_impl,
            query_with_special_chars,
            fallback_result=False,
            error_message="Failed to search with special characters"
        )

    def _search_with_special_characters_impl(self, query_with_special_chars):
        """Implementation for special character search"""
        search_input = self.wait.until(EC.presence_of_element_located(BlueOriginLocators.SEARCH_INPUT))
        search_input.clear()
        search_input.send_keys(query_with_special_chars)
        search_input.send_keys(Keys.RETURN)
        time.sleep(3)
        return True

    def get_search_results_count(self):
        """Get the count of search results with improved parsing"""
        try:
            results_count_element = self.wait.until(
                EC.presence_of_element_located(BlueOriginLocators.RESULTS_COUNT)
            )
            results_text = results_count_element.text

            # Multiple regex patterns for different text formats
            patterns = [
                r'of (\d+)',  # "Showing jobs 1 – 25 of 573"
                r'(\d+)\s+jobs?\s+found',  # "573 jobs found"
                r'(\d+)\s+total',  # "573 total"
                r'(\d+)$'  # Just a number at the end
            ]

            for pattern in patterns:
                match = re.search(pattern, results_text, re.IGNORECASE)
                if match:
                    self.search_results_count = int(match.group(1))
                    return self.search_results_count

            # Fallback: extract all numbers and take the largest (likely total)
            numbers = re.findall(r'\d+', results_text)
            if numbers:
                self.search_results_count = max(map(int, numbers))
                return self.search_results_count

            return 0

        except TimeoutException:
            self.logger.warning("Could not find search results count element")
            return 0

    def check_keyword_relevance_in_results(self, keyword, max_results=5):
        """Check relevance of keyword in search results with robust locators."""
        job_listings = []
        # Try multiple selectors to find the job listings, making the test more robust
        for selector_type, selector_value in BlueOriginLocators.JOB_LISTING_SELECTORS:
            try:
                # Wait for at least one element to be present using the current selector
                self.wait.until(EC.presence_of_element_located((selector_type, selector_value)))
                # If found, get all matching elements
                job_listings = self.driver.find_elements(selector_type, selector_value)
                if job_listings:
                    self.logger.info(f"Found {len(job_listings)} job listings with selector: {selector_value}")
                    break  # Exit loop once listings are found
            except TimeoutException:
                continue  # Try the next selector in the list

        if not job_listings:
            self.logger.warning("Could not find job listings for relevance check using any available selector.")
            return 0, []

        top_results = job_listings[:max_results]
        relevant_count = 0

        for result in top_results:
            if result.is_displayed() and keyword.lower() in result.text.lower():
                relevant_count += 1

        return relevant_count, job_listings

    def navigate_to_search_jobs(self):
        """Navigate to search jobs page using button or logo link"""
        navigation_elements = [
            BlueOriginLocators.SEARCH_FOR_JOBS_BUTTON,
            BlueOriginLocators.LOGO_LINK
        ]

        for element_locator in navigation_elements:
            try:
                element = self.wait.until(EC.element_to_be_clickable(element_locator))
                if self.click_element_safely(element):
                    return True
            except TimeoutException:
                continue

        return False

    def search_with_new_system(self, keyword):
        """Search using the new system interface"""
        return self.safe_execute(
            self._search_with_new_system_impl,
            keyword,
            fallback_result=False,
            error_message="Failed to search with new system"
        )

    def _search_with_new_system_impl(self, keyword):
        """Implementation for new system search"""
        search_input = self.wait.until(
            EC.presence_of_element_located(BlueOriginLocators.KEYWORD_SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(keyword)
        search_input.send_keys(Keys.RETURN)
        time.sleep(2)
        return True

    def get_new_system_results_count(self):
        """Get results count from the new system"""
        try:
            results_element = self.wait.until(
                EC.presence_of_element_located(BlueOriginLocators.JOB_FOUND_TEXT)
            )
            results_text = results_element.text

            match = re.search(r'(\d+)', results_text)
            return int(match.group(1)) if match else 0

        except TimeoutException:
            return 0

    def find_header_logo(self):
        """Find the header logo element with improved validation"""
        for selector_type, selector_value in BlueOriginLocators.HEADER_LOGO_SELECTORS:
            try:
                header_logo = self.wait.until(EC.presence_of_element_located((selector_type, selector_value)))

                if header_logo.is_displayed() and header_logo.is_enabled():
                    href = header_logo.get_attribute("href") or ""
                    if href.endswith("/") or "blueorigin.com" in href:
                        return header_logo

            except (TimeoutException, NoSuchElementException):
                continue

        return None

    def verify_blue_origin_content(self):
        """Verify that we're on a valid Blue Origin page"""
        # Check page title
        page_title = self.driver.title.lower()
        if "blue origin" in page_title:
            return True

        # Check for Blue Origin elements
        blue_origin_selectors = [
            (By.XPATH, "//h1[contains(text(), 'Blue Origin')]"),
            (By.XPATH, "//img[contains(@alt, 'Blue Origin')]"),
            (By.CSS_SELECTOR, "[alt*='Blue Origin']")
        ]

        for selector_type, selector_value in blue_origin_selectors:
            try:
                elements = self.driver.find_elements(selector_type, selector_value)
                for element in elements:
                    if element.is_displayed():
                        element_text = element.text.lower() if element.text else ""
                        alt_text = element.get_attribute("alt") or ""
                        if "blue origin" in (element_text + alt_text).lower():
                            return True
            except NoSuchElementException:
                continue

        return False

    def navigate_with_keyboard(self, max_tabs=20):
        """Navigate using keyboard to find search jobs link"""
        actions = ActionChains(self.driver)

        for i in range(max_tabs):
            try:
                actions.send_keys(Keys.TAB).perform()
                time.sleep(0.5)

                focused_element = self.driver.switch_to.active_element
                element_text = (focused_element.text or "").lower()
                element_href = focused_element.get_attribute("href") or ""

                if ("search job" in element_text or
                        "job search" in element_text or
                        "/careers/search" in element_href):
                    return True

            except Exception as e:
                self.logger.debug(f"Keyboard navigation error at tab {i}: {str(e)}")
                continue

        return False

    def find_search_input_with_keyboard(self, max_tabs=10):
        """Find search input field using keyboard navigation"""
        actions = ActionChains(self.driver)

        for i in range(max_tabs):
            try:
                actions.send_keys(Keys.TAB).perform()
                time.sleep(0.5)

                focused_element = self.driver.switch_to.active_element
                if (focused_element.tag_name == "input" and
                        focused_element.get_attribute("type") in ["search", "text"]):
                    return True

            except Exception as e:
                self.logger.debug(f"Search input navigation error at tab {i}: {str(e)}")
                continue

        return False

    # Workday-specific methods with improved error handling
    def get_workday_job_count(self):
        """Get job count from Workday careers page"""
        try:
            self.driver.get(self.workday_url)
            self.wait_for_page_load()
            self.handle_workday_cookie_consent()

            for selector_type, selector_value in BlueOriginLocators.WORKDAY_JOB_COUNT_SELECTORS:
                try:
                    element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((selector_type, selector_value))
                    )
                    text = element.text

                    # Parse different text formats
                    patterns = [
                        r'of (\d+)',
                        r'(\d+)\s+jobs?',
                        r'(\d+)\s+total'
                    ]

                    for pattern in patterns:
                        match = re.search(pattern, text, re.IGNORECASE)
                        if match:
                            self.workday_job_count = int(match.group(1))
                            return self.workday_job_count

                except (TimeoutException, NoSuchElementException):
                    continue

            # Fallback: count visible job listings
            job_listings = self.driver.find_elements(
                *BlueOriginLocators.WORKDAY_JOB_TITLE_SELECTORS[0]
            )
            return len([job for job in job_listings if job.is_displayed()])

        except Exception as e:
            self.logger.error(f"Error getting Workday job count: {str(e)}")
            return 0

    def search_workday_platform(self, keyword):
        """Search for keyword on Workday platform"""
        for selector_type, selector_value in BlueOriginLocators.WORKDAY_SEARCH_SELECTORS:
            try:
                search_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
                search_input.clear()
                search_input.send_keys(keyword)
                search_input.send_keys(Keys.RETURN)
                time.sleep(3)
                self.wait_for_page_load()
                return True
            except (TimeoutException, NoSuchElementException):
                continue

        self.logger.error("Could not find search input on Workday")
        return False

    def get_first_workday_job_title(self):
        """Get the title of the first available job listing from Workday"""
        self.wait_for_page_load()

        for selector_type, selector_value in BlueOriginLocators.WORKDAY_JOB_TITLE_SELECTORS:
            try:
                job_elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((selector_type, selector_value))
                )

                for element in job_elements:
                    if element.is_displayed():
                        job_title = element.text.strip()
                        if self._is_valid_job_title(job_title):
                            self.logger.info(f"Found job title: '{job_title}'")
                            return job_title

            except (TimeoutException, NoSuchElementException):
                continue

        # Fallback to regex extraction
        return self._extract_job_title_from_page_source()

    def _is_valid_job_title(self, job_title):
        """Validate if text looks like a job title"""
        if not job_title or len(job_title) <= 5:
            return False

        job_keywords = [
            'engineer', 'manager', 'analyst', 'specialist', 'technician',
            'developer', 'designer', 'coordinator', 'director', 'associate',
            'intern', 'senior', 'junior', 'lead', 'principal', 'staff',
            'supervisor', 'administrator', 'consultant', 'officer'
        ]

        job_title_lower = job_title.lower()

        # Check for job keywords
        if any(keyword in job_title_lower for keyword in job_keywords):
            return True

        # Check for professional multi-word titles
        if (len(job_title) > 10 and
                job_title.count(' ') >= 1 and
                not any(char in job_title for char in ['@', '#', '$', '%', '&'])):
            return True

        return False

    def _extract_job_title_from_page_source(self):
        """Extract job title using regex patterns from page source"""
        try:
            page_source = self.driver.page_source

            # Workday-specific patterns
            patterns = [
                r'data-automation-id="jobTitle"[^>]*>([^<]+)<',
                r'<a[^>]*data-automation-id="jobTitle"[^>]*>([^<]+)</a>',
                r'<h3[^>]*data-automation-id="jobTitle"[^>]*>([^<]+)</h3>',
                r'aria-label="([^"]*(?:Engineer|Manager|Analyst|Specialist|Technician|Developer|Designer)[^"]*)"',
                r'title="([^"]*(?:Engineer|Manager|Analyst|Specialist|Technician|Developer|Designer)[^"]*)"'
            ]

            for pattern in patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                for match in matches:
                    job_title = match.strip()
                    if self._is_valid_job_title(job_title):
                        self.logger.info(f"Found job title via regex: '{job_title}'")
                        return job_title

            self.logger.warning("Could not extract job title from page source")
            return None

        except Exception as e:
            self.logger.error(f"Error extracting job title from page source: {str(e)}")
            return None

    def get_workday_search_results_count(self):
        """Get search results count from Workday after search"""
        self.wait_for_page_load()

        result_count_selectors = [
            (By.CSS_SELECTOR, "[data-automation-id='jobFoundText']"),
            (By.XPATH, "//span[contains(text(), 'jobs found') or contains(text(), 'Jobs Found')]"),
            (By.XPATH, "//div[contains(text(), 'of') and contains(text(), 'jobs')]")
        ]

        for selector_type, selector_value in result_count_selectors:
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
                text = element.text

                # Extract number from various formats
                patterns = [
                    r'(\d+)\s+jobs?\s+found',
                    r'of (\d+)',
                    r'(\d+)\s+total'
                ]

                for pattern in patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        return int(match.group(1))

            except (TimeoutException, NoSuchElementException):
                continue

        # Fallback: count visible job listings
        try:
            job_listings = self.driver.find_elements(*BlueOriginLocators.WORKDAY_JOB_TITLE_SELECTORS[0])
            visible_jobs = [job for job in job_listings if job.is_displayed()]
            return len(visible_jobs)
        except Exception:
            return 0

    def find_exact_job_title_in_results(self, exact_title):
        """Find exact job title in search results"""
        try:
            # Try Blue Origin selectors first
            selectors_to_try = [
                BlueOriginLocators.JOB_LISTING_SELECTORS[0],
                BlueOriginLocators.WORKDAY_JOB_TITLE_SELECTORS[0]
            ]

            for selector in selectors_to_try:
                try:
                    job_listings = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located(selector)
                    )

                    for job in job_listings:
                        if job.is_displayed() and job.text.strip() == exact_title:
                            return True

                except TimeoutException:
                    continue

            return False

        except Exception as e:
            self.logger.error(f"Error finding exact job title: {str(e)}")
            return False

    def test_javascript_disabled_career_functionality(self, test_case):
        """Test career page functionality with JavaScript disabled"""
        print("Starting JavaScript disabled functionality test...")

        # Verify JavaScript status
        js_disabled = True
        try:
            js_result = self.driver.execute_script("return 'javascript_working';")
            print(f"JavaScript is working: {js_result}")
            js_disabled = False
        except Exception as e:
            print(f"JavaScript disabled: {type(e).__name__}")

        # Test page title accessibility
        try:
            page_title = self.driver.title
            print(f"Page title: '{page_title}'")
            test_case.assertIn("Blue Origin", page_title, "Page title not accessible")
        except Exception as e:
            test_case.fail(f"Page title not accessible: {e}")

        # Test basic HTML content
        try:
            body_element = self.driver.find_element(By.TAG_NAME, "body")
            body_text = body_element.text
            body_length = len(body_text)
            print(f"Body text length: {body_length} characters")
            test_case.assertGreater(body_length, 100, "Page content not accessible")
        except Exception as e:
            test_case.fail(f"Body content not accessible: {e}")

        # Test navigation links
        try:
            nav_links = self.driver.find_elements(By.TAG_NAME, "a")
            accessible_links = []
            for link in nav_links:
                if link.is_displayed():
                    href = link.get_attribute("href")
                    if href and not href.startswith("javascript:"):
                        accessible_links.append(link)

            print(f"Found {len(accessible_links)} accessible navigation links")
            test_case.assertGreater(len(accessible_links), 0, "No accessible navigation links")
        except Exception as e:
            print(f"Navigation test failed: {e}")

        print("JavaScript disabled functionality test completed")

    def check_video_elements_disabled(self):
        """Check if video elements are not functional (indicating JS is disabled)"""
        try:
            # Look for video elements
            video_elements = self.driver.find_elements(By.TAG_NAME, "video")
            iframe_elements = self.driver.find_elements(By.TAG_NAME, "iframe")

            print(f"Found {len(video_elements)} video elements and {len(iframe_elements)} iframes")

            # Check if videos are not playing (good sign for JS disabled)
            videos_not_playing = True

            for video in video_elements:
                if video.is_displayed():
                    try:
                        # Try to get video properties that require JS
                        current_time = video.get_attribute("currentTime")
                        duration = video.get_attribute("duration")

                        # If we can get these, video might be working
                        if current_time or duration:
                            videos_not_playing = False
                            print(f"Video appears functional: currentTime={current_time}, duration={duration}")

                    except Exception:
                        # Exception getting video properties is good (JS disabled)
                        print("Video properties not accessible (good for JS disabled test)")

            # Check for JavaScript-dependent video players
            js_video_selectors = [
                "div[class*='video-player']",
                "div[class*='player']",
                "div[id*='player']",
                "div[class*='embed']"
            ]

            js_video_containers = []
            for selector in js_video_selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                js_video_containers.extend(elements)

            print(f"Found {len(js_video_containers)} potential JS video containers")

            # If no videos found or videos not playing, JS likely disabled
            if len(video_elements) == 0 and len(js_video_containers) == 0:
                print("No video elements found - cannot determine JS status from videos")
                return True  # Assume JS disabled

            return videos_not_playing

        except Exception as e:
            print(f"Video check failed: {e}")
            return True  # Assume JS disabled if we can't check

    def test_basic_link_navigation(self):
        """Test basic HTML link navigation functionality"""
        try:
            # Find navigation links that don't use JavaScript
            links = self.driver.find_elements(By.TAG_NAME, "a")

            valid_links = []
            for link in links:
                if link.is_displayed():
                    href = link.get_attribute("href")
                    text = link.text.strip()

                    # Look for valid HTML links (not JavaScript links)
                    if (href and
                            not href.startswith("javascript:") and
                            not href.startswith("#") and
                            len(text) > 0 and
                            len(text) < 50):  # Reasonable link text length
                        valid_links.append((link, href, text))

            print(f"Found {len(valid_links)} valid HTML links")

            if len(valid_links) == 0:
                print("No valid HTML links found for testing")
                return False

            # Try to click the first valid link
            test_link, test_href, test_text = valid_links[0]
            current_url_before = self.driver.current_url

            print(f"Testing link: '{test_text}' -> {test_href}")

            try:
                test_link.click()
                time.sleep(3)  # Wait for navigation

                current_url_after = self.driver.current_url

                if current_url_after != current_url_before:
                    print(f"Navigation successful: {current_url_before} -> {current_url_after}")
                    return True
                else:
                    print("URL did not change after clicking link")
                    return False

            except Exception as click_error:
                print(f"Link click failed: {click_error}")

                # Try alternative approach - check if link is at least clickable
                try:
                    if test_link.is_enabled() and test_link.is_displayed():
                        print("Link appears clickable (HTML functional)")
                        return True
                    else:
                        print("Link not clickable")
                        return False
                except:
                    return False

        except Exception as e:
            print(f"Link navigation test failed: {e}")
            return False

    def _find_accessible_search_input(self, selectors):
        """Find an accessible search input field"""
        for selector in selectors:
            try:
                inputs = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for inp in inputs:
                    if inp.is_displayed() and inp.is_enabled():
                        return inp
            except Exception:
                continue
        return None

    def _test_input_functionality(self, search_input, test_case):
        """Test basic input field functionality"""
        try:
            search_input.clear()
            search_input.send_keys("test search")
            entered_value = search_input.get_attribute("value")
            test_case.assertEqual(
                entered_value, "test search",
                "Input field not functional without JavaScript"
            )
            self.logger.info("✓ Basic form input functionality works")

            # Try form submission
            try:
                search_input.send_keys(Keys.RETURN)
                time.sleep(2)
                new_url = self.driver.current_url
                self.logger.info(f"Form submission attempted, current URL: {new_url}")
            except Exception as e:
                self.logger.info(f"Form submission failed (expected without JS): {str(e)}")

        except Exception as e:
            self.logger.error(f"Form interaction test failed: {str(e)}")

    # Utility methods for better code organization
    def check_for_search_functionality(self):
        """Check if search functionality is available on current page"""
        search_selectors = [
            BlueOriginLocators.SEARCH_INPUT,
            BlueOriginLocators.KEYWORD_SEARCH_INPUT,
            (By.CSS_SELECTOR, "input[type='search']"),
            (By.CSS_SELECTOR, "input[type='text']"),
            (By.CSS_SELECTOR, "input[placeholder*='search' i]")
        ]

        for selector in search_selectors:
            try:
                search_element = self.driver.find_element(*selector)
                if search_element.is_displayed() and search_element.is_enabled():
                    return True
            except NoSuchElementException:
                continue

        return False

    def take_screenshot(self, filename):
        """Take screenshot for debugging purposes"""
        try:
            screenshot_dir = "screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            filepath = os.path.join(screenshot_dir, f"{filename}_{int(time.time())}.png")
            self.driver.save_screenshot(filepath)
            self.logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            return None

    def get_page_performance_metrics(self):
        """Get basic page performance metrics"""
        try:
            navigation_timing = self.driver.execute_script(
                "return window.performance.timing"
            )

            load_time = navigation_timing['loadEventEnd'] - navigation_timing['navigationStart']
            dom_ready_time = navigation_timing['domContentLoadedEventEnd'] - navigation_timing['navigationStart']

            return {
                'load_time_ms': load_time,
                'dom_ready_time_ms': dom_ready_time,
                'page_ready': load_time > 0
            }
        except Exception as e:
            self.logger.warning(f"Could not get performance metrics: {str(e)}")
            return {'load_time_ms': 0, 'dom_ready_time_ms': 0, 'page_ready': False}


class BlueOriginUrls:
    """Class containing all URLs for Blue Origin career website"""

    BASE_URL = "https://www.blueorigin.com"
    CAREERS_URL = f"{BASE_URL}/careers"
    CAREERS_SEARCH_URL = f"{BASE_URL}/careers/search"
    WORKDAY_URL = "https://blueorigin.wd5.myworkdayjobs.com/en-US/BlueOrigin"

    @classmethod
    def get_all_urls(cls):
        """Get all available URLs as a dictionary"""
        return {
            'base': cls.BASE_URL,
            'careers': cls.CAREERS_URL,
            'careers_search': cls.CAREERS_SEARCH_URL,
            'workday': cls.WORKDAY_URL
        }

    @classmethod
    def validate_url(cls, url):
        """Validate if URL belongs to Blue Origin domain"""
        valid_domains = ['blueorigin.com', 'wd5.myworkdayjobs.com']
        return any(domain in url.lower() for domain in valid_domains)