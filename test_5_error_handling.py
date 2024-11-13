import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def chrome_driver():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    # Quit the driver after test
    driver.quit()


def test_contact_us_invalid_fields(chrome_driver):
    print("Test started: Navigating to the Contact Us page...")

    # Open the "Contact Us" page
    chrome_driver.get("http://localhost/demo/index.php?route=information/contact&language=en-gb")

    # Wait for the page to load and JavaScript to execute
    time.sleep(5)  # Allow time for page to load

    # Get the height of the page and scroll halfway down
    print("Scrolling the page halfway...")
    scroll_height = chrome_driver.execute_script("return document.body.scrollHeight")
    chrome_driver.execute_script(f"window.scrollTo(0, {scroll_height / 3});")  # Scroll halfway
    time.sleep(2)  # Optional: Wait for the page to load/adjust after scrolling

    print("Page scrolled halfway. Now starting to fill the form...")

    # Find and fill in the "Name" field
    name_field = chrome_driver.find_element(By.ID, "input-name")
    name_field.send_keys("HP")  # Invalid value (name must be between 3 and 32 characters)
    time.sleep(2)

    # Find and fill in the "Email" field
    email_field = chrome_driver.find_element(By.ID, "input-email")
    email_field.send_keys("l@h@p@gmail.com")  # Invalid email
    time.sleep(2)

    # Find and fill in the "Enquiry" field
    enquiry_field = chrome_driver.find_element(By.ID, "input-enquiry")
    enquiry_field.send_keys("Satisfied")  # Too short (should be between 10 and 3000 characters)
    time.sleep(2)

    # Find and click the "Submit" button
    submit_button = chrome_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)

    print("Checking for error messages...")

    # Check error for the "Name" field
    error_name = chrome_driver.find_element(By.ID, "error-name")
    time.sleep(1)  # Wait for the error message to appear
    assert error_name.is_displayed(), "Error not displayed for 'Name' field"
    assert error_name.text == "Name must be between 3 and 32 characters!", "Incorrect error message for 'Name'"
    print(f"Name error message: {error_name.text}")

    # Check error for the "Email" field
    error_email = chrome_driver.find_element(By.ID, "error-email")
    time.sleep(1)  # Wait for the error message to appear
    assert error_email.is_displayed(), "Error not displayed for 'Email' field"
    assert error_email.text == "E-Mail Address does not appear to be valid!", "Incorrect error message for 'Email'"
    print(f"Email error message: {error_email.text}")

    # Check error for the "Enquiry" field
    error_enquiry = chrome_driver.find_element(By.ID, "error-enquiry")
    time.sleep(1)  # Wait for the error message to appear
    assert error_enquiry.is_displayed(), "Error not displayed for 'Enquiry' field"
    assert error_enquiry.text == "Enquiry must be between 10 and 3000 characters!", "Incorrect error message for 'Enquiry'"
    print(f"Enquiry error message: {error_enquiry.text}")

    print("Test completed successfully.")

    # Optional: Wait a few seconds to visually confirm the behavior
    time.sleep(2)


def test_registration_invalid_fields(chrome_driver):
    print("Test started: Navigating to the Registration page...")

    # Open the "Registration" page
    chrome_driver.get("http://localhost/demo/index.php?route=account/register&language=en-gb")

    # Wait for the page to load
    time.sleep(5)  # Allow time for the page to load

    # Wait for the page to load and JavaScript to execute
    time.sleep(5)  # Allow time for page to load

    # Get the height of the page and scroll halfway down
    print("Scrolling the page halfway...")
    scroll_height = chrome_driver.execute_script("return document.body.scrollHeight")
    chrome_driver.execute_script(f"window.scrollTo(0, {scroll_height / 4});")  # Scroll halfway
    time.sleep(2)  # Optional: Wait for the page to load/adjust after scrolling


    # Fill in the "First Name" field
    firstname_field = chrome_driver.find_element(By.ID, "input-firstname")
    firstname_field.send_keys("1111111111111111111111111111111111111111111111")  # Invalid first name
    time.sleep(2)

    # Fill in the "Last Name" field
    lastname_field = chrome_driver.find_element(By.ID, "input-lastname")
    lastname_field.send_keys("1111111111111111111111111111111111111111111111")  # Invalid last name
    time.sleep(2)

    # Fill in the "Email" field (invalid email format)
    email_field = chrome_driver.find_element(By.ID, "input-email")
    email_field.send_keys("")  # Invalid email
    time.sleep(2)

    # Fill in the "Password" field (invalid password length)
    password_field = chrome_driver.find_element(By.ID, "input-password")
    password_field.send_keys("123")  # Invalid password (should be between 4 and 20 characters)
    time.sleep(2)

    # Check the "Newsletter" checkbox
    newsletter_checkbox = chrome_driver.find_element(By.ID, "input-newsletter")
    newsletter_checkbox.click()
    time.sleep(1)

    # Check the "Agree to terms" checkbox
    agree_checkbox = chrome_driver.find_element(By.NAME, "agree")
    agree_checkbox.click()
    time.sleep(2)

    # Click the "Continue" button to submit the form
    submit_button = chrome_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()
    time.sleep(2)

    print("Checking for error messages...")

    # Check error for the "First Name" field
    error_firstname = chrome_driver.find_element(By.ID, "error-firstname")
    time.sleep(1)  # Wait for the error message to appear
    assert error_firstname.is_displayed(), "Error not displayed for 'First Name' field"
    assert error_firstname.text == "First Name must be between 1 and 32 characters!", "Incorrect error message for 'First Name'"
    print(f"First Name error message: {error_firstname.text}")

    # Check error for the "Last Name" field
    error_lastname = chrome_driver.find_element(By.ID, "error-lastname")
    time.sleep(1)  # Wait for the error message to appear
    assert error_lastname.is_displayed(), "Error not displayed for 'Last Name' field"
    assert error_lastname.text == "Last Name must be between 1 and 32 characters!", "Incorrect error message for 'Last Name'"
    print(f"Last Name error message: {error_lastname.text}")

    # Check error for the "Email" field
    error_email = chrome_driver.find_element(By.ID, "error-email")
    time.sleep(1)  # Wait for the error message to appear
    assert error_email.is_displayed(), "Error not displayed for 'Email' field"
    assert error_email.text == "E-Mail Address does not appear to be valid!", "Incorrect error message for 'Email'"
    print(f"Email error message: {error_email.text}")

    # Check error for the "Password" field
    error_password = chrome_driver.find_element(By.ID, "error-password")
    time.sleep(1)  # Wait for the error message to appear
    assert error_password.is_displayed(), "Error not displayed for 'Password' field"
    assert error_password.text == "Password must be between 4 and 20 characters!", "Incorrect error message for 'Password'"
    print(f"Password error message: {error_password.text}")

    print("Test completed successfully.")

    # Optional: Wait a few seconds to visually confirm the behavior
    time.sleep(2)


