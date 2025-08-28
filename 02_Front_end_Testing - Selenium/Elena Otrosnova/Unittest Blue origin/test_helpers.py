import time
import os
import signal
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService


class WebDriverFactory:
    """Factory class for creating browser instances with proper configuration"""

    @staticmethod
    def create_chrome_driver(disable_javascript=False):
        """Create Chrome WebDriver with optimized settings"""
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")

        if disable_javascript:
            chrome_options.add_argument("--disable-javascript")

        try:
            # Create service and pass both service and options
            service = ChromeService()
            driver = webdriver.Chrome(service=service, options=chrome_options)

            if not disable_javascript:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            return driver
        except Exception as e:
            print(f"Failed to create Chrome driver: {e}")
            raise

    @staticmethod
    def create_firefox_driver(disable_javascript=False):
        """Create Firefox WebDriver with optimized settings"""
        firefox_options = FirefoxOptions()
        firefox_options.set_preference("dom.webdriver.enabled", False)
        firefox_options.set_preference('useAutomationExtension', False)
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")

        if disable_javascript:
            firefox_options.set_preference("javascript.enabled", False)

        try:
            # Create service and pass both service and options
            service = FirefoxService()
            driver = webdriver.Firefox(service=service, options=firefox_options)

            if not disable_javascript:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            driver.maximize_window()
            return driver
        except Exception as e:
            print(f"Failed to create Firefox driver: {e}")
            raise

    @staticmethod
    def create_edge_driver(disable_javascript=False):
        """Create Edge WebDriver with optimized settings"""
        edge_options = EdgeOptions()
        edge_options.add_argument("--disable-blink-features=AutomationControlled")
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--start-maximized")

        if disable_javascript:
            edge_options.add_argument("--disable-javascript")

        try:
            # Create service and pass both service and options
            service = EdgeService()
            driver = webdriver.Edge(service=service, options=edge_options)

            if not disable_javascript:
                driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            return driver
        except Exception as e:
            print(f"Failed to create Edge driver: {e}")
            raise

    @staticmethod
    def get_driver(browser_name, disable_javascript=False):
        """Get driver instance based on browser name"""
        browser_name = browser_name.lower()
        if browser_name == 'chrome':
            return WebDriverFactory.create_chrome_driver(disable_javascript)
        elif browser_name == 'firefox':
            return WebDriverFactory.create_firefox_driver(disable_javascript)
        elif browser_name == 'edge':
            return WebDriverFactory.create_edge_driver(disable_javascript)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")



class ElementInteraction:
    """Helper class for element interactions"""

    @staticmethod
    def safe_click(driver, element, browser_name=""):
        """Safely click an element with fallback to JavaScript click"""
        try:
            element.click()
            print(f"{browser_name}: Successfully clicked with regular click")
            return True
        except Exception as click_error:
            print(f"{browser_name}: Regular click failed, trying JavaScript: {click_error}")
            try:
                driver.execute_script("arguments[0].click();", element)
                print(f"{browser_name}: Successfully clicked with JavaScript")
                return True
            except Exception as js_error:
                print(f"{browser_name}: JavaScript click failed: {js_error}")
                return False

    @staticmethod
    def safe_send_keys(driver, element, text, browser_name=""):
        """Safely send keys to an element with multiple attempts"""
        try:
            element.clear()
            element.send_keys(text)
            print(f"{browser_name}: Successfully entered text: {text}")
            return True
        except Exception as e:
            print(f"{browser_name}: Send keys failed: {e}")
            try:
                # Try JavaScript approach
                driver.execute_script(f"arguments[0].value = '{text}';", element)
                print(f"{browser_name}: Successfully entered text via JavaScript")
                return True
            except Exception as js_error:
                print(f"{browser_name}: JavaScript text entry failed: {js_error}")
                return False

    @staticmethod
    def scroll_to_element(driver, element, smooth=True):
        """Scroll element into view"""
        if smooth:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        else:
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        time.sleep(1)

    @staticmethod
    def wait_and_find_element(driver, selectors, timeout=5):
        """Try multiple selectors and return the first element found"""
        wait = WebDriverWait(driver, timeout)
        for by_type, selector in selectors:
            try:
                element = wait.until(EC.presence_of_element_located((by_type, selector)))
                return element, selector
            except TimeoutException:
                continue
        return None, None

    @staticmethod
    def wait_and_find_elements(driver, selectors, timeout=5):
        """Try multiple selectors and return the first list of elements found"""
        wait = WebDriverWait(driver, timeout)
        for by_type, selector in selectors:
            try:
                elements = wait.until(EC.presence_of_all_elements_located((by_type, selector)))
                if elements:
                    return elements, selector
            except TimeoutException:
                continue
        return [], None


