import time
import random
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def chrome_driver():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    # Quit the driver after test
    driver.quit()


def test_navigate_to_random_product_detail_chrome(chrome_driver):
    # Step 1: Navigate to the homepage
    chrome_driver.get("http://localhost/demo/index.php?route=common/home&language=en-gb")
    time.sleep(3)  # Wait for homepage to load
    print("Navigated to homepage.")

    # List of product selectors for MacBook, iPhone, Apple Cinema, and Canon EOS 5D
    product_selectors = [
        "//div[@class='image']/a[@href='http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=42']",  # iPhone
        "//div[@class='image']/a[@href='http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=43']",  # MacBook
        "//div[@class='image']/a[@href='http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=44']",  # Apple Cinema
        "//div[@class='image']/a[@href='http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=45']"   # Canon EOS 5D
    ]

    # Randomly select a product selector from the list
    selected_product_selector = random.choice(product_selectors)
    selected_product = chrome_driver.find_element(By.XPATH, selected_product_selector)

    # Scroll to the selected product to make sure it's in view
    ActionChains(chrome_driver).move_to_element(selected_product).perform()
    time.sleep(1)  # Brief wait after scrolling
    print("Scrolled to the selected product.")

    # Click on the selected product
    selected_product.click()
    time.sleep(3)  # Wait for product detail page to load
    print(f"Clicked on a random product. Navigated to {chrome_driver.current_url}")

    # Expected Result: Verify that the user is on the correct product detail page
    assert chrome_driver.current_url in [
        "http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=42",  # iPhone
        "http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=43",  # MacBook
        "http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=44",  # Apple Cinema
        "http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=45"   # Canon EOS 5D
    ], f"Unexpected product detail page URL: {chrome_driver.current_url}"

    print("Successfully navigated to the correct product detail page.")


def test_navigate_to_empty_cart_chrome(chrome_driver):
    # Step 1: Navigate to the homepage
    chrome_driver.get("http://localhost/demo/index.php?route=common/home&language=en-gb")
    time.sleep(3)  # Wait for homepage to load
    print("Navigated to homepage.")

    # Step 2: Click the shopping cart icon
    cart_icon = chrome_driver.find_element(By.CSS_SELECTOR, "a[title='Shopping Cart']")
    cart_icon.click()
    time.sleep(3)  # Wait for the cart page to load
    print("Clicked on the shopping cart icon.")

    # Verify that the user is on the cart page
    expected_url = "http://localhost/demo/index.php?route=checkout/cart&language=en-gb"
    assert chrome_driver.current_url == expected_url, \
        f"Expected to navigate to the cart page, but was on {chrome_driver.current_url}"

    # Verify the header on the cart page
    cart_header = chrome_driver.find_element(By.TAG_NAME, "h1")
    assert cart_header.text == "Shopping Cart", "Shopping Cart header is not found!"
    print("Shopping Cart header is present: " + cart_header.text)

    # Verify the empty cart message
    empty_cart_message = chrome_driver.find_element(By.XPATH, "//div[@id='content']/p[1]")
    assert empty_cart_message.text == "Your shopping cart is empty!", "Empty cart message is not found!"
    print("Empty cart message is present: " + empty_cart_message.text)

    # Print the header and empty message explicitly
    print("Header: " + cart_header.text)
    print("Message: " + empty_cart_message.text)

    # (Step 3) Optional: Verify the button that indicates items in the cart
    cart_button = chrome_driver.find_element(By.CSS_SELECTOR, "button[data-bs-toggle='dropdown']")
    assert cart_button.text == "0 item(s) - $0.00", "Cart button does not show '0 item(s) - $0.00'!"
    print("Cart button shows correct item count: " + cart_button.text)

    # Click on the cart button to see the dropdown
    cart_button.click()
    time.sleep(1)  # Wait for the dropdown to appear
    dropdown_message = chrome_driver.find_element(By.XPATH, "//ul[@class='dropdown-menu dropdown-menu-end p-2 show']/li")
    assert dropdown_message.text == "Your shopping cart is empty!", "Dropdown message is not correct!"
    print("Dropdown message is present: " + dropdown_message.text)


def add_product_to_cart(chrome_driver, product_url, quantity):
    # Step 1: Navigate to the product page
    chrome_driver.get(product_url)
    time.sleep(2)  # Wait for the page to load

    try:
        # Find the quantity input field and set quantity
        quantity_input = chrome_driver.find_element(By.ID, "input-quantity")
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))

        # Click the "Add to Cart" button
        add_to_cart_button = chrome_driver.find_element(By.ID, "button-cart")
        add_to_cart_button.click()
        time.sleep(3)  # Wait for the success message to appear

        # Locate the success message and print it
        success_message = chrome_driver.find_element(By.CSS_SELECTOR, "div.alert-success").text
        print(f"Added {quantity} of the product at {product_url} to the cart. Message: {success_message}")

    except Exception as e:
        print(f"Error adding product to cart: {e}")

