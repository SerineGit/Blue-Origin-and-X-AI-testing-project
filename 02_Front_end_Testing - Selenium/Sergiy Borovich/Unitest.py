import time
import random
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService





def delay():
    time.sleep(random.randint(2, 5))



class ChromePositiveTestes(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        #options.page_load_strategy = 'eager'
        #options.add_argument("--disable-blink-features=AutomationControlled")
        #options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.maximize_window()


    def test_Positive_Starlink_TC_031(self):
        driver = self.driver
        print("Positive TC-031")
        driver.get("https://shop.blueorigin.com/")
        wait = WebDriverWait(driver, 10)