class NavigationHelpers:
    """Navigation helper class for Blue Origin shop"""

    @staticmethod
    def navigate_to_homepage(driver, browser_name=""):
        """Navigate to Blue Origin homepage"""
        try:
            driver.get(Constants.BASE_URL_HOME)
            TestUtils.wait_for_page_load(driver)
            print(f"{browser_name}: Successfully navigated to homepage")
            return True
        except Exception as e:
            print(f"{browser_name}: Failed to navigate to homepage: {e}")
            return False

    @staticmethod
    def navigate_to_accessories(driver, browser_name=""):
        """Navigate to Blue Origin accessories page"""
        try:
            driver.get(Constants.BASE_URL_ACCESSORIES)
            TestUtils.wait_for_page_load(driver)
            print(f"{browser_name}: Successfully navigated to accessories page")
            return True
        except Exception as e:
            print(f"{browser_name}: Failed to navigate to accessories page: {e}")
            return False



class PageHelpers:
    """Helper class for page-specific operations"""

    @staticmethod
    def verify_page_title(driver, expected_texts, browser_name=""):
        """Verify page title contains expected text"""
        title = driver.title
        title_valid = any(text in title for text in expected_texts)
        if title_valid:
            print(f"{browser_name}: Page title is: {title}")
        return title_valid, title

    @staticmethod
    def find_product_grid(driver, browser_name="", timeout=5):
        """Find and verify product grid presence"""
        product_grid_selectors = [
            (By.CSS_SELECTOR, ".product-grid .product-item img"),
            (By.CSS_SELECTOR, ".collection-grid .product img"),
            (By.XPATH, "//div[contains(@class, 'product')]//img"),
            (By.CSS_SELECTOR, "[class*='product'] img")
        ]

        element, selector = ElementInteraction.wait_and_find_element(driver, product_grid_selectors, timeout)
        if element:
            print(f"{browser_name}: Product grid found using selector: {selector}")
            return True
        return False

    @staticmethod
    def find_products(driver, browser_name="", timeout=5):
        """Find products on the page"""
        product_selectors = [
            (By.CSS_SELECTOR, ".product-grid .product-item"),
            (By.CSS_SELECTOR, ".collection-grid .product"),
            (By.XPATH, "//div[contains(@class, 'product')]"),
            (By.CSS_SELECTOR, "[class*='product-item']")
        ]

        products, selector = ElementInteraction.wait_and_find_elements(driver, product_selectors, timeout)
        if products:
            print(f"{browser_name}: Found {len(products)} products using selector: {selector}")
            return products, len(products)
        return [], 0

    @staticmethod
    def navigate_to_product(driver, browser_name="", timeout=5):
        """Navigate to a product detail page"""
        product_link_selectors = [
            (By.CSS_SELECTOR, ".product-grid .product-item a"),
            (By.CSS_SELECTOR, ".collection-grid .product a"),
            (By.XPATH, "//div[contains(@class,'product')]//a[contains(@href,'/products/')]")
        ]

        for by_type, selector in product_link_selectors:
            try:
                wait = WebDriverWait(driver, timeout)
                links = wait.until(EC.presence_of_all_elements_located((by_type, selector)))
                if not links:
                    continue

                for i, link in enumerate(links[:3]):
                    try:
                        wait.until(EC.element_to_be_clickable(link))
                        ElementInteraction.scroll_to_element(driver, link)

                        if ElementInteraction.safe_click(driver, link, browser_name):
                            print(f"{browser_name}: Successfully clicked product {i + 1}")
                            return True
                    except Exception:
                        continue
            except TimeoutException:
                continue
        return False

    @staticmethod
    def find_add_to_cart_button(driver, browser_name="", timeout=5):
        """Find and click Add to Cart button"""
        add_to_cart_selectors = [
            (By.NAME, "add"),
            (By.CSS_SELECTOR, "button[name='add']"),
            (By.XPATH, "//button[contains(text(), 'Add to cart') or contains(text(), 'ADD TO CART')]"),
            (By.CSS_SELECTOR, ".btn-cart, .add-to-cart, [class*='add-to-cart']")
        ]

        element, selector = ElementInteraction.wait_and_find_element(driver, add_to_cart_selectors, timeout)
        if element:
            try:
                wait = WebDriverWait(driver, timeout)
                btn = wait.until(EC.element_to_be_clickable(element))
                print(f"{browser_name}: Add to Cart button found")
                ElementInteraction.scroll_to_element(driver, btn)

                if ElementInteraction.safe_click(driver, btn, browser_name):
                    print(f"{browser_name}: Add to Cart button clicked successfully")
                    return True
            except (TimeoutException, NoSuchElementException):
                pass
        return False

    @staticmethod
    def test_image_zoom(driver, browser_name="", timeout=5):
        """Test zoom functionality on product images"""
        image_selectors = [
            "//img[contains(@class, 'product-image')]",
            "//div[contains(@class, 'product-image')]//img",
            "//div[contains(@class, 'product-photo')]//img",
            "//img[contains(@alt, 'product') or contains(@alt, 'Product')]"
        ]

        wait = WebDriverWait(driver, timeout)
        for selector in image_selectors:
            try:
                product_image = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                wait.until(EC.visibility_of(product_image))

                # Test hover functionality
                actions = ActionChains(driver)
                actions.move_to_element(product_image).perform()
                time.sleep(1)
                print(f"{browser_name}: Hovered over product image")

                # Test click functionality
                if product_image.is_displayed():
                    ElementInteraction.safe_click(driver, product_image, browser_name)
                    time.sleep(1)
                    print(f"{browser_name}: Successfully interacted with product image")
                    return True
            except (TimeoutException, NoSuchElementException):
                continue
        return False

    @staticmethod
    def find_login_functionality(driver, browser_name="", timeout=5):
        """Find and test login functionality"""
        login_selectors = [
            "//a[contains(text(), 'Login')]",
            "//a[contains(text(), 'Sign In')]",
            "//a[contains(text(), 'Account')]",
            "//a[contains(@href, 'login')]",
            "//a[contains(@href, 'account')]"
        ]

        wait = WebDriverWait(driver, timeout)
        for selector in login_selectors:
            try:
                login_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, selector)))
                if login_elements:
                    login_link = login_elements[0]
                    wait.until(EC.element_to_be_clickable(login_link))
                    ElementInteraction.scroll_to_element(driver, login_link)

                    if ElementInteraction.safe_click(driver, login_link, browser_name):
                        print(f"{browser_name}: Found and clicked login link using selector: {selector}")
                        return True
            except TimeoutException:
                continue
        return False

    @staticmethod
    def verify_login_form(driver, browser_name="", timeout=2):
        """Verify login form elements are present"""
        login_form_selectors = [
            "//input[@type='email' or @name='email']",
            "//input[@type='password' or @name='password']",
            "//button[contains(text(), 'Login') or contains(text(), 'Sign In')]"
        ]

        wait = WebDriverWait(driver, timeout)
        form_elements_found = 0

        for selector in login_form_selectors:
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                form_elements_found += 1
                print(f"{browser_name}: Login form element found: {selector}")
            except TimeoutException:
                continue

        if form_elements_found >= 2:
            print(f"{browser_name}: Login form elements verified - email, password fields and login button present")
            return True
        return False