def remove_all_products_from_cart(chrome_driver):
    # Step 4: Navigate to the shopping cart page
    chrome_driver.get("http://localhost/demo/index.php?route=checkout/cart&language=en-gb")
    time.sleep(3)  # Wait for the cart page to load
    print("Navigated to shopping cart page.")

    try:
        # Remove each product from the cart
        while True:
            # Re-locate the "Remove" buttons after each removal
            remove_buttons = chrome_driver.find_elements(By.CSS_SELECTOR, "button.btn-danger[formaction*='cart.remove']")

            if not remove_buttons:
                break  # Exit the loop if there are no more items to remove

            # Click the first "Remove" button and wait for the page to refresh
            remove_buttons[0].click()
            time.sleep(3)  # Wait for the item to be removed and the page to refresh
            print("Removed an item from the shopping cart.")

        print("All products have been removed from the cart.")

    except Exception as e:
        print("Error removing products from the cart:", e)

def test_navigate_to_shopping_cart(chrome_driver):
    product_urls = [
        "http://localhost/demo/index.php?route=product/product&path=20&product_id=40",  # iPhone
        "http://localhost/demo/index.php?route=product/product&path=20&product_id=43",  # MacBook
        "http://localhost/demo/index.php?route=product/product&path=20&product_id=49"   # Canon EOS 5D
    ]

    for product_url in product_urls:
        random_quantity = random.randint(1, 5)
        add_product_to_cart(chrome_driver, product_url, random_quantity)

    # Step 2: Click on the shopping cart icon to view the cart
    try:
        time.sleep(2)
        cart_icon = chrome_driver.find_element(By.CSS_SELECTOR, "button[data-bs-toggle='dropdown']")
        cart_icon.click()
        print("Clicked on the shopping cart icon.")
        time.sleep(3)

        # Click on the "View Cart" option
        time.sleep(1)
        view_cart_button = chrome_driver.find_element(By.LINK_TEXT, "View Cart")
        view_cart_button.click()
        print("Clicked on 'View Cart'.")
    except Exception as e:
        print("Error while navigating to the shopping cart:", e)

    # Step 3: Verify that the user is redirected to the shopping cart page
    expected_url = "http://localhost/demo/index.php?route=checkout/cart&language=en-gb"

    # Check for alert and dismiss if present
    try:
        alert = chrome_driver.find_element(By.CSS_SELECTOR, "div.alert-danger")
        if alert.is_displayed():
            print("Alert detected: Product(s) not available in desired quantity.")
            close_button = alert.find_element(By.CSS_SELECTOR, "button.btn-close")
            close_button.click()
            print("Alert dismissed.")
            time.sleep(2)  # Wait briefly after dismissing the alert
    except NoSuchElementException:
        print("No alert present.")

    current_url = chrome_driver.current_url
    if current_url == expected_url:
        print("User is redirected to the shopping cart page.")
    else:
        print(f"User is not redirected to the shopping cart page. Current URL: {current_url}")

    # Verify the shopping cart header is present
    try:
        time.sleep(2)
        header = chrome_driver.find_element(By.TAG_NAME, "h1")
        chrome_driver.execute_script("arguments[0].scrollIntoView(true);", header)
        assert "Shopping Cart" in header.text
        print("Shopping cart header is present on the page.")
    except AssertionError:
        print("Shopping cart header is not found.")
    except Exception as e:
        print("Error verifying shopping cart header:", e)

        # Step 4: Scroll down to the checkout button and click it
    try:
        # Scroll to the checkout button
        checkout_button = chrome_driver.find_element(By.CSS_SELECTOR, "a.btn.btn-primary[href*='checkout']")
        chrome_driver.execute_script("arguments[0].scrollIntoView(true);", checkout_button)
        time.sleep(1)  # Optional: wait for smooth scroll

        # Click on the checkout button
        checkout_button.click()
        print("Clicked on the 'Checkout' button.")
    except Exception as e:
        print("Error while clicking the 'Checkout' button:", e)

    time.sleep(5)

    # Step 4: Remove each product from the cart
    # remove_all_products_from_cart(chrome_driver)


