import random
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def chrome_driver():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    # Quit the driver after test
    driver.quit()


def test_search_macbook(chrome_driver):
    # Step 1: Navigate to the homepage
    chrome_driver.get("http://localhost/demo/index.php?route=common/home&language=en-gb")
    time.sleep(1)  # Wait for the page to load
    print("Navigated to the homepage.")

    # Step 2: Find the search input box and randomly enter "MacBook" or "macbook"
    search_box = chrome_driver.find_element(By.NAME, "search")
    search_term = random.choice(["MacBook", "macbook"])
    search_box.send_keys(search_term)
    time.sleep(1)  # Wait after entering the keyword
    print(f"Entered '{search_term}' into the search box.")

    # Step 3: Click the search button
    search_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn.btn-light.btn-lg")
    search_button.click()
    time.sleep(2)  # Wait for the search results page to load
    print("Clicked the search button and navigated to the results page.")

    # Step 4: Verify the URL of the search results page
    expected_url = f"http://localhost/demo/index.php?route=product/search&language=en-gb&search={search_term}"
    assert chrome_driver.current_url == expected_url, f"Expected URL to be '{expected_url}', but got '{chrome_driver.current_url}'"
    print(f"Verified URL: {chrome_driver.current_url}")

    # Step 5: Verify the presence of the search result heading with the text "Search - MacBook"
    search_heading = chrome_driver.find_element(By.TAG_NAME, "h1").text
    expected_heading = f"Search - {search_term.capitalize()}"

    # Convert both to lowercase to make the comparison case-insensitive
    assert search_heading.lower() == expected_heading.lower(), f"Expected heading '{expected_heading}', but got '{search_heading}'"
    print(f"Verified heading: '{search_heading}'")

    # Step 6: Verify the presence of product listings for "MacBook"
    product_list = chrome_driver.find_element(By.ID, "product-list")
    products = product_list.find_elements(By.CLASS_NAME, "product-thumb")

    # Ensure there are multiple products listed
    assert len(products) > 0, "Expected at least one product, but found none."
    print(f"Found {len(products)} product(s) in the search results for '{search_term}'.")

    # Step 7: Verify each product item contains "MacBook" in the title
    for product in products:
        product_title = product.find_element(By.CSS_SELECTOR, ".content h4 a").text
        assert "MacBook" in product_title, f"Product title '{product_title}' does not contain 'MacBook'."
        print(f"Verified product: '{product_title}'")

        # Optionally, print the price information for each product
        product_price = product.find_element(By.CLASS_NAME, "price-new").text
        print(f"Product '{product_title}' has a price of {product_price}")


def test_search_macbook_fail(chrome_driver):
    # Step 1: Navigate to the homepage
    chrome_driver.get("http://localhost/demo/index.php?route=common/home&language=en-gb")
    time.sleep(1)  # Wait for the page to load
    print("Navigated to the homepage.")

    # Step 2: Find the search input box and enter an intentionally incorrect term like "MacBok" or "macbok"
    search_box = chrome_driver.find_element(By.NAME, "search")
    search_term = random.choice(["MacBok", "macbok"])  # Intentionally misspelled terms
    search_box.send_keys(search_term)
    time.sleep(1)  # Wait after entering the keyword
    print(f"Entered '{search_term}' into the search box.")

    # Step 3: Click the search button
    search_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn.btn-light.btn-lg")
    search_button.click()
    time.sleep(5)  # Wait for the search results page to load
    print("Clicked the search button and navigated to the results page.")

    # Step 4: Verify the URL of the search results page
    expected_url = f"http://localhost/demo/index.php?route=product/search&language=en-gb&search={search_term}"
    assert chrome_driver.current_url == expected_url, f"Expected URL to be '{expected_url}', but got '{chrome_driver.current_url}'"
    print(f"Verified URL: {chrome_driver.current_url}")

    # Step 5: Verify the presence of the search result heading with the text "Search - MacBok" or "Search - macbok"
    search_heading = chrome_driver.find_element(By.TAG_NAME, "h1").text
    expected_heading = f"Search - {search_term}"
    assert search_heading == expected_heading, f"Expected heading '{expected_heading}', but got '{search_heading}'"
    print(f"Verified heading: '{search_heading}'")

    # Step 6: Verify that the "no product matches" message appears
    no_results_message = chrome_driver.find_element(By.XPATH, "//p[contains(text(), 'There is no product that matches the search criteria.')]").text
    expected_message = "There is no product that matches the search criteria."
    assert no_results_message == expected_message, f"Expected message '{expected_message}', but got '{no_results_message}'"
    print(f"Verified 'no product matches' message: '{no_results_message}'")