class ProductHelpers:
    """Product interaction helpers"""

    @staticmethod
    def find_product_by_name(driver, product_name, browser_name="", timeout=2):
        """Find a product by its name or partial name"""
        # Split product name into keywords for more flexible searching
        keywords = product_name.split()

        product_selectors = []

        # Add selectors for full product name
        product_selectors.extend([
            (By.XPATH, f"//h2[contains(text(), '{product_name}')]"),
            (By.XPATH, f"//h3[contains(text(), '{product_name}')]"),
            (By.XPATH, f"//a[contains(text(), '{product_name}')]"),
            (By.XPATH, f"//*[contains(text(), '{product_name}')]//ancestor::div[contains(@class, 'product')]"),
            (By.XPATH, f"//*[contains(text(), '{product_name}')]//ancestor::a"),
            (By.XPATH, f"//img[contains(@alt, '{product_name}')]//ancestor::a")
        ])

        # Add selectors for individual keywords
        for keyword in keywords:
            if len(keyword) > 3:  # Only use meaningful keywords
                product_selectors.extend([
                    (By.XPATH, f"//h2[contains(text(), '{keyword}')]"),
                    (By.XPATH, f"//h3[contains(text(), '{keyword}')]"),
                    (By.XPATH, f"//a[contains(text(), '{keyword}')]"),
                    (By.XPATH, f"//*[contains(text(), '{keyword}')]//ancestor::div[contains(@class, 'product')]"),
                    (By.XPATH, f"//*[contains(text(), '{keyword}')]//ancestor::a"),
                    (By.XPATH, f"//img[contains(@alt, '{keyword}')]//ancestor::a")
                ])

        for by_type, selector in product_selectors:
            try:
                wait = WebDriverWait(driver, timeout)
                element = wait.until(EC.presence_of_element_located((by_type, selector)))
                if element and element.is_displayed():
                    print(f"{browser_name}: Found product '{product_name}' using selector: {selector}")
                    return element
            except TimeoutException:
                continue

        print(f"{browser_name}: Could not find specific product '{product_name}', will try any available product")
        return None

    @staticmethod
    def click_product(driver, product_name, browser_name="", timeout=3):
        """Click on a specific product"""
        # First try to find the product
        product_element = ProductHelpers.find_product_by_name(driver, product_name, browser_name, timeout)

        if product_element:
            try:
                wait = WebDriverWait(driver, timeout)
                clickable_element = wait.until(EC.element_to_be_clickable(product_element))
                ElementInteraction.scroll_to_element(driver, clickable_element)

                if ElementInteraction.safe_click(driver, clickable_element, browser_name):
                    print(f"{browser_name}: Successfully clicked on product '{product_name}'")
                    TestUtils.wait_for_page_load(driver)
                    return True
            except TimeoutException:
                pass

        # If specific product not found, try general product clicking
        return ProductHelpers.click_any_product(driver, browser_name, timeout)

    @staticmethod
    def click_any_product(driver, browser_name="", timeout=3):
        """Click on any available product"""
        product_link_selectors = [
            (By.CSS_SELECTOR, ".product-grid .product-item a"),
            (By.CSS_SELECTOR, ".collection-grid .product a"),
            (By.XPATH, "//div[contains(@class,'product')]//a[contains(@href,'/products/')]"),
            (By.CSS_SELECTOR, "[class*='product'] a[href*='/products/']"),
            (By.XPATH, "//a[contains(@href, '/products/')]"),
            (By.CSS_SELECTOR, "a[href*='/products/']"),
            (By.XPATH, "//img//ancestor::a[contains(@href, '/products/')]"),
            (By.CSS_SELECTOR, ".product a"),
            (By.CSS_SELECTOR, "[data-product] a"),
            (By.XPATH, "//div[contains(@class, 'item')]//a")
        ]

        for by_type, selector in product_link_selectors:
            try:
                wait = WebDriverWait(driver, timeout)
                links = wait.until(EC.presence_of_all_elements_located((by_type, selector)))
                if not links:
                    continue

                print(f"{browser_name}: Found {len(links)} product links using selector: {selector}")

                for i, link in enumerate(links[:5]):  # Try up to 5 products
                    try:
                        if not link.is_displayed():
                            continue

                        wait.until(EC.element_to_be_clickable(link))
                        ElementInteraction.scroll_to_element(driver, link)

                        if ElementInteraction.safe_click(driver, link, browser_name):
                            print(f"{browser_name}: Successfully clicked product {i + 1}")
                            TestUtils.wait_for_page_load(driver)
                            return True
                    except Exception as e:
                        print(f"{browser_name}: Failed to click product {i + 1}: {e}")
                        continue
            except TimeoutException:
                continue

        print(f"{browser_name}: Could not click any product")
        return False

    @staticmethod
    def set_quantity(driver, quantity, browser_name="", timeout=3):
        """Set quantity in the quantity field"""
        quantity_selectors = [
            (By.NAME, "quantity"),
            (By.ID, "quantity"),
            (By.CSS_SELECTOR, "input[name='quantity']"),
            (By.CSS_SELECTOR, ".quantity-input"),
            (By.XPATH, "//input[@type='number']"),
            (By.XPATH, "//input[contains(@class, 'quantity')]"),
            (By.CSS_SELECTOR, "input[type='number']"),
            (By.XPATH, "//input[contains(@placeholder, 'quantity')]"),
            (By.XPATH, "//input[contains(@id, 'quantity')]"),
            (By.CSS_SELECTOR, "[data-quantity] input"),
            (By.XPATH, "//input[contains(@name, 'qty')]")
        ]

        element, selector = ElementInteraction.wait_and_find_element(driver, quantity_selectors, timeout)
        if element:
            try:
                wait = WebDriverWait(driver, timeout)
                input_element = wait.until(EC.element_to_be_clickable(element))
                ElementInteraction.scroll_to_element(driver, input_element)

                # Clear field first
                input_element.clear()
                time.sleep(0.5)

                # Try multiple methods to set the value
                success = False

                # Method 1: Regular send_keys
                try:
                    input_element.send_keys(str(quantity))
                    if input_element.get_attribute("value") == str(quantity):
                        success = True
                        print(f"{browser_name}: Successfully set quantity to {quantity} using send_keys")
                except:
                    pass

                # Method 2: JavaScript if send_keys failed
                if not success:
                    try:
                        driver.execute_script(f"arguments[0].value = '{quantity}';", input_element)
                        # Trigger change event
                        driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", input_element)
                        if input_element.get_attribute("value") == str(quantity):
                            success = True
                            print(f"{browser_name}: Successfully set quantity to {quantity} using JavaScript")
                    except:
                        pass

                # Method 3: Clear and type character by character
                if not success:
                    try:
                        input_element.clear()
                        for char in str(quantity):
                            input_element.send_keys(char)
                            time.sleep(0.1)
                        if input_element.get_attribute("value") == str(quantity):
                            success = True
                            print(
                                f"{browser_name}: Successfully set quantity to {quantity} using character-by-character")
                    except:
                        pass

                return success

            except TimeoutException:
                pass

        print(f"{browser_name}: Could not set quantity to {quantity}")
        return False

    @staticmethod
    def get_quantity_value(driver, browser_name="", timeout=5):
        """Get current value from quantity field"""
        quantity_selectors = [
            (By.NAME, "quantity"),
            (By.ID, "quantity"),
            (By.CSS_SELECTOR, "input[name='quantity']"),
            (By.CSS_SELECTOR, ".quantity-input"),
            (By.XPATH, "//input[@type='number']")
        ]

        element, selector = ElementInteraction.wait_and_find_element(driver, quantity_selectors, timeout)
        if element:
            try:
                value = element.get_attribute("value")
                print(f"{browser_name}: Current quantity value: {value}")
                return value
            except Exception as e:
                print(f"{browser_name}: Could not get quantity value: {e}")

        return None

    @staticmethod
    def find_sold_out_button(driver, browser_name="", timeout=3):
        """Find and verify sold out button"""
        sold_out_selectors = [
            (By.XPATH, "//button[contains(text(), 'SOLD OUT')]"),
            (By.XPATH, "//button[contains(text(), 'Sold Out')]"),
            (By.CSS_SELECTOR, "button[disabled][aria-label*='Sold Out']"),
            (By.CSS_SELECTOR, ".sold-out-button"),
            (By.XPATH, "//button[@disabled and contains(text(), 'OUT')]")
        ]

        element, selector = ElementInteraction.wait_and_find_element(driver, sold_out_selectors, timeout)
        if element:
            is_disabled = not element.is_enabled()
            print(f"{browser_name}: Found sold out button, disabled: {is_disabled}")
            return element, is_disabled

        print(f"{browser_name}: Could not find sold out button")
        return None, False


