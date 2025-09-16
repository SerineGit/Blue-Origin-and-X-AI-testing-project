from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from helpers import get_driver, Helper
from locators import (
    nav_toggle, URLs, buttons, header, field, forms)
import pytest

@pytest.fixture(scope="function", params=["chrome","firefox","edge"])
def helper(request):
    driver = get_driver(request.param)
    helper = Helper(driver)
    yield helper
    try:
        driver.quit()
    except Exception:
        pass

def test_n_041(helper):
    print("Validate email input field enforces format constraints under invalid input conditions")
    helper.driver.get(URLs.home_url)
    helper.scroll(field.footer_email,5)
    helper.delay(2,4)
    helper.enter_data(field.footer_email, "jane.austin")
    helper.delay(2,4)
    helper.wait_to_click(field.check_box,3)
    helper.delay(2, 4)
    helper.click(field.submit_button, 3)
    helper.delay(2, 4)
    if helper.is_element_present(field.subscribe_message):
        print("The system accepted wrong email format without a domain")
        assert False, "Invalid email was accepted — validation failed!"
    else:
        print("The system didn't accept wrong email format without a domain")

def test_n_042(helper):
    print("Verify mutual exclusivity and state management of concurrent dropdown menu interactions")
    helper.driver.get(URLs.home_url)
    helper.hover(header.vehicle)
    helper.click(header.vehicle,5)
    helper.is_element_present(header.vehicle_dropdown,5)
    helper.delay(2,4)
    if helper.click(header.vehicle,5):
        print("Clicked on 'Vehicle")
        #trying to hover over systems
        try:
            print("Attempting to hover over 'Systems' while 'Vehicle' dropdown is still open")
            helper.hover(header.systems)
            helper.delay(2, 4)
            print("Hovered over 'System'")
            dropdown= [
                (header.vehicle_dropdown, 'Vehicle dropdown menu'),
                (header.system_dropdown, 'Systems dropdown menu')
            ]
            for locator, name in dropdown:
                print(f"Testing{name}")
                helper.is_element_present(locator)
                helper.driver.save_screenshot("dropdownmenu_bug.png")
        except NoSuchElementException:
            print("Unable to locate the 'Systems'")
    else:
        print("Unable to display 2 dropdown menus after hovering")

def test_n_043(helper):
    print("Form Submission with Malformed and Non-Existent Data")
    helper.driver.get(URLs.home_url)
    helper.click(buttons.fly_to_space,5)
    helper.delay(2,4)
    helper.assert_url("https://www.blueorigin.com/new-shepard/fly")
    helper.click(buttons.purchase_seat,5)
    helper.assert_title_and_url("https://www.blueorigin.com/new-shepard/reserve-a-seat","Reserve a Seat | Blue Origin")
    helper.scroll(forms.form,5)
    helper.delay(3,5)
    #filling the form
    try:
        helper.enter_data(forms.first_name,"V")
    except NoSuchElementException:
        print("Element not found")

    try:
        helper.enter_data(forms.last_name,"P")
    except NoSuchElementException:
        print("Last Name not found")

    try:
        helper.enter_data(forms.email,"viktor@mail.com")
    except NoSuchElementException:
        print("Email not found")

    try:
        helper.enter_data(forms.phone_number,"12345678910111213141516")
    except NoSuchElementException:
        print("Phone Number not found")

    try:
        helper.enter_data(forms.address,"e7")
    except NoSuchElementException:
        print("Address Number not found")

    try:
        helper.enter_data(forms.city,"1")
        print("BUG!!! A one number accepted as a city")
    except:
        print("Input wasn't accepted")

    try:
        helper.click(forms.country,5)
        helper.delay(3,5)
        element = helper.driver.find_element(By.XPATH,"//div[@id='«Rk8mm9tndrnbH4»-option-Australia']")
        element.click()
        helper.delay(3, 5)
        print("Selected Australia")
    except:
        pass

    try:
        helper.click(forms.monthOfBirth,5)
        helper.delay(2,4)
        el = helper.driver.find_element(By.XPATH,"//div[@id='«Rcomm9tndrnbH4»-option-December']")
        el.click()
        helper.delay(2,4)
        print("Selected November")
    except:
        pass

    try:
        helper.click(forms.yearOfBirth,5)
        helper.delay(2,4)
        el = helper.driver.find_element(By.XPATH,"//div[@id='«Rkomm9tndrnbH4»-option-2007']")
        el.click()
        helper.delay(2,4)
        print("Selected 2007")
    except:
        pass
    #scrolling down
    helper.scroll(forms.tell_about_yourself,5)
    helper.delay(4,6)

    try:
        helper.click(forms.how_did_you_hear,5)
        el = helper.driver.find_element(By.XPATH,"//div[@id='«R2p6m9tndrnbH4»-option-FlightBroadcast']")
        el.click()
        helper.delay(2, 4)
        print("Selected Flight Broadcast")
    except:
        pass

    try:
        helper.enter_data(forms.tell_about_yourself,"       ")
        print("BUG!!! Accepted Spaces as an input")
    except:
        pass


    helper.delay(2,4)
    if helper.click(forms.acknowledge,5):
        helper.click(forms.confirm, 5)
    else:
        print("Can't click on Acknowledge button")
        helper.delay(2, 4)

    helper.click(buttons.submit, 5)

    helper.delay(5,6)

    helper.scroll(forms.success_message,5)
    helper.delay(5, 6)
    if helper.is_element_present(forms.success_message,5):
        print(" the form has accepted Malformed and Non-Existent Data")

def test_044(helper):
        #navigating to a fake URL
        helper.driver.get("https://www.blueorigin.com/this-page-does-not-exist")
        helper.delay(2,4)

        helper.assert_title("Not Found | Blue Origin")
        print(f"Page loaded with title: {helper.driver.title}")

        try:
            helper.is_element_present("//img[@alt='404']",5)
            print("Unique element 404 image is present")
        except:
             print("Could not read body text")
        #
        # Verify user can still navigate back to home
        try:
            #look for the Blue Origin logo (home link)
            home_logo = helper.wait_for_clickable(nav_toggle.home_button)
            home_logo.click()
            print("Clicked on home logo")
        except Exception as e:
            print(f"an error occurred : {e}")

        helper.assert_url(URLs.home_url)

def test_045(helper):
    print("Verify that the main content remains readable and properly structured when the browser is zoomed to 200% or more.")
    helper.driver.get(URLs.home_url)
    if helper.is_element_present(header.new_shep_next_flight):
        print("New Shepard header is present")
    else:
        pytest.fail()

    try:
        print("changing ZOOM to 250%")
        helper.delay(4,6)
        if helper.set_zoom_level(helper.driver,250 ):
            helper.is_element_present(header.new_shep_next_flight)
            print("PASSED!"
            "Unique element 'New Shepard' is present with 250% zoom")
        else:
            pass
            print("element isn't visible")
    except Exception as e:
        print(f"error has occurred {e}")

    try:
        print("changing ZOOM to 450%")
        helper.delay(4,6)
        if helper.set_zoom_level(helper.driver,450 ):
            helper.is_element_present(header.new_shep_next_flight)
            print("PASSED!"
            "Unique element 'New Shepard' is present with 450% zoom")
        else:
            pass
            print("element isn't visible")
    except Exception as e:
        print(f"error has occurred {e}")



























