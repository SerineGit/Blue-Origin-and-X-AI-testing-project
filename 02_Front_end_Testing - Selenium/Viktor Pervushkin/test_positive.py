from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from helpers import get_driver, Helper
from locators import (
    nav_toggle, URLs, title, elements, buttons, header)
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

def test_p_041(helper):
    print(" TEST CASE 041"
          "Verify video playback functionality")
    helper.driver.get(URLs.home_url)
    helper.click(nav_toggle.burger_menu,5)
    helper.delay(2,4)
    helper.click(nav_toggle.nav_new_shepard,5)
    helper.delay(1,3)

    #scrolling down
    helper.scroll(buttons.explore_the_crew,5)
    helper.delay(3,5)

    #clicking on explore the crew button
    try:
        helper.wait_to_click(buttons.explore_the_crew,10)
        helper.delay(5,10)
        print("Clicked on Explore Crew Button")
    except:
        pytest.fail("unable to click on 'Explore The Crew")

    #switching to Iframe
    try:
        iframe = helper.wait(elements.video_iframe, 10)
        helper.driver.switch_to.frame(iframe)
        print("Switched into video iframe")
        #wait to click
    except Exception as e:
        pytest.fail(f"Error in iframe: {e}")
    #waiting for YT player to load
    try:
        helper.wait(elements.video_player, 10)
        helper.delay(10,15)
        print("#movie_player found — YouTube player loaded!")
    except Exception as e:
        pytest.fail(f"Failed to find #movie_player: {e}")

    try:
        helper.click(buttons.play_button, 10)
        print("Clicked on Play Button")
        helper.delay(10,15)
    except:
        pytest.fail("Can't click")
        # helper.driver.switch_to.default_content()
        pytest.fail("Can' load Youtube video")
    #validate video playback by checking class of the video
    player = helper.driver.find_element(By.ID, "movie_player")
    classes = player.get_attribute("class")
    if "playing-mode" in classes:
        print("Video is playing!")
    else:

        pytest.fail("Video is not playing")


    helper.driver.switch_to.default_content()

def test_p_042(helper):
    print("TEST CASE 047."
          "Validate URL address of 'New Shepard' and confirm a presence of a unique element")

    helper.driver.get(URLs.home_url)
    helper.hover(header.vehicle)
    helper.click(header.new_shep,5)
    helper.assert_url(URLs.new_shepard_url)
    helper.delay(2,4)
    helper.is_element_present(header.new_shep_unique_elem,5)
    print(f"unique element is present")

def test_p_043(helper):
    print("TEST CASE 048 "
          "Verify that dropdown manu appears after hovering over Vehicles, Systems, and About  ")

    helper.driver.get(URLs.home_url)
    # helper.hover(header.vehicle)
    # print("hovered over 'Vehicle' successfully")
    # helper.delay(1, 3)
    # helper.is_element_present(header.vehicle_dropdown,5)
    # #testing Systems dropdown
    # helper.hover(header.systems)
    # print("Hovered over 'Systems' successfully")
    # helper.delay(1, 3)
    # helper.is_element_present(header.system_dropdown,5)
    # #testing About dropdown
    # helper.hover(header.systems)
    # helper.delay(1, 3)
    # print("Hovered over 'About' successfully")
    # helper.is_element_present(header.about, 5)

    header_items = [
        (header.vehicle, header.vehicle_dropdown, "Vehicles"),
        (header.systems, header.system_dropdown, "Systems"),
        (header.about, header.about_dropdown, "About")
    ]
    for locator, dropdown_menu, name in header_items:
        print(f"Testing:{name}")
        try:
            helper.hover(locator)
            helper.delay(2,4)
            print(f"successfully hover over:{name}")
            helper.is_element_present(dropdown_menu,10)
        except Exception as e:
            raise AssertionError(f"Failed to navigate to {name}: {str(e)}")

