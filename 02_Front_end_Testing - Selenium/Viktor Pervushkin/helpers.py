import os
import random
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService, Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions



def get_driver(browser):

    """setting up chrome as uc driver"""
    #
    # #adding arguments to simulate human behaviour
    # options = ChromeOptions()
    # options.add_argument("--start-maximized")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    # options.add_argument("--disable-infobars")  #disable chrome is controlled mode
    #
    # # Initialize undetected chromedriver
    # driver = uc.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    #
    # # Set implicit wait for all elements (so it can wait for elements without needing explicit delays in your tests)
    # driver.implicitly_wait(10)
    #
    # return driver
    browser=browser.lower()
    if browser == "chrome":
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--kiosk")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.implicitly_wait(10)

    elif browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--start-maximized")
        driver_path = r'C:\drivers\msedgedriver.exe'
        service = Service(executable_path=driver_path)

        driver = webdriver.Edge(service=service, options=options)
        driver.maximize_window()
        return driver


    return driver


# encapsulating all helper functions in one class using constructor method
class Helper:
    def __init__(self,driver):
        self.driver = driver

    def click(self,locator,timeout):
        try:
            #normal Selenium click
            web_element = self.driver.find_element(*locator)
            web_element.click()
            return True
        except:
            print(f" Normal click failed. Using JS click fallback.")
            try:
                #wait for element to be clickable using the ORIGINAL locator
                web_element = self.wait_for_clickable(locator, timeout)
                #scroll into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", web_element)
                #JS click
                self.driver.execute_script("arguments[0].click();", web_element)
                print(f"JS click successful on: {locator}")
                return True
            except Exception as e2:
                print(f"JS click also failed for {locator}: {e2}")
                return False


    def scroll(self, locator, timeout):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator))
        self.driver.execute_script("""
        arguments[0].scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    """, element)
        print(f"Scrolled down to {locator}")

    def hover(self,element):
        element = self.driver.find_element(*element)
        action = ActionChains(self.driver)
        action.move_to_element(element).pause(2).perform()


    def enter_data(self,element,text):
        element = self.driver.find_element(*element)
        name_element = element.get_attribute("name")
        element.clear()
        element.send_keys(text)
        print(f"Entered {name_element}: {text}")

    def wait_to_click(self, locator,timeout):
        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
        try:
            element.click()
            print(f"click successful on: {locator}")
            return True
        except Exception as e:
            print(f" Normal click failed: {e}. Using JS click fallback.")

        try:
            print("Regular click failed.Using JS method")
            self.driver.execute_script("arguments[0].click();", element)
            print(f"JS click successful on: {locator}")
            return True
        except Exception as e2:
                print(f"JS click also failed for {locator}: {e2}")
                return False

    # def click_and_wait(self, element1_locator, element2_locator,timeout):
    #     element1 = self.driver.find_element(*element1_locator)
    #     element1.click()
    #     print(f"Clicked on :{element1}")
    #     element2 = (WebDriverWait(self.driver, timeout).until
    #                 (EC.element_to_be_clickable(element2_locator))
    #                 )
    #     element2.click()
    #     print(f"clicked on :{element2}")

    def assert_url(self, expected_url):
        actual_url = self.driver.current_url.strip().rstrip("/")
        expected_url = expected_url.strip().rstrip("/")
        if actual_url == expected_url:
            print(f"URL match:{expected_url}")
        else:
            print(f"URL mismatch. Expected: {expected_url}, Got: {actual_url}")
            raise AssertionError(f"Expected {expected_url}, got {actual_url}")

    def assert_title(self, expected_title):
        actual_title = self.driver.title.strip().rstrip("/")
        expected_title = expected_title.strip().rstrip("/")
        if actual_title == expected_title:
            print(f"Title match:{expected_title}")
        else:
            print(f"Title mismatch. Expected:{expected_title}, Got:{actual_title}")
            raise AssertionError(f"Expected:{expected_title}, Got:{actual_title}")

    def assert_title_and_url(self,expected_url, expected_title):
        actual_url = self.driver.current_url.strip().rstrip("/")
        expected_url = expected_url.strip().rstrip("/")
        actual_title = self.driver.title.strip().rstrip("/")
        expected_title = expected_title.strip().rstrip("/")
        if actual_url == expected_url or actual_title == expected_title:
            print(f"Either URL or Title matched: URL = Expected: {expected_url}, Got: {actual_url}/"
                  f"TITLE = Expected:{expected_title}, Got:{actual_title}")
        else:
            print("Neither URL or Title matched: ")


    def delay(self, min_sec, max_sec):
        time.sleep(random.uniform(min_sec, max_sec))

    def wait_for_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait(self, locator, timeout):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def is_element_present(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            print(f"{locator} is present")
            return True
        except:
            return False

    def set_zoom_level(self, driver, zoom_percent):
        zoom = zoom_percent / 100
        driver.execute_script(f"document.body.style.zoom = '{zoom}';")
        return True









    





