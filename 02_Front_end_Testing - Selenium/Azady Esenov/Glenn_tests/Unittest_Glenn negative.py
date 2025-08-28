import unittest
import time
import AllureReports
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import helpers as h

def delay():
    time.sleep(random.randint(2, 5))

class ChromeSearchNegative(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=options, service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()

    def dismiss_popups(self):
        """Helper method to dismiss any popups or banners"""
        try:
            # Try to close cookie/privacy banner
            accept_btn = self.driver.find_element(By.XPATH,
                                                  "//button[contains(text(), 'Accept') or contains(text(), 'OK') or contains(text(), 'Close')]")
            accept_btn.click()
            time.sleep(1)
        except:
            pass
        try:
            # Try to close any modal dialogs
            close_btn = self.driver.find_element(By.XPATH,
                                                 "//button[@class='close'] | //span[text()='×'] | //*[@aria-label='Close']")
            close_btn.click()
            time.sleep(1)
        except:
            pass

    def safe_click(self, element):
        """Helper method for safe clicking with multiple strategies"""
        try:
            # First try normal click
            element.click()
            return True
        except:
            return False

    def test_N1_invalid_new_glenn_url_chrome(self):
        """TC_N_011: Verify that accessing an invalid New Glenn collection URL returns an error page"""
        driver = self.driver

        print("Starting TC_N_011 - Invalid New Glenn URL Test")

        # Step 1: Navigate to incorrect URL with random characters
        invalid_url = h.shop_main_url + "collections/new-gle6768nngfhn"
        driver.get(invalid_url)
        print(f"Step 1: Navigate to invalid URL: {invalid_url}")

        # Step 2: Wait for the page to load
        time.sleep(3)
        print("Step 2: Wait for the page to load")

        # Step 3: Verify 404 error page appears
        try:
            # Check for common 404 indicators
            page_source = driver.page_source.lower()
            if "404" in page_source or "not found" in page_source or "page not found" in page_source:
                print("Step 3: 404 error page correctly displayed")
                print("TC_N_011 PASSED")
            else:
                print("Step 3: Expected 404 error page not found")
                print("TC_N_011 FAILED")
        except Exception as e:
            print(f"Step 3: Error checking for 404 page: {e}")
            print("TC_N_011 FAILED")

    def test_N2_invalid_search_characters_chrome(self):
        """TC_N_012: Verify that user can enter invalid characters in Search Line and proper handling occurs"""
        driver = self.driver

        print("Starting TC_N_012 - Invalid Search Characters Test")

        # Step 1: Navigate to New Glenn collection
        driver.get(h.new_glenn_collection_url)
        print("Step 1: Navigate to New Glenn collection")

        # Step 2: Wait for page to load
        time.sleep(3)
        print("Step 2: Wait for page to load")

        # Step 3: Click on search icon
        try:
            search_icon = driver.find_element(By.XPATH, h.search_icon)
            search_icon.click()
            delay()
            print("Step 3: Click on search icon")
        except NoSuchElementException:
            print("Search icon not found, continuing with direct search")

        # Step 4: Enter special characters
        try:
            search_box = driver.find_element(By.XPATH, h.search_input)
            invalid_search = h.invalid_search_chars
            search_box.clear()
            search_box.send_keys(invalid_search)
            search_box.send_keys(Keys.ENTER)
            print(f"Step 4: Enter special characters: {invalid_search}")

            # Step 5: Wait for results
            time.sleep(3)
            print("Step 5: Wait for search results")

            # Step 6: Check if proper "no results" message appears
            page_source = driver.page_source.lower()
            if "no results" in page_source or "no products found" in page_source or "0 results" in page_source:
                print("Step 6: Proper 'no results' message displayed")
                print("TC_N_012 PASSED")
            else:
                print("Step 6: Expected 'no results' message not found - showing unrelated products")
                print("TC_N_012 FAILED")

        except NoSuchElementException:
            print("Search input field not found")
            print("TC_N_012 FAILED")

    def test_N3_float_quantity_validation_chrome(self):
        """TC_N_013: Verify that entering a non-integer (float) value in quantity field is not accepted"""
        driver = self.driver

        print("Starting TC_N_013 - Float Quantity Validation Test")

        # Step 1: Navigate to New Glenn collection
        driver.get(h.new_glenn_collection_url)
        print("Step 1: Navigate to New Glenn collection")

        # Step 2: Wait for page to load
        time.sleep(5)
        print("Step 2: Wait for page to load")

        # Dismiss any popups
        self.dismiss_popups()

        # Step 3: Click on the first available product
        try:
            wait = WebDriverWait(driver, 10)
            hat = wait.until(EC.element_to_be_clickable((By.XPATH, h.new_glenn_monogram_hat)))

            # Scroll to element first
            driver.execute_script("arguments[0].scrollIntoView(true);", hat)
            time.sleep(2)

            # Try safe click
            if self.safe_click(hat):
                print("Step 3: Click on New Glenn Monogram Hat")
                delay()

                # Step 4: Locate quantity input field
                try:
                    quantity_field = wait.until(EC.presence_of_element_located((By.XPATH, h.quantity_input)))

                    # Scroll to quantity field
                    driver.execute_script("arguments[0].scrollIntoView(true);", quantity_field)
                    time.sleep(1)

                    quantity_field.clear()
                    float_value = "1.5"
                    quantity_field.send_keys(float_value)
                    print(f"Step 4: Enter float value: {float_value}")

                    # Step 5: Try to add to cart or submit
                    try:
                        add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, h.add_to_cart_button)))

                        # Scroll to add to cart button
                        driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart_btn)
                        time.sleep(1)

                        if self.safe_click(add_to_cart_btn):
                            time.sleep(3)

                            # Step 6: Check for validation message
                            page_source = driver.page_source.lower()
                            if "multiple of 1" in page_source or "whole number" in page_source or "integer" in page_source:
                                print("Step 6: Proper validation message displayed")
                                print("TC_N_013 PASSED")
                            else:
                                print("Step 6: Expected validation message not found")
                                print("TC_N_013 FAILED")
                        else:
                            print("Could not click Add to Cart button")
                            print("TC_N_013 FAILED")

                    except Exception as e:
                        print(f"Add to Cart button error: {e}")
                        print("TC_N_013 FAILED")

                except Exception as e:
                    print(f"Quantity input field error: {e}")
                    print("TC_N_013 FAILED")
            else:
                print("Could not click on product")
                print("TC_N_013 FAILED")

        except Exception as e:
            print(f"New Glenn Monogram Hat error: {e}")
            print("TC_N_013 FAILED")

    def test_N4_price_filter_max_value_chrome(self):
        """TC_N_014: Verify that entering price above maximum in filter triggers validation"""
        driver = self.driver

        print("Starting TC_N_014 - Price Filter Max Value Test")

        # Step 1: Navigate to New Glenn collection
        driver.get(h.new_glenn_collection_url)
        print("Step 1: Navigate to New Glenn collection")

        # Step 2: Wait for page to load
        time.sleep(3)
        print("Step 2: Wait for page to load")

        # Step 3: Look for price filter
        try:
            # Try to find and interact with price filter
            driver.find_element(By.XPATH, h.price_button).click()
            price_to_field = driver.find_element(By.XPATH, h.price_filter_to)
            price_to_field.clear()
            high_price = "300"
            price_to_field.send_keys(high_price)
            price_to_field.send_keys(Keys.ENTER)
            print(f"Step 3: Enter high price value: ${high_price}")

            # Step 4: Wait for validation
            time.sleep(2)
            print("Step 4: Wait for validation response")

            # Step 5: Check for validation message
            page_source = driver.page_source.lower()
            if "highest price" in page_source or "maximum price" in page_source or "price limit" in page_source:
                print("Step 5: Price validation message displayed correctly")
                print("TC_N_014 PASSED")
            else:
                print("Step 5: Expected price validation message not found")
                print("TC_N_014 FAILED")

        except NoSuchElementException:
            print("Price filter not found on this page")
            print("TC_N_014 SKIPPED - Feature not available")

    def test_N5_empty_cart_checkout_chrome(self):
        """TC_N_015: Verify that attempting to check out with empty cart shows proper message"""
        driver = self.driver

        print("Starting TC_N_015 - Empty Cart Checkout Test")

        # Step 1: Navigate to shop main page
        driver.get(h.shop_main_url)
        print("Step 1: Navigate to shop main page")

        # Step 2: Wait for page to load
        time.sleep(3)
        print("Step 2: Wait for page to load")

        # Step 3: Try to access cart directly
        try:
            # Look for cart icon or link
            cart_link = driver.find_element(By.XPATH, h.cart_link)
            cart_link.click()
            delay()
            print("Step 3: Click on cart")

            # Step 4: Check for empty cart message
            page_source = driver.page_source.lower()
            if "empty" in page_source or "no items" in page_source or "cart is empty" in page_source:
                print("Step 4: Empty cart message displayed correctly")

                # Step 5: Try to find checkout button and verify it's disabled or shows message
                try:
                    checkout_btn = driver.find_element(By.XPATH, h.checkout_button)
                    if not checkout_btn.is_enabled():
                        print("Step 5: Checkout button properly disabled")
                        print("TC_N_015 PASSED")
                    else:
                        checkout_btn.click()
                        time.sleep(2)
                        # Check if proper message appears after clicking
                        new_page_source = driver.page_source.lower()
                        if "add items" in new_page_source or "cart is empty" in new_page_source:
                            print("Step 5: Proper message shown when trying to checkout empty cart")
                            print("TC_N_015 PASSED")
                        else:
                            print("Step 5: No proper handling of empty cart checkout")
                            print("TC_N_015 FAILED")
                except NoSuchElementException:
                    print("Step 5: Checkout button not available for empty cart")
                    print("TC_N_015 PASSED")
            else:
                print("Step 4: Empty cart message not found")
                print("TC_N_015 FAILED")

        except NoSuchElementException:
            print("Cart link not found")
            print("TC_N_015 FAILED")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(AllureReports)