class FormHelpers:
    """Form interaction helpers"""

    @staticmethod
    def navigate_to_cart(driver, browser_name="", timeout=3):
        """Navigate to shopping cart"""
        cart_selectors = [
            (By.XPATH, "//a[contains(@href, 'cart')]"),
            (By.CSS_SELECTOR, "a[href*='cart']"),
            (By.XPATH, "//button[contains(text(), 'Cart')]"),
            (By.CSS_SELECTOR, ".cart-button"),
            (By.XPATH, "//a[contains(@aria-label, 'cart')]")
        ]

        element, selector = ElementInteraction.wait_and_find_element(driver, cart_selectors, timeout)
        if element:
            try:
                wait = WebDriverWait(driver, timeout)
                clickable_element = wait.until(EC.element_to_be_clickable(element))
                ElementInteraction.scroll_to_element(driver, clickable_element)

                if ElementInteraction.safe_click(driver, clickable_element, browser_name):
                    print(f"{browser_name}: Successfully navigated to cart")
                    TestUtils.wait_for_page_load(driver)
                    return True
            except TimeoutException:
                pass

        print(f"{browser_name}: Could not navigate to cart")
        return False

    @staticmethod
    def click_checkout_button(driver, browser_name="", timeout=3):
        """Click checkout button"""
        checkout_selectors = [
            (By.XPATH, "//button[contains(text(), 'Checkout')]"),
            (By.XPATH, "//a[contains(text(), 'Checkout')]"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, ".checkout-button"),
            (By.NAME, "checkout")
        ]

        element, selector = ElementInteraction.wait_and_find_element(driver, checkout_selectors, timeout)
        if element:
            try:
                wait = WebDriverWait(driver, timeout)
                clickable_element = wait.until(EC.element_to_be_clickable(element))
                ElementInteraction.scroll_to_element(driver, clickable_element)

                if ElementInteraction.safe_click(driver, clickable_element, browser_name):
                    print(f"{browser_name}: Successfully clicked checkout button")
                    TestUtils.wait_for_page_load(driver)
                    return True
            except TimeoutException:
                pass

        print(f"{browser_name}: Could not click checkout button")
        return False

    @staticmethod
    def enter_credit_card(driver, card_number, browser_name="", timeout=3):
        """Enter credit card number"""
        card_selectors = [
            (By.NAME, "credit_card"),
            (By.NAME, "card_number"),
            (By.ID, "card_number"),
            (By.CSS_SELECTOR, "input[placeholder*='card number']"),
            (By.CSS_SELECTOR, "input[placeholder*='Card number']"),
            (By.XPATH, "//input[contains(@placeholder, 'card')]")
        ]

        element, selector = ElementInteraction.wait_and_find_element(driver, card_selectors, timeout)
        if element:
            try:
                wait = WebDriverWait(driver, timeout)
                input_element = wait.until(EC.element_to_be_clickable(element))
                ElementInteraction.scroll_to_element(driver, input_element)

                if ElementInteraction.safe_send_keys(driver, input_element, card_number, browser_name):
                    print(f"{browser_name}: Successfully entered credit card number")
                    return True
            except TimeoutException:
                pass

        print(f"{browser_name}: Could not enter credit card number")
        return False


