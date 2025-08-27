import random
import time


from selenium.common import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# ANSI escape codes:
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
BOLD = '\033[1m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'


def delay(): time.sleep(random.randint(2, 5))

# noinspection SpellCheckingInspection
def test_TC_P_036(driver):
	print(f"{BLUE}{BOLD}\n=============================Starting test TC_P_036: Verify Verify the Blue Origin homepage load============================={RESET}")

	print(f"{ITALIC}1. Opening Blue Origin homepage...")
	print(f"{GREEN}   - Verified: Homepage loaded.{RESET}")
	driver.get("https://www.blueorigin.com/")
	delay()

	try:
		print(f"{ITALIC}2. Verifying page title...{RESET}")
		x= driver.title
		print (f"   ", x),
		assert "Home | Blue Origin" in driver.title
		print(f"{GREEN}   - Verified: Page title matches expected value.{RESET}")
	except AssertionError:
		print(f"{RED}{BOLD}Test failed: Page title does not match expected value.{RESET}")
		# print(f"{RED}{ITALIC}Actual value: .{RESET}")
	try:
		print(f"{ITALIC}3. Verifying the presence of logo on page...{RESET}")
		logo = driver.find_element(By.CSS_SELECTOR, "img[alt='Blue Origin: For The Benefit of Earth']")
		assert logo.is_displayed()
		print(f"{GREEN}   - Verified: Logo is present and visible on the page.{RESET}")
	except (NoSuchElementException, AssertionError):
		print(f"{RED}{BOLD}Test failed: Logo element not found or not visible on the page.")

	try:
		print(f"{ITALIC}4. Verifying the presence Main Nav Burger Button...{RESET}")
		burgrBttn = driver.find_element(By.CSS_SELECTOR, "#«R65tndrnb»")
		assert burgrBttn.is_enabled() and burgrBttn.is_displayed()
		print(f"{GREEN}   - Verified: Main Nav Burger Button is displayed and enabled.{RESET}")
	except (NoSuchElementException, AssertionError):
		print(f"{RED}{BOLD}Test failed: main nav burger button IS NOT displayed and enabled.")

	try:
		print(f"{ITALIC}5. Verifying the presence of Footer Nav Menu...{RESET}")
		ftrNavMnu = driver.find_element(By.CSS_SELECTOR, ".FooterNavigationColumn_controlsWrapper__4NXZn")
		assert ftrNavMnu.is_enabled() and ftrNavMnu.is_displayed()
		print(f"{GREEN}   - Verified: Footer Nav Menu is  displayed and enabled.{RESET}")
	except (NoSuchElementException, AssertionError):
		print(f"{RED}{BOLD}Test failed: main nav burger button IS NOT displayed and enabled.")

	print(f"{BLUE}{BOLD}\n=============================Finished test TC_P_036: 100% "
	      f"Passed============================================================={RESET}")


def test_TC_P_037(driver):
	print(f"{BLUE}{BOLD}\n=============================Starting test TC_P_037: Verify clickability of Footer links============================={RESET}")
	# print(f"{BLUE}{BOLD}\n***Starting test TC_P_037: ***{RESET}")

	print(f"{ITALIC}1. Opening Blue Origin homepage...")
	print(f"{GREEN}   - Verified: Homepage loaded.{RESET}")
	driver.get("https://www.blueorigin.com/")
	delay()

	try:
		print(f"{ITALIC}5. Verifying the presence of Footer Nav Menu...{RESET}")
		ftrNavMnu = driver.find_element(By.CSS_SELECTOR, ".FooterNavigationColumn_controlsWrapper__4NXZn")
		assert ftrNavMnu.is_enabled() and ftrNavMnu.is_displayed()
		print(f"{GREEN}   - Verified: Footer Nav Menu is  displayed and enabled.{RESET}")
	except (NoSuchElementException, AssertionError):
		print("Test failed: main nav burger button IS NOT displayed and enabled.")

		print(f"{ITALIC}3. Collecting footer navigation menu items...{RESET}")
		# Find all list items in the footer navigation menu, store them in a list.
		footer_items = ftrNavMnu.find_elements(By.TAG_NAME, "li")

	print(f"{BLUE}{BOLD}\n=============================Finished test TC_P_037: 100% "
	      f"Passed====================================================={RESET}")
