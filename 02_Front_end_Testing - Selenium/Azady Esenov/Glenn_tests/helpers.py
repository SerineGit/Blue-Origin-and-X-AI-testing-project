# helpers.py
# Blue Origin Test Helper File

# ================================
# WEBSITE URLS
# ================================
main_url = "https://www.blueorigin.com/"
shop_main_url = "https://shop.blueorigin.com/"
new_glenn_collection_url = "https://shop.blueorigin.com/collections/new-glenn"

# ================================
# POSITIVE TEST LOCATORS
# ================================

# TC_P_011: New Glenn Collection Page
shop_button = "//a[@id='67d2fd164d044b0007e61e8d']//span[@class='HeaderNavigationLink_animatedFocusStateWrapper__SNBzC'][normalize-space()='Shop']"
new_glenn_menu_item = "//a[@class='header__menu-item header__menu-item list-menu__item link link--text focus-inset']//span[contains(text(),'New Glenn')]"
new_glenn_collection_title = "//h1[contains(text(), 'New Glenn')] | //h2[contains(text(), 'New Glenn')] | //*[contains(text(), 'New Glenn Collection')]"

# TC_P_012: Product Details (Image, Title, Price)
new_glenn_technical_tee = "//a[@id='CardLink-template--17946734788848__product-grid-8774535446768']"
new_glenn_monogram_hat = "//a[@id='CardLink-template--17946734788848__product-grid-9430989734128']"

# TC_P_013: Product Clickable
# Uses same locators as above

# TC_P_014: Add to Cart
add_to_cart_button = "//button[@name='add']"
cart_icon = "//div[@id='cart-notification']"

# TC_P_015: Search Function
search_icon = "//summary[@aria-label='Search']//span//*[name()='svg']"
search_input = "//input[@id='Search-In-Modal']"

# ================================
# NEGATIVE TEST LOCATORS
# ================================

# TC_N_012: Invalid Search Characters
invalid_search_chars = "&%&%$^*()"

# TC_N_013: Float Quantity Validation
quantity_input = "//input[@name='quantity'] | //input[contains(@class, 'quantity')] | //input[@type='number'] | //input[contains(@id, 'quantity')]"

# TC_N_014: Price Filter Max Value
price_button = "//h3//span[contains(text(),'Price')]"
price_filter_to = "//input[@id='Filter-Price-LTE']"

# TC_N_015: Empty Cart Checkout
cart_link = "//a[@id='cart-icon-bubble']//*[name()='svg']"
checkout_button = "//button[contains(text(), 'Checkout')] | //a[contains(text(), 'Checkout')] | //input[@value='Checkout']"

# ================================
# FALLBACK LOCATORS (Generic)
# ================================
first_product_link = "//a[contains(@href, 'products')]"
any_button = "//button"
any_link = "//a"

# ================================
# ERROR PAGE INDICATORS
# ================================
error_404_indicators = [
    "//h1[contains(text(), '404')]",
    "//*[contains(text(), 'Page not found')]",
    "//*[contains(text(), 'Not Found')]",
    "//title[contains(text(), '404')]"
]

# ================================
# VALIDATION MESSAGE LOCATORS
# ================================
validation_messages = "//div[contains(@class, 'error')] | //span[contains(@class, 'error')] | //*[contains(text(), 'Please enter')] | //*[contains(text(), 'Invalid')]"

# ================================
# TEST DATA
# ================================
expected_words = {
    "blue_origin": "Blue Origin",
    "new_glenn": "New Glenn",
    "shop": "Shop",
    "product": "product",
    "cart": "cart",
    "search": "search"
}

# Negative test data
negative_test_data = {
    "invalid_url_suffix": "collections/new-gle6768nngfhn",
    "invalid_search": "&%&%$^*()",
    "float_quantity": "1.5",
    "high_price": "999999",
    "invalid_email": "invalid-email-format"
}

# ================================
# COMMON TIMEOUTS
# ================================
DEFAULT_WAIT = 10
PAGE_LOAD_WAIT = 3
ELEMENT_INTERACTION_DELAY = 2

# ================================
# HELPER FUNCTIONS
# ================================
def delay():
    """Simple delay function for test stability"""
    import time
    time.sleep(ELEMENT_INTERACTION_DELAY)