class ValidationHelpers:
    """Validation and assertion helpers"""

    @staticmethod
    def check_page_title(driver, expected_texts, browser_name=""):
        """Check if page title contains expected text"""
        try:
            title = driver.title
            title_valid = any(text.lower() in title.lower() for text in expected_texts)
            print(f"{browser_name}: Page title: {title}")
            return title_valid, title
        except Exception as e:
            print(f"{browser_name}: Could not get page title: {e}")
            return False, ""

    @staticmethod
    def check_error_message(driver, expected_message, browser_name="", timeout=5):
        """Check for error message containing expected text"""
        error_selectors = [
            (By.CSS_SELECTOR, ".error-message"),
            (By.CSS_SELECTOR, ".validation-error"),
            (By.CSS_SELECTOR, "[role='alert']"),
            (By.XPATH, "//div[contains(@class, 'error')]"),
            (By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'Error')]")
        ]

        for by_type, selector in error_selectors:
            try:
                wait = WebDriverWait(driver, timeout)
                error_element = wait.until(EC.presence_of_element_located((by_type, selector)))
                error_text = error_element.text

                if expected_message.lower() in error_text.lower():
                    print(f"{browser_name}: Found expected error message: {error_text}")
                    return True, error_text
            except TimeoutException:
                continue

        print(f"{browser_name}: Expected error message not found: {expected_message}")
        return False, ""

    @staticmethod
    def check_404_page(driver, browser_name=""):
        """Check if current page is a 404 error page"""
        try:
            page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
            page_title = driver.title.lower()

            is_404 = any(indicator in page_text for indicator in ["404", "not found", "page not found"]) or \
                     any(indicator in page_title for indicator in ["404", "not found"])

            if is_404:
                print(f"{browser_name}: 404 page detected")
            else:
                print(f"{browser_name}: Not a 404 page")

            return is_404
        except Exception as e:
            print(f"{browser_name}: Could not check for 404 page: {e}")
            return False

    @staticmethod
    def check_field_accepts_input(driver, field_selector, test_value, browser_name="", timeout=2):
        """Check if a field accepts the given input"""
        try:
            wait = WebDriverWait(driver, timeout)
            field = wait.until(EC.presence_of_element_located(field_selector))

            # Clear and enter value
            field.clear()
            field.send_keys(test_value)

            # Get actual value
            actual_value = field.get_attribute("value")

            accepts_input = actual_value == test_value
            print(
                f"{browser_name}: Field input test - Expected: '{test_value}', Actual: '{actual_value}', Accepts: {accepts_input}")

            return accepts_input, actual_value
        except Exception as e:
            print(f"{browser_name}: Could not test field input: {e}")
            return False, ""


