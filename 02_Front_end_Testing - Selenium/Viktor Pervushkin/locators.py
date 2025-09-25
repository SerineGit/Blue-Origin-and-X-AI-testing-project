from selenium.webdriver.common.by import By


class URLs:
     # as strings
    home_url = 'https://www.blueorigin.com/'
    new_shepard_url = 'https://www.blueorigin.com/new-shepard'
    new_glenn_url = 'https://www.blueorigin.com/new-glenn'
    blue_moon_url = 'https://www.blueorigin.com/blue-moon'
    blue_ring_url = 'https://www.blueorigin.com/blue-ring'
    engines_url = 'https://www.blueorigin.com/engines'
    destinations_url = 'https://www.blueorigin.com/destinations'
    motion_ctr_url = 'https://www.blueorigin.com/motion-control'
    exploration_sys_url = 'https://www.blueorigin.com/exploration-systems'
    about_blue_url = 'https://www.blueorigin.com/about-blue'
    sustainability_url = 'https://www.blueorigin.com/sustainability'
    news_url ='https://www.blueorigin.com/news'
    gallery_url = 'https://www.blueorigin.com/news/gallery'
    careers_url = 'https://www.blueorigin.com/careers'
    shop_url = 'https://shop.blueorigin.com/'
    reserve_seat_url = "https://www.blueorigin.com/new-shepard/reserve-a-seat"


class title:
    new_shepard = "New Shepard | Blue Origin"
    new_glenn = "New Glenn | Blue Origin"
    blue_moon = "Blue Moon | Blue Origin"
    blue_ring = "Blue Ring | Blue Origin"
    engines = "Engines | Blue Origin"
    destinations = "LEO Destinations | Blue Origin"
    motion_ctrl = "Motion Control | Blue Origin"
    exploration_system = "Exploration Systems | Blue Origin"
    about_blue = "About Blue | Blue Origin"
    sustainability = "Sustainability | Blue Origin"
    news = "News | Blue Origin"
    gallery = "Gallery | Blue Origin"
    career = "Jobs in Aerospace | Find Your Career with Blue Origin"
    shop = " Blue Origin Shop | Official store"
    reserve_seat = "Reserve a Seat | Blue Origin"