def test_navigate_to_checkout(chrome_driver):
    # Step 1: Truy cập trang sản phẩm Canon EOS 5D
    product_url = "http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=30"
    chrome_driver.get(product_url)
    print(f"Accessed product page: {product_url}")

    # Step 2: Chọn màu ngẫu nhiên (Red hoặc Blue) từ dropdown
    try:
        color_select = WebDriverWait(chrome_driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-option-226"))
        )
        random_color = random.choice([15, 16])  # Red = 15, Blue = 16
        color_select.click()
        color_select.find_element(By.XPATH, f"//option[@value='{random_color}']").click()
        print(f"Selected color: {'Red' if random_color == 15 else 'Blue'}")
    except Exception as e:
        print("Error while selecting color:", e)

    # Step 3: Chọn số lượng ngẫu nhiên từ 1 đến 5
    try:
        quantity_field = WebDriverWait(chrome_driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-quantity"))
        )
        random_quantity = random.randint(1, 5)
        quantity_field.clear()  # Clear the current value
        quantity_field.send_keys(str(random_quantity))  # Enter random quantity
        print(f"Selected quantity: {random_quantity}")
    except Exception as e:
        print("Error while selecting quantity:", e)

    # Step 4: Nhấn nút "Add to Cart"
    try:
        add_to_cart_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "button-cart"))
        )
        # Scroll to the "Add to Cart" button to ensure it's in view
        chrome_driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart_button)
        time.sleep(1)  # Optional pause to ensure the element is scrolled into view

        add_to_cart_button.click()
        print("Clicked 'Add to Cart' button.")

        # Wait for success message
        WebDriverWait(chrome_driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#alert .alert-success"))
        )
    except Exception as e:
        print("Error while clicking 'Add to Cart' button:", e)

    # Step 5: Kiểm tra thông báo thành công
    try:
        success_message = chrome_driver.find_element(By.CSS_SELECTOR, "#alert .alert-success").text
        print("Success message:", success_message)
    except Exception as e:
        print("Error while verifying success message:", e)

    # Step 6: Cuộn lên đầu trang và nhấn nút "Checkout"
    try:
        # Scroll to the top of the page before clicking the Checkout button
        chrome_driver.execute_script("window.scrollTo(0, 0);")
        print("Scrolled to the top of the page.")
        time.sleep(10)  # Wait for any potential animations to finish

        # Wait for the Checkout button to be clickable and then click
        checkout_button = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.list-inline-item a[href*='route=checkout/checkout']"))
        )
        checkout_button.click()
        print("Clicked 'Checkout' button. Redirecting to checkout page.")

        # Wait for the checkout page to load by verifying that the URL contains 'checkout/checkout'
        WebDriverWait(chrome_driver, 10).until(
            EC.url_contains("checkout/checkout")
        )
        print("Successfully redirected to the checkout page.")
    except Exception as e:
        print("Error while clicking 'Checkout' button:", e)

    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

    time.sleep(5)


def test_navigate_to_sitemap_page(chrome_driver):
    print("Step 1: Navigate to the homepage")
    # Step 1: Navigate to the homepage
    chrome_driver.get("http://localhost/demo/index.php?route=common/home&language=en-gb")
    print("Homepage loaded.")

    # Step 2: Scroll down to the bottom of the page
    print("Step 2: Scroll down to the bottom of the page")
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for the page to finish scrolling
    print("Page scrolled to the bottom.")

    # Step 3: Find the "Site Map" link at the bottom of the page and click it
    print("Step 3: Find and click the 'Site Map' link")
    try:
        site_map_link = WebDriverWait(chrome_driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Site Map"))
        )
        site_map_link.click()
        print("'Site Map' link clicked.")
    except NoSuchElementException:
        pytest.fail("Site Map link not found")

    # Step 4: Verify the URL has changed to the sitemap page
    print("Step 4: Verify the URL has changed to the sitemap page")
    expected_url = "http://localhost/demo/index.php?route=information/sitemap&language=en-gb"
    WebDriverWait(chrome_driver, 10).until(EC.url_to_be(expected_url))
    print("URL changed to: " + chrome_driver.current_url)

    # Step 5: Verify the URL is correct
    print("Step 5: Verify the URL is correct")
    assert chrome_driver.current_url == expected_url, f"Expected URL {expected_url}, but got {chrome_driver.current_url}"
    print("URL is correct.")

    # Step 6: Verify the page title
    print("Step 6: Verify the page title contains 'Site Map'")
    page_title = chrome_driver.title
    assert "Site Map" in page_title, f"Expected 'Site Map' in the page title, but got {page_title}"
    print("Page title verified.")

    # Optional Step: Scroll halfway down on the sitemap page
    print("Step 7: Scroll halfway down the sitemap page")
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
    time.sleep(5)
    print("Page scrolled halfway down.")