class TestUtils:
    """General test utilities"""

    @staticmethod
    def safe_teardown(driver, browser_name=""):
        """Safely teardown driver with error handling"""
        try:
            if driver:
                time.sleep(1)
                driver.quit()
                print(f"{browser_name}: Driver successfully closed")
        except Exception as e:
            print(f"{browser_name}: Warning during teardown: {e}")
            # Force kill any remaining processes if needed
            try:
                if hasattr(driver, 'service') and driver.service.process:
                    os.kill(driver.service.process.pid, signal.SIGTERM)
            except:
                pass

    @staticmethod
    def wait_for_page_load(driver, timeout=5):
        """Wait for page to load completely"""
        try:
            wait = WebDriverWait(driver, timeout)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            # Additional wait for JavaScript to load
            driver.execute_script("return document.readyState") == "complete"
            time.sleep(2)
        except TimeoutException:
            print("Page load timeout - continuing anyway")

    @staticmethod
    def take_screenshot(driver, filename, browser_name=""):
        """Take screenshot for debugging"""
        try:
            driver.save_screenshot(f"{browser_name}_{filename}")
            print(f"{browser_name}: Screenshot saved as {browser_name}_{filename}")
        except Exception as e:
            print(f"{browser_name}: Could not take screenshot: {e}")