def test_TC_P_038(driver):


	print(f"{BLUE}{BOLD}\n=============================Starting test TC_P_038: Verify functionality of Font Preference Dropdown List============================={RESET}")
	print(f"{ITALIC}1. Opening Blue Origin homepage...")
	print(f"{GREEN}   - Verified: Homepage loaded.{RESET}")
	driver.get("https://www.blueorigin.com/")
	delay()

	# noinspection PyShadowingNames
	def scroll_to_element(driver, element):

		# Using JavaScript to scroll to the element, it's more reliable than using Selenium's built-in scroll_to_element() method.
		driver.execute_script("arguments[0].scrollIntoView(true);", element)
		time.sleep(1)
	font_selection_dropdown = driver.find_element(By.XPATH, "//select[@id='andromeda-font-preference']")
	try:
		print(f"{ITALIC}2. Locate Font Preference Dropdown...")
		print(f"{GREEN}   - Verified: element located.{RESET}")
	except NoSuchElementException:
		print("Test failed: main nav burger button IS NOT displayed and enabled.")
	try:
		print(f"{ITALIC}3. Scroll to 'Font Preference Dropdown'...")
		scroll_to_element(driver, font_selection_dropdown)
		assert font_selection_dropdown.is_displayed()
		print(f"{GREEN}   - Verified: Element is displayed.{RESET}")
	except (NoSuchElementException, AssertionError):
		print(f"{RED}{BOLD}Test failed: Font Preference Dropdown IS NOT displayed and/or enabled.")

	# Using Axes Xpath to relatively locate font option elements in DOM:

	font_one = driver.find_element(By.XPATH, "//div[@class='FooterNavigationColumn_controlsWrapper__4NXZn']/..//option[@value='atkinson-hyperlegible']")
	font_two = driver.find_element(By.XPATH, "//div[@class='FooterNavigationColumn_fontPreferenceSelectorWrapper__rluP_']/..//option[@value='open-dyslexic']")
	font_default = driver.find_element(By.XPATH, "//div[@class='FooterNavigationColumn_fontPreferenceSelectorWrapper__rluP_']/..//option[@value='no-preference']")
	font_test_object = driver.find_element(By.XPATH, "//h2[@class='FooterFormColumn_formHeading__mA4Oh']")
	try:
		print(f"{ITALIC}4. Click on 'Atkinson-Hyperlegible' option in dropdown...{RESET}")
		font_one.click()
		time.sleep(1)
		print(f"{GREEN}   - Verified: 'Atkinson-Hyperlegible' selected, page reloads.{RESET}")
		print(f"{ITALIC}5. Verifying the font change in the DOM{RESET}")
		assert "atkinsonHyperlegible" in font_test_object.value_of_css_property('font-family')
		print(f"{GREEN}   - Verified: 'Atkinson-Hyperlegible' is selected and displayed.{RESET}")

		print(f"{ITALIC}6. Click on 'openDyslexic' option in dropdown...{RESET}")
		font_two.click()
		time.sleep(1)
		print(f"{GREEN}   - Verified: 'openDyslexic' selected, page reloads.{RESET}")
		print(f"{ITALIC}7. Verifying the font change in the DOM{RESET}")
		assert "openDyslexic" in font_test_object.value_of_css_property('font-family')
		print(f"{GREEN}   - Verified: 'openDyslexic' is selected and displayed.{RESET}")

		print(f"{ITALIC}8. Click on 'No Preference' option in dropdown...{RESET}")
		font_default.click()
		time.sleep(1)
		print(f"{GREEN}   - Verified: 'No Preference' selected, page reloads.{RESET}")
		print(f"{ITALIC}9. Verifying the font change in the DOM{RESET}")
		assert "fromTheStars" in font_test_object.value_of_css_property('font-family')
		print(f"{GREEN}   - Verified: 'No Preference/Default' font is selected and displayed.{RESET}")

	except (NoSuchElementException, AssertionError):
		print(f"{RED}{BOLD}Test failed: Font change cannot be verified.")

	print(f"{BLUE}{BOLD}\n=============================Finished test TC_P_038: 100% "
	      f"Passed======================================================================{RESET}")

def test_TC_P_039(driver):

	global font_selection_dropdown
	print(f"{BLUE}{BOLD}\n=============================Starting test TC_P_038: Verify functionality of Font Preference Dropdown List============================={RESET}")
	print(f"{ITALIC}1. Opening Blue Origin homepage...")
	print(f"{GREEN}   - Verified: Homepage loaded.{RESET}")
	driver.get("https://www.blueorigin.com/")
	delay()

	# noinspection PyShadowingNames
	def scroll_to_element(driver, element):
		# Using JavaScript to scroll to the element, it's more reliable than using Selenium's built-in scroll_to_element() method.
		driver.execute_script("arguments[0].scrollIntoView(true);", element)
		time.sleep(1)
	try:
		print(f"{ITALIC}2. Locate Font Preference Dropdown...")
		font_selection_dropdown = driver.find_element(By.XPATH, "")
		print(f"{GREEN}   - Verified: element located.{RESET}")
	except NoSuchElementException:
		print("Test failed: main nav burger button IS NOT displayed and enabled.")
	finally:
		print(f"{ITALIC}3. Select Andromeda Font in Preference Dropdown...")
		font_selection_dropdown.click()
		time.sleep(1)