def test_p_044(helper):
    print("Validate consistent home navigation from all hamburger menu destinations")
    helper.driver.get(URLs.home_url)
    helper.click(nav_toggle.burger_menu, 3)
    helper.delay(1, 3)

    nav_items = [
        (nav_toggle.nav_new_shepard, "New Shepard"),
        (nav_toggle.nav_new_glenn, "New Glenn"),
        (nav_toggle.nav_blue_moon, "Blue Moon"),
        (nav_toggle.nav_blue_ring,  "Blue Ring"),
        (nav_toggle.nav_engines, "Engines"),
        (nav_toggle.nav_destinations,  "Destinations"),
        (nav_toggle.nav_motion_ctrl, "Motion control"),
        (nav_toggle.nav_exploration_system,  "Exploration system"),
        (nav_toggle.nav_about_blue,  "About"),
        (nav_toggle.nav_sustainability, "Sustainability"),
        (nav_toggle.nav_news, "News"),
        (nav_toggle.nav_gallery,  "Gallery"),
        (nav_toggle.nav_career,  "Career "),
        (nav_toggle.nav_shop,  "Shop")
    ]
    for locator, name in nav_items:
        print(f"Navigating to :{name}")

        item = helper.wait_for_clickable(locator, 10)  # waiting for an element to appear
        item.click()
        print(f"Clicked on {name}")
        helper.delay(3,5)


        if helper.click(nav_toggle.home_button,3):
            print(f"Clicked on Home Logo")
        elif helper.click(nav_toggle.home_button2,3):
            print(f"Had to use another locator:{locator}")
        elif helper.click(nav_toggle.home_button3,3):
            print(f"Had to use another locator:{locator}")
        else:
            print("Failed to click on Home Button")

        helper.delay(5,7)
        if helper.driver.current_url != URLs.home_url:
            print(f"FAILED! Wasn't able to return to a home page from:{helper.driver.current_url}")
        else:
            print(f"Successfully returned to Home page {helper.driver.current_url}")

        print("---------------------------------------------------------")
        # wait for a home page to load
        helper.delay(5, 7)
        try:
            #helper.wait_for_clickable(nav_toggle.burger_menu, 15)
            helper.click(nav_toggle.burger_menu, 3)  # clicking on burger menu
        except TimeoutException:
            print("BURGER MENU NOT FOUND!")
            print("Current URL:", helper.driver.current_url)
            print("Page title:", helper.driver.title)
            # Take screenshot for debugging
            helper.driver.save_screenshot("debug_burger_menu_missing.png")
            raise
        helper.delay(1, 3)
        print("--------Clicked on burger menu---------")

def test_045(helper):
    print("Validate that the URL of every navigation module matches the expected URL/Validate burger menu functionality")
    helper.driver.get(URLs.home_url)
    helper.click(nav_toggle.burger_menu,3)
    helper.delay(1,3)
    nav_items = [
        (nav_toggle.nav_new_shepard, URLs.new_shepard_url, title.new_shepard, "New Shepard"),
        (nav_toggle.nav_new_glenn, URLs.new_glenn_url, title.new_glenn, "New Glenn"),
        (nav_toggle.nav_blue_moon, URLs.blue_moon_url, title.blue_moon, "Blue Moon"),
        (nav_toggle.nav_blue_ring, URLs.blue_ring_url, title.blue_ring, "Blue Ring"),
        (nav_toggle.nav_engines, URLs.engines_url, title.engines, "Engines"),
        (nav_toggle.nav_destinations, URLs.destinations_url, title.destinations, "Destinations"),
        (nav_toggle.nav_motion_ctrl,URLs.motion_ctr_url, title.motion_ctrl, "Motion control"),
        (nav_toggle.nav_exploration_system,URLs.exploration_sys_url, title.exploration_system, "Exploration system"),
        (nav_toggle.nav_about_blue, URLs.about_blue_url, title.about_blue, "About"),
        (nav_toggle.nav_sustainability, URLs.sustainability_url, title.sustainability, "Sustainability"),
        (nav_toggle.nav_news, URLs.news_url, title.news, "News"),
        (nav_toggle.nav_gallery, URLs.gallery_url, title.gallery, "Gallery"),
        (nav_toggle.nav_career,URLs.careers_url, title.career, "Career "),
        (nav_toggle.nav_shop, URLs.shop_url, title.shop, "Shop")
        ]

    for locator, expected_url, expected_title, name in nav_items: # this loop is unpacking nav items
        print(f"Navigating to {name}")
        try:

            #waiting for a target item to appear
            item = helper.wait_for_clickable(locator, 10) # waiting for an element to appear
            item.click()
            print(f"Clicked on {name}")
            #verifying URL
            helper.delay(3,5)
            helper.assert_url(expected_url)
            helper.assert_title(expected_title)
            helper.delay(3, 5)
            #return 2 home page
            helper.driver.get(URLs.home_url)
            print("--------Returned to Home Page---------")
            #wait for a home page to load
            helper.wait_for_clickable(nav_toggle.burger_menu,15)
            helper.click(nav_toggle.burger_menu,3)  # clicking on burger menu
            helper.delay(1, 3)
            print("Clicked on burger menu")

        except Exception as e:
            raise AssertionError(f"Failed to navigate to {name}: {str(e)}")
