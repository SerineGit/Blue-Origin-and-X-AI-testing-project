import random
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('headless')
    # chrome_options.add_argument("disable-gpu")
    options.add_argument("--eager-resource-limits")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(4)
    try:
        yield driver
    finally:
        driver.quit()


def delay():
    def _delay(min_s=2, max_s=5):
        time.sleep(random.randint(min_s, max_s))
    return _delay