def test_error_page_displayed_when_adding_product_to_cart_fails(chrome_driver):
    # Step 1: Navigate to the product page
    driver = chrome_driver
    driver.get("http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=43")
    print("Navigated to the product page.")

    # Step 2: Find the quantity input field and set the value to an extremely large number
    quantity_field = driver.find_element(By.ID, "input-quantity")
    quantity_field.clear()  # Clear any existing value
    quantity_field.send_keys("2147483648")
    print("Entered the quantity: 2147483648")

    # Step 3: Find the 'Add to Cart' button and click it
    add_to_cart_button = driver.find_element(By.ID, "button-cart")
    add_to_cart_button.click()
    print("Clicked on 'Add to Cart' button.")

    # Step 4: Wait for a moment for the response to show up (could be replaced with explicit wait)
    time.sleep(2)  # This could be replaced with a more explicit wait for an element

    # Step 5: Check the success message
    try:
        success_message = driver.find_element(By.CSS_SELECTOR, ".alert-success")
        print(f"Success message: {success_message.text}")
    except Exception as e:
        print(f"Error finding success message: {e}")

    # Step 6: Check the cart button and print the cart content
    cart_button = driver.find_element(By.CSS_SELECTOR, "button[data-bs-toggle='dropdown']")
    cart_text = cart_button.text
    print(f"Cart button text: {cart_text}")

    # Step 7: Verify that the cart content message is showing the extremely high item quantity
    assert "2147483647 item(s)" in cart_text, f"Expected cart to show '2147483647 item(s)', but found: {cart_text}"
    print("Verified the cart button shows the expected number of items.")

    # Step 8: Optionally, validate that no further issues occur due to the invalid quantity
    # (You can add more checks here depending on the application behavior)


def test_error_page_displayed_when_adding_product_with_negative_quantity(chrome_driver):
    # Step 1: Navigate to the product page
    driver = chrome_driver
    driver.get("http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=43")
    print("Navigated to the product page.")

    # Step 2: Find the quantity input field and set the value to a negative number (-1)
    quantity_field = driver.find_element(By.ID, "input-quantity")
    quantity_field.clear()  # Clear any existing value
    quantity_field.send_keys("-1")
    print("Entered the quantity: -1")

    # Step 3: Find the 'Add to Cart' button and click it
    add_to_cart_button = driver.find_element(By.ID, "button-cart")
    add_to_cart_button.click()
    print("Clicked on 'Add to Cart' button.")

    # Step 4: Wait for the error message to appear
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-danger"))
        )
        print(f"Error message: {error_message.text}")
    except TimeoutException:
        print("Error message did not appear within the wait time.")

    # Step 5: Check the cart button and print the cart content
    cart_button = driver.find_element(By.CSS_SELECTOR, "button[data-bs-toggle='dropdown']")
    cart_text = cart_button.text
    print(f"Cart button text: {cart_text}")

    # Step 6: Verify that the cart button shows '0 item(s) - $0.00'
    assert "0 item(s)" in cart_text, f"Expected cart to show '0 item(s)', but found: {cart_text}"
    assert "$0.00" in cart_text, f"Expected cart to show '$0.00', but found: {cart_text}"
    print("Verified the cart button shows '0 item(s) - $0.00' after attempting to add a negative quantity.")