import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import urllib.parse


@pytest.fixture
def chrome_driver():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    # Quit the driver after test
    driver.quit()


def test_login_success_chrome(chrome_driver):
    # Go to the login page
    chrome_driver.get("http://localhost/demo/index.php?route=account/login&language=en-gb")
    time.sleep(2)  # Wait for the page to load
    print("Navigated to login page.")

    # Input email
    email_input = chrome_driver.find_element(By.ID, "input-email")
    email_input.send_keys("hieuphong144@gmail.com")
    time.sleep(1)
    print("Entered email.")

    # Input password
    password_input = chrome_driver.find_element(By.ID, "input-password")
    password_input.send_keys("21112003")
    time.sleep(1)
    print("Entered password.")

    # Click login button
    login_button = chrome_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    time.sleep(3)  # Wait for login to process
    print("Clicked login button.")

    # Assert no error alert is displayed
    error_alert = chrome_driver.find_elements(By.CSS_SELECTOR, ".alert.alert-danger")
    assert not error_alert, "Login failed with valid credentials!"
    print("No error alert found; login should be successful.")

    # Capture the current URL after login
    current_url = chrome_driver.current_url
    print(f"Current URL after login: {current_url}")

    # Assert that the current URL contains the account route
    assert "route=account/account" in current_url, \
        f"Expected to be redirected to account page, but was redirected to {current_url}!"

    # Extract the customer_token from the URL
    parsed_url = urllib.parse.urlparse(current_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    customer_token = query_params.get('customer_token', [None])[0]

    assert customer_token is not None, "Customer token not found in the URL!"
    print("Successfully redirected to account page with a valid customer token.")

    # Navigate back to the main page and verify
    logo = chrome_driver.find_element(By.CSS_SELECTOR, "img[title='Your Store']")
    logo.click()
    time.sleep(3)  # Wait for the main page to load
    print("Clicked on the logo to go back to the home page.")

    # Check that we're on the home page with logged-in status
    assert chrome_driver.current_url == "http://localhost/demo/index.php?route=common/home&language=en-gb", \
        "Failed to return to the home page with logged-in status!"
    print("Returned to the home page successfully.")

    # Check the "My Account" dropdown
    my_account_dropdown = chrome_driver.find_element(By.CSS_SELECTOR, "a.dropdown-toggle i.fa-user")
    my_account_dropdown.click()
    time.sleep(2)  # Wait for dropdown to open
    print("Opened 'My Account' dropdown.")

    # Count the number of items in the dropdown menu
    account_menu_items = chrome_driver.find_elements(By.CSS_SELECTOR, "ul.dropdown-menu.dropdown-menu-right li")
    item_count = len(account_menu_items)
    print(f"Found {item_count} items in the dropdown menu.")

    # Assert that there are five items in the dropdown when logged in
    assert item_count == 5, f"Expected 5 menu items in My Account dropdown, but found {item_count}. Login likely failed."
    print("Login success confirmed. Dropdown contains expected 5 items.")


def test_login_failure_invalid_username_chrome(chrome_driver):
    # Go to the login page
    chrome_driver.get("http://localhost/demo/index.php?route=account/login&language=en-gb")
    time.sleep(2)  # Wait for page to load
    print("Navigated to login page.")

    # Input incorrect email
    email_input = chrome_driver.find_element(By.ID, "input-email")
    email_input.send_keys("incorrect@example.com")
    time.sleep(1)
    print("Entered incorrect email.")

    # Input incorrect password
    password_input = chrome_driver.find_element(By.ID, "input-password")
    password_input.send_keys("21112003")
    time.sleep(1)
    print("Entered incorrect password.")

    # Click login button
    login_button = chrome_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    time.sleep(3)  # Wait for login attempt to process
    print("Clicked login button.")

    # Verify that login failed by checking for a specific error alert message
    error_alerts = chrome_driver.find_elements(By.CSS_SELECTOR, ".alert.alert-danger")
    assert error_alerts, "Expected an error alert, but none was found."

    # Check that the first error alert is displayed and contains the correct message
    error_alert = error_alerts[0]
    assert error_alert.is_displayed(), "Expected the error alert to be displayed, but it was not found."
    assert "Warning: No match for E-Mail Address and/or Password." in error_alert.text, \
        "The specific warning message for incorrect login was not displayed as expected."
    print(f"Correct warning message found; login failed as expected. Alert message: {error_alert.text}")

    # Click on the logo to go back to the home page
    logo = chrome_driver.find_element(By.CSS_SELECTOR, "img[title='Your Store']")
    logo.click()
    time.sleep(3)  # Wait for the home page to load
    print("Clicked on the logo to go back to the home page.")

    # Click on the "My Account" dropdown
    my_account_dropdown = chrome_driver.find_element(By.CSS_SELECTOR, "a.dropdown-toggle i.fa-user")
    my_account_dropdown.click()
    time.sleep(2)  # Wait for dropdown to open
    print("Opened 'My Account' dropdown.")

    # Count the number of items in the dropdown menu
    account_menu_items = chrome_driver.find_elements(By.CSS_SELECTOR, "ul.dropdown-menu.dropdown-menu-right li")
    item_count = len(account_menu_items)
    print(f"Found {item_count} items in the dropdown menu.")

    # Assert that there are only two items (Register and Login) in the dropdown when login fails
    assert item_count == 2, f"Expected 2 menu items in My Account dropdown, but found {item_count}. Login failure not detected correctly."
    print("Login failure confirmed. Dropdown contains expected 2 items.")


def test_login_failure_invalid_password_chrome(chrome_driver):
    # Go to the login page
    chrome_driver.get("http://localhost/demo/index.php?route=account/login&language=en-gb")
    time.sleep(2)  # Wait for page to load
    print("Navigated to login page.")

    # Input incorrect email
    email_input = chrome_driver.find_element(By.ID, "input-email")
    email_input.send_keys("hieuphong144@gmail.com")
    time.sleep(1)
    print("Entered incorrect email.")

    # Input incorrect password
    password_input = chrome_driver.find_element(By.ID, "input-password")
    password_input.send_keys("211120033")
    time.sleep(1)
    print("Entered incorrect password.")

    # Click login button
    login_button = chrome_driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    time.sleep(3)  # Wait for login attempt to process
    print("Clicked login button.")

    # Verify that login failed by checking for a specific error alert message
    error_alerts = chrome_driver.find_elements(By.CSS_SELECTOR, ".alert.alert-danger")
    assert error_alerts, "Expected an error alert, but none was found."

    # Check that the first error alert is displayed and contains the correct message
    error_alert = error_alerts[0]
    assert error_alert.is_displayed(), "Expected the error alert to be displayed, but it was not found."
    assert "Warning: No match for E-Mail Address and/or Password." in error_alert.text, \
        "The specific warning message for incorrect login was not displayed as expected."
    print(f"Correct warning message found; login failed as expected. Alert message: {error_alert.text}")

    # Click on the logo to go back to the home page
    logo = chrome_driver.find_element(By.CSS_SELECTOR, "img[title='Your Store']")
    logo.click()
    time.sleep(3)  # Wait for the home page to load
    print("Clicked on the logo to go back to the home page.")

    # Click on the "My Account" dropdown
    my_account_dropdown = chrome_driver.find_element(By.CSS_SELECTOR, "a.dropdown-toggle i.fa-user")
    my_account_dropdown.click()
    time.sleep(2)  # Wait for dropdown to open
    print("Opened 'My Account' dropdown.")

    # Count the number of items in the dropdown menu
    account_menu_items = chrome_driver.find_elements(By.CSS_SELECTOR, "ul.dropdown-menu.dropdown-menu-right li")
    item_count = len(account_menu_items)
    print(f"Found {item_count} items in the dropdown menu.")

    # Assert that there are only two items (Register and Login) in the dropdown when login fails
    assert item_count == 2, f"Expected 2 menu items in My Account dropdown, but found {item_count}. Login failure not detected correctly."
    print("Login failure confirmed. Dropdown contains expected 2 items.")


def test_logout_success_chrome(chrome_driver):
    # First, call the test_login_success to ensure the user is logged in
    test_login_success_chrome(chrome_driver)

    # Click on the logout link
    logout_link = chrome_driver.find_element(By.LINK_TEXT, "Logout")
    logout_link.click()
    time.sleep(3)  # Wait for logout to process
    print("Clicked logout link.")
    # time.sleep(3000)

    # Verify redirection to logout confirmation page
    expected_logout_url = "http://localhost/demo/index.php?route=account/logout&language=en-gb"
    assert chrome_driver.current_url == expected_logout_url, "Logout redirection failed!"
    print("Redirected to logout page successfully.")

    # Verify that the logout confirmation page contains the expected content
    logout_header = chrome_driver.find_element(By.TAG_NAME, "h1")
    assert logout_header.is_displayed() and logout_header.text == "Account Logout", "Logout header not found!"
    print("Logout confirmation header is present.")

    logout_message = chrome_driver.find_element(By.XPATH, "//div[@id='content']/p[1]")
    assert "You have been logged off your account." in logout_message.text, "Logout message not found!"
    print("Logout confirmation message is present.")

    # Click on the 'Continue' button to return to the home page
    continue_button = chrome_driver.find_element(By.CSS_SELECTOR, "a.btn.btn-primary")
    continue_button.click()
    time.sleep(3)  # Wait for home page to load
    print("Clicked 'Continue' button.")

    # Verify redirection back to the home page
    expected_home_url = "http://localhost/demo/index.php?route=common/home&language=en-gb"
    assert chrome_driver.current_url == expected_home_url, "Failed to return to the home page after logout!"
    print("Returned to the home page successfully after logout.")

    # Click on the 'My Account' dropdown again
    my_account_dropdown = chrome_driver.find_element(By.CSS_SELECTOR, "a.dropdown-toggle i.fa-user")
    my_account_dropdown.click()
    time.sleep(2)  # Wait for dropdown to open
    print("Opened 'My Account' dropdown again.")

    # Count the number of items in the dropdown menu
    account_menu_items = chrome_driver.find_elements(By.CSS_SELECTOR, "ul.dropdown-menu.dropdown-menu-right li")
    item_count = len(account_menu_items)
    print(f"Found {item_count} items in the dropdown menu after logout.")

    # Assert that there are only two items (Register and Login) in the dropdown after logout
    assert item_count == 2, f"Expected 2 menu items in My Account dropdown after logout, but found {item_count}."
    print("Logout success confirmed. Dropdown contains expected 2 items after logout.")


# The main test case based on the description provided
def test_lost_session_when_navigating_back_from_order_creation(chrome_driver):
    # First, login successfully
    print("Step 1: Logging in...")
    test_login_success_chrome(chrome_driver)

    # Navigate to 'Order History' page by clicking the 'Order History' link
    print("Step 2: Navigating to Order History page...")
    order_history_link = chrome_driver.find_element(By.CSS_SELECTOR, "a.dropdown-item[href*='route=account/order']")
    order_history_link.click()
    time.sleep(2)  # wait for the page to load

    # Check if we are on the order history page
    assert "order" in chrome_driver.current_url, "Failed to navigate to Order History page"
    print(f"Navigated to Order History page. Current URL: {chrome_driver.current_url}")

    # Click on the 'View' button to view order details
    print("Step 3: Clicking on the 'View' button for order details...")
    view_button = chrome_driver.find_element(By.CSS_SELECTOR, "a.btn.btn-info")
    view_button.click()
    time.sleep(2)  # wait for the order details page to load

    # Check if we are on the order details page
    assert "order.info" in chrome_driver.current_url, "Failed to navigate to order details page"
    print(f"Navigated to Order Details page. Current URL: {chrome_driver.current_url}")

    # After navigating to the order details page (Step 7 complete)
    print("Step 4: Scrolling down to ensure 'Return' button is visible...")
    # Scroll down to make sure the 'Return' button is visible (you can also use JavaScript scroll)
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # wait for scroll to complete

    # Find and click on the 'Return' button
    print("Step 5: Clicking on the 'Return' button to initiate a return request...")
    return_button = chrome_driver.find_element(By.CSS_SELECTOR, "a.btn.btn-danger")
    return_button.click()
    time.sleep(2)  # wait for the return page to load

    # Check if we are on the return page
    assert "returns.add" in chrome_driver.current_url, "Failed to navigate to return page"
    print(f"Navigated to Return page. Current URL: {chrome_driver.current_url}")

    # Scroll down again to ensure the 'Back' button is visible
    print("Step 6: Scrolling down to ensure 'Back' button is visible...")
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # wait for scroll to complete

    # Find and click on the 'Back' button
    print("Step 7: Clicking on the 'Back' button to return to the previous page...")
    back_button = chrome_driver.find_element(By.CSS_SELECTOR, "a.btn.btn-light")
    back_button.click()
    time.sleep(2)  # wait for the back navigation to complete

    # Check if we're redirected to the login page
    assert "login" in chrome_driver.current_url, "Session should be lost and redirected to login page"
    print(f"Redirected to login page. Current URL: {chrome_driver.current_url}")