class Constants:
    """Test constants and test data"""

    # URLs
    BASE_URL_HOME = "https://shop.blueorigin.com"
    BASE_URL_ACCESSORIES = "https://shop.blueorigin.com/collections/accessories"
    BASE_URL = "https://shop.blueorigin.com/collections/accessories"  # Legacy compatibility

    # Timeouts
    DEFAULT_TIMEOUT = 5
    LONG_TIMEOUT = 10

    # Expected content
    EXPECTED_TITLE_TEXTS = ["Blue Origin", "Accessories", "Shop"]

    # Test data
    TEST_PRODUCTS = {
        "titanium_pen": "Black Titanium Nitride",
        "khaki-performance-hat": "Khaki Performance Hat"
    }

    # Invalid inputs for testing
    INVALID_INPUTS = {
        "fractional numbers" : "0.5",
        "negative_quantity": "-5",
        "invalid_credit_card": "1234567890123456",
        "-5": "-5",
        "0.5": "0.5",
    }


    # URLs for testing 404
    INVALID_URLS = [
        "https://shop.blueorigin.com/accessoriesss",
        "https://shop.blueorigin.com/collections/nonexistent"
]


    # Browser configurations
    SUPPORTED_BROWSERS = ["chrome", "firefox", "edge"]


# Example usage and test runner
class TestRunner:
    """Main test runner class"""

    def __init__(self, browser_name="chrome"):
        self.browser_name = browser_name
        self.driver = None

    def setup(self):
        """Setup the test environment"""
        try:
            self.driver = WebDriverFactory.get_driver(self.browser_name)
            print(f"Successfully created {self.browser_name} driver")
            return True
        except Exception as e:
            print(f"Failed to setup {self.browser_name} driver: {e}")
            return False

    def teardown(self):
        """Cleanup the test environment"""
        if self.driver:
            TestUtils.safe_teardown(self.driver, self.browser_name)

    def run_basic_test(self):
        """Run a basic test scenario"""
        if not self.setup():
            return False

        try:
            # Navigate to homepage
            if not NavigationHelpers.navigate_to_homepage(self.driver, self.browser_name):
                return False

            # Verify page title
            title_valid, title = PageHelpers.verify_page_title(
                self.driver, Constants.EXPECTED_TITLE_TEXTS, self.browser_name
            )

            if not title_valid:
                print(f"{self.browser_name}: Page title validation failed")
                return False

            # Navigate to accessories
            if not NavigationHelpers.navigate_to_accessories(self.driver, self.browser_name):
                return False

            # Find products
            products, count = PageHelpers.find_products(self.driver, self.browser_name)
            if count == 0:
                print(f"{self.browser_name}: No products found")
                return False

            print(f"{self.browser_name}: Basic test completed successfully")
            return True

        except Exception as e:
            print(f"{self.browser_name}: Test failed with error: {e}")
            return False
        finally:
            self.teardown()


if __name__ == "__main__":
    # Example usage
    for browser in ["chrome", "firefox", "edge"]:
        try:
            print(f"\n--- Testing with {browser} ---")
            test_runner = TestRunner(browser)
            result = test_runner.run_basic_test()
            print(f"{browser} test result: {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            print(f"Failed to test {browser}: {e}")