class nav_toggle:
    burger_menu = (By.XPATH, "//button[@aria-haspopup='dialog']")
    home_button =  (By.XPATH, "//img[@alt='Blue Origin: For The Benefit of Earth']")
    home_button2 = (By.XPATH, "//img[@alt='Blue Origin | Careers']")
    home_button3 =(By.XPATH,"//img[@alt='Blue Origin Shop']")
    #nav bar
    nav_new_shepard = (By.XPATH, "//a[@id='64e4e0cf0e85e32ff503b5df']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_new_glenn = (By.XPATH, "//a[@id='64e4e0e10e85e32ff503b5e0']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_blue_moon = (By.XPATH, "//a[@id='64e4e0e80e85e32ff503b5e1']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_blue_ring = (By.XPATH, "//a[@id='6602f6a219f0529a3ba2fea9']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_engines = (By.XPATH, "//a[@id='68095a15bf94a3d9aac62765']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_destinations = (By.XPATH, "//a[@id='68095a23bf94a3d9aac62766']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_motion_ctrl = (By.XPATH, "//a[@id='68095a35bf94a3d9aac62767']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_exploration_system = (By.XPATH,"//a[@id='68095a41bf94a3d9aac62768']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_about_blue = (By.XPATH, "//a[@id='6539441974d24126e7b91e47']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_sustainability = (By.XPATH, "//a[@id='6578e92fe15e4831fd1ba8de']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_news = (By.XPATH, "//a[@id='64e4e12b0e85e32ff503b5e7']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_gallery = (By.XPATH, "//a[@id='64e4e1340e85e32ff503b5e8']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_career = (By.XPATH, "//a[@id='64e4e1460e85e32ff503b5e9']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")
    nav_shop = (By.XPATH,"//a[@id='64e4e1530e85e32ff503b5ea']/span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC']")


class elements:
    video_iframe = (By.XPATH,"//iframe[contains(@src, 'C68OFAJNwBU')]")
    playing_mode = (By.XPATH,"//div[contains(@class, 'html5-video-player') and contains(@class, 'playing-mode')]")
    # video_player = (By.XPATH,"//video[@class='video-stream html5-main-video']")
    video_player =(By.ID, "movie_player")
class buttons:
    play_button = (By.XPATH, "//button[@title='Play' and contains(@class, 'ytp-large-play-button')]")
    explore_the_crew = (By.XPATH, "//button[.//span[contains(., 'Explore the Crew Capsule')]]")
    fly_to_space = (By.ID, '68644201f778ac8cd855fa1d')
    purchase_seat = (By.ID, '67ec3e759d4aed11e393f3b0')
    submit = (By.XPATH, "//button[@id='66db21e652f528776524b2ea-submit-button']")

class header:
    vehicle = (By.XPATH, "//button[text()='Vehicles']")
    systems = (By.XPATH, "//button[text()='Systems']")
    about = (By.XPATH, "//button[text()='About']")
    vehicle_dropdown = (By.XPATH, "//ul[contains(@class, 'HeaderNavigationFlyout_headerNavigationFlyoutList')]")
    system_dropdown = (By.XPATH, "//ul[.//span[text()='Engines']]")
    about_dropdown = (By.XPATH, "//ul[.//a[@href='/about-blue'] and .//a[@href='/sustainability'] and .//a[@href='/news']]")
    new_shep =(By.XPATH, "//span[text()='New Shepard']")
    new_shep_unique_elem = (By.XPATH, "//a[contains(@class, 'buttons_button') and .//span[text()='Fly to Space']]")
    new_shep_next_flight = (By.XPATH,"//h2[@id='6851bf026859295bf24363c7']/span[@class='DisplayTextBlock_displayText___W0zt DisplayTextBlock_uppercase__299Ks'][1]")

class field:
    footer_email = (By.XPATH, "//input[@name='EMAIL']")
    check_box = (By.XPATH,"//input[@type='checkbox' and contains(@class, 'Checkbox_checkbox') and @required]")
    submit_button = (By.XPATH, "//button[@type='submit' and span='Submit']")
    subscribe_message = (By.XPATH,"//p[contains(@class, 'ext-highlight') and contains(text(), 'Thank you for subscribing')]")

class forms:
    form = (By.XPATH, "//form[@id='66db21e652f528776524b2ea']/fieldset[@class='Form_fieldset__TUIOl'][1]")
    first_name = (By.XPATH,"//div[@id='66eadbca99f4d5037e43f168']/div[1]/label[@class='Form_label__yfPmN']/input[@class='Form_textInput__75im_']")
    last_name = (By.XPATH, "//div[@id='66eadbca99f4d5037e43f168']/div[2]/label[@class='Form_label__yfPmN']/input[@class='Form_textInput__75im_']")
    email = (By.XPATH,"//form[@id='66db21e652f528776524b2ea']/fieldset[@class='Form_fieldset__TUIOl'][1]/label[@class='Form_label__yfPmN']/input[@class='Form_textInput__75im_']")
    phone_number = (By.XPATH, "//form[@id='66db21e652f528776524b2ea']/fieldset[@class='Form_fieldset__TUIOl'][1]/div[3]/label[@class='Form_label__yfPmN']/input[@class='Form_textInput__75im_']")
    address = (By.XPATH, "//input[@name='address_one']")
    city = (By.XPATH, "//input[@name='city']")
    country = (By.XPATH,"//button[@role='combobox' and .//span[text()='Select an option']]")
    yearOfBirth = (By.XPATH,"//button[@id='«Rkomm9tndrnbH3»']")
    monthOfBirth = (By.XPATH,"//button[@id='«Rcomm9tndrnbH3»']")
    how_did_you_hear = (By.XPATH,"//div[@id='«R2p6m9tndrnbH2»']")
    tell_about_yourself = (By.XPATH,"//form[@id='66db21e652f528776524b2ea']/fieldset[@class='Form_fieldset__TUIOl'][2]/div[2]/label[@class='Form_label__yfPmN']/textarea[@class='Form_textInput__75im_ TextAreaInputBlock_textArea__9pxQB']")
    acknowledge = (By.XPATH,"//input[@id='6797fae489d0d664e44ed9c8']")
    confirm = (By.XPATH,"//input[@id='66db2386a8faa10e2089370d']")
    success_message = (By.XPATH,"//section[@id='66e08622010ca5000757c32c']/div[@class='Section_container__saIUK Section_column__ZOloK']")









