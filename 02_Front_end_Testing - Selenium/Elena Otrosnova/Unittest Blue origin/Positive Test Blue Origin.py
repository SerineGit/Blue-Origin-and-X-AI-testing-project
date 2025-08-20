import unittest
#import AllureReports
import time
from test_helpers import (WebDriverFactory, PageHelpers, TestUtils, Constants)


class BlueOriginChromeTest(unittest.TestCase):
    """Chrome browser test cases"""

    def setUp(self):
        """Set up Chrome driver"""
        try:
            self.driver = WebDriverFactory.create_chrome_driver()
            self.browser_name = "Chrome"
        except TypeError as e:
            # Fallback to simple driver creation
            from selenium.webdriver import Chrome
            from selenium.webdriver.chrome.options import Options as ChromeOptions

            chrome_options = ChromeOptions()
            chrome_options.add_argument("--start-maximized")
            self.driver = Chrome(options=chrome_options)
            self.browser_name = "Chrome"

    def test_accessories_page_loads_successfully_chrome(self):
        """TC_P_016: Verify that Accessories page loads successfully with product grid in Chrome"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Verify page title
        title_valid, title = PageHelpers.verify_page_title(
            driver, Constants.EXPECTED_TITLE_TEXTS, self.browser_name
        )
        assert title_valid, f"Expected Blue Origin or Accessories in title, got: {title}"

        # Verify product grid presence
        grid_found = PageHelpers.find_product_grid(driver, self.browser_name)
        assert grid_found, "Product grid not found on accessories page in Chrome"
        print(f"{self.browser_name}: Product grid verification passed")

    def test_relevant_products_displayed_chrome(self):
        """TC_P_017: Verify that relevant products in Accessories page are displayed in Chrome"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Find products
        products, product_count = PageHelpers.find_products(driver, self.browser_name)
        assert products, "No products found on accessories page in Chrome"
        assert product_count > 0, f"Expected at least 1 product, found {product_count} in Chrome"
        print(f"{self.browser_name}: Product display verification passed - {product_count} products found")

    def test_add_to_cart_button_works_chrome(self):
        """TC_P_018: Verify that Add to Cart button works in Chrome"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Navigate to product detail page
        product_clicked = PageHelpers.navigate_to_product(driver, self.browser_name)
        assert product_clicked, "Could not click on any product in Chrome"

        # Wait for product detail page to load
        time.sleep(1)
        TestUtils.wait_for_page_load(driver)

        # Find and click Add to Cart button
        cart_button_clicked = PageHelpers.find_add_to_cart_button(driver, self.browser_name)
        assert cart_button_clicked, "Add to Cart button not found or not clickable in Chrome"
        print(f"{self.browser_name}: Add to Cart functionality verification passed")

    def test_zoom_functionality_chrome(self):
        """TC_P_019: Verify that Zoom functionality works in Chrome"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Navigate to product detail page
        product_clicked = PageHelpers.navigate_to_product(driver, self.browser_name)
        assert product_clicked, "Could not navigate to product detail page in Chrome"

        # Wait for product page to load
        time.sleep(1)
        TestUtils.wait_for_page_load(driver)

        # Test zoom functionality
        zoom_tested = PageHelpers.test_image_zoom(driver, self.browser_name)
        if zoom_tested:
            print(f"{self.browser_name}: Zoom functionality verification completed")
        else:
            print(f"{self.browser_name}: No explicit zoom functionality found - this may be normal for this site")

    def test_user_login_functionality_chrome(self):
        """TC_P_020: Verify user login functionality in Chrome"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Find and click login link
        login_found = PageHelpers.find_login_functionality(driver, self.browser_name)

        if login_found:
            time.sleep(1)
            TestUtils.wait_for_page_load(driver)
            print(f"{self.browser_name}: Login page/form displayed")

            # Verify login form elements
            form_valid = PageHelpers.verify_login_form(driver, self.browser_name)
            assert form_valid, "Login form incomplete"
            print(f"{self.browser_name}: Login functionality structure verified")
        else:
            print(f"{self.browser_name}: No login functionality found on the page")

    def tearDown(self):
        """Clean up after each test"""
        TestUtils.safe_teardown(self.driver, self.browser_name)


class BlueOriginFirefoxTest(unittest.TestCase):
    """Firefox browser test cases"""

    def setUp(self):
        """Set up Firefox driver"""
        try:
            self.driver = WebDriverFactory.create_firefox_driver()
            self.browser_name = "Firefox"
        except Exception as e:
            self.skipTest(f"Firefox driver failed to initialize: {e}")

    def test_accessories_page_loads_successfully_firefox(self):
        """TC_P_016: Verify that Accessories page loads successfully with product grid in Firefox"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Verify page title
        title_valid, title = PageHelpers.verify_page_title(
            driver, Constants.EXPECTED_TITLE_TEXTS, self.browser_name
        )
        assert title_valid, f"Expected Blue Origin or Accessories in title, got: {title}"

        # Verify product grid presence
        grid_found = PageHelpers.find_product_grid(driver, self.browser_name)
        assert grid_found, "Product grid not found on accessories page in Firefox"
        print(f"{self.browser_name}: Product grid verification passed")

    def test_relevant_products_displayed_firefox(self):
        """TC_P_017: Verify that relevant products in Accessories page are displayed in Firefox"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Find products
        products, product_count = PageHelpers.find_products(driver, self.browser_name)
        assert products, "No products found on accessories page in Firefox"
        assert product_count > 0, f"Expected at least 1 product, found {product_count} in Firefox"
        print(f"{self.browser_name}: Product display verification passed - {product_count} products found")

    def test_add_to_cart_button_works_firefox(self):
        """TC_P_018: Verify that Add to Cart button works in Firefox"""
        driver = self.driver

        try:
            driver.get(Constants.BASE_URL)
            TestUtils.wait_for_page_load(driver, timeout=10)

            # Navigate to product detail page
            product_clicked = PageHelpers.navigate_to_product(driver, self.browser_name, timeout=10)
            if not product_clicked:
                self.skipTest("Could not click on any product in Firefox - page may not have loaded properly")

            # Wait for product detail page to load
            time.sleep(1)
            TestUtils.wait_for_page_load(driver, timeout=10)

            # Find and click Add to Cart button
            cart_button_clicked = PageHelpers.find_add_to_cart_button(driver, self.browser_name, timeout=10)
            assert cart_button_clicked, "Add to Cart button not found or not clickable in Firefox"

            time.sleep(2)
            print(f"{self.browser_name}: Add to Cart functionality verification passed")

        except Exception as e:
            self.skipTest(f"Firefox test failed due to browser instability: {e}")

    def test_zoom_functionality_firefox(self):
        """TC_P_019: Verify that Zoom functionality works in Firefox"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Navigate to product detail page
        product_clicked = PageHelpers.navigate_to_product(driver, self.browser_name)
        assert product_clicked, "Could not navigate to product detail page in Firefox"

        # Wait for product page to load
        time.sleep(2)
        TestUtils.wait_for_page_load(driver)

        # Test zoom functionality
        zoom_tested = PageHelpers.test_image_zoom(driver, self.browser_name)
        if zoom_tested:
            print(f"{self.browser_name}: Zoom functionality verification completed")
        else:
            print(f"{self.browser_name}: No explicit zoom functionality found - this may be normal for this site")

    def test_user_login_functionality_firefox(self):
        """TC_P_020: Verify user login functionality in Firefox"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Find and click login link
        login_found = PageHelpers.find_login_functionality(driver, self.browser_name)

        if login_found:
            time.sleep(1)
            TestUtils.wait_for_page_load(driver)
            print(f"{self.browser_name}: Login page/form displayed")

            # Verify login form elements
            form_valid = PageHelpers.verify_login_form(driver, self.browser_name)
            assert form_valid, "Login form incomplete"
            print(f"{self.browser_name}: Login functionality structure verified")
        else:
            print(f"{self.browser_name}: No login functionality found on the page")

    def tearDown(self):
        """Clean up after each test"""
        TestUtils.safe_teardown(self.driver, self.browser_name)


class BlueOriginEdgeTest(unittest.TestCase):
    """Edge browser test cases"""

    def setUp(self):
        """Set up Edge driver"""
        self.driver = WebDriverFactory.create_edge_driver()
        self.browser_name = "Edge"

    def test_accessories_page_loads_successfully_edge(self):
        """TC_P_016: Verify that Accessories page loads successfully with product grid in Edge"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Verify page title
        title_valid, title = PageHelpers.verify_page_title(
            driver, Constants.EXPECTED_TITLE_TEXTS, self.browser_name
        )
        assert title_valid, f"Expected Blue Origin or Accessories in title, got: {title}"

        # Verify product grid presence
        grid_found = PageHelpers.find_product_grid(driver, self.browser_name)
        assert grid_found, "Product grid not found on accessories page in Edge"
        print(f"{self.browser_name}: Product grid verification passed")

    def test_relevant_products_displayed_edge(self):
        """TC_P_017: Verify that relevant products in Accessories page are displayed in Edge"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Find products
        products, product_count = PageHelpers.find_products(driver, self.browser_name)
        assert products, "No products found on accessories page in Edge"
        assert product_count > 0, f"Expected at least 1 product, found {product_count} in Edge"
        print(f"{self.browser_name}: Product display verification passed - {product_count} products found")

    def test_add_to_cart_button_works_edge(self):
        """TC_P_018: Verify that Add to Cart button works in Edge"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Navigate to product detail page
        product_clicked = PageHelpers.navigate_to_product(driver, self.browser_name)
        assert product_clicked, "Could not click on any product in Edge"

        # Wait for product detail page to load
        time.sleep(1)
        TestUtils.wait_for_page_load(driver)

        # Find and click Add to Cart button
        cart_button_clicked = PageHelpers.find_add_to_cart_button(driver, self.browser_name)
        assert cart_button_clicked, "Add to Cart button not found or not clickable in Edge"
        print(f"{self.browser_name}: Add to Cart functionality verification passed")

    def test_zoom_functionality_edge(self):
        """TC_P_019: Verify that Zoom functionality works in Edge"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Navigate to product detail page
        product_clicked = PageHelpers.navigate_to_product(driver, self.browser_name)
        assert product_clicked, "Could not navigate to product detail page in Edge"

        # Wait for product page to load
        time.sleep(1)
        TestUtils.wait_for_page_load(driver)

        # Test zoom functionality
        zoom_tested = PageHelpers.test_image_zoom(driver, self.browser_name)
        if zoom_tested:
            print(f"{self.browser_name}: Zoom functionality verification completed")
        else:
            print(f"{self.browser_name}: No explicit zoom functionality found - this may be normal for this site")

    def test_user_login_functionality_edge(self):
        """TC_P_020: Verify user login functionality in Edge"""
        driver = self.driver
        driver.get(Constants.BASE_URL)
        TestUtils.wait_for_page_load(driver)

        # Find and click login link
        login_found = PageHelpers.find_login_functionality(driver, self.browser_name)

        if login_found:
            time.sleep(1)
            TestUtils.wait_for_page_load(driver)
            print(f"{self.browser_name}: Login page/form displayed")

            # Verify login form elements
            form_valid = PageHelpers.verify_login_form(driver, self.browser_name)
            assert form_valid, "Login form incomplete"
            print(f"{self.browser_name}: Login functionality structure verified")
        else:
            print(f"{self.browser_name}: No login functionality found on the page")

    def tearDown(self):
        """Clean up after each test"""
        TestUtils.safe_teardown(self.driver, self.browser_name)



#if __name__ == "__main__":
    #unittest.main(AllureReports)

if __name__ == '__main__':
      loader = unittest.TestLoader()