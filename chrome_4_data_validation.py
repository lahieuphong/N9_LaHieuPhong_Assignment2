import time
import random
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def chrome_driver():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    # Quit the driver after test
    driver.quit()


def test_dashboard_product_info(chrome_driver):
    # Step 1: Access the dashboard page
    dashboard_url = "http://localhost/demo/admin/index.php?route=common/dashboard&user_token=edb79579958f6bc283b3a46e52a73283"
    chrome_driver.get(dashboard_url)
    # time.sleep(2)

    # Step 2: Close the alert pop-up (assuming it's a Bootstrap modal close button)
    try:
        close_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn-close[data-bs-dismiss='alert']")
        close_button.click()
        print("Alert closed.")
    except NoSuchElementException:
        print("No alert found to close.")

    # Step 3: Login
    # Fill in username and password and submit the form
    try:
        username_input = chrome_driver.find_element(By.CSS_SELECTOR, "input#input-username")
        password_input = chrome_driver.find_element(By.CSS_SELECTOR, "input#input-password")

        # Enter credentials
        username_input.send_keys("admin")
        time.sleep(2)
        password_input.send_keys("admin")
        time.sleep(2)

        # Submit login form
        login_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
        login_button.click()

        # Wait for the page to load after login
        time.sleep(3)

        # Verify if redirected to the correct dashboard page
        assert "route=common/dashboard" in chrome_driver.current_url, "Login failed or incorrect redirection."
        print("Successfully logged in and redirected to dashboard.")

    except NoSuchElementException as e:
        print("Login form elements not found:", e)
    except AssertionError as e:
        print(e)

    # Step 4: Close modal (if exists)
    try:
        modal_close_button = chrome_driver.find_element(By.CSS_SELECTOR, "button.btn-close[data-bs-dismiss='modal']")
        modal_close_button.click()
        print("Modal closed.")
    except NoSuchElementException:
        print("No modal found to close.")

    time.sleep(5)

    # Scroll to the bottom of the page
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Scrolled to the bottom of the page.")

    time.sleep(5)

    # Step 5: Check Recent Activity
    try:
        # Locate the "Recent Activity" section
        recent_activity_section = chrome_driver.find_element(By.CSS_SELECTOR, "div.card.mb-3 .list-group")

        # Check if there are no results (displayed as a list item)
        no_results_message = recent_activity_section.find_element(By.CSS_SELECTOR, "li.list-group-item.text-center")

        if no_results_message.text == "No results!":
            print("\nRecent Activity: No results found.")
            print("-" * 40)
        else:
            print("\nRecent Activity: Data found.")
            print("-" * 40)

            # Optionally, add checks for activity data if it exists
            activity_items = recent_activity_section.find_elements(By.CSS_SELECTOR, "li.list-group-item")
            for item in activity_items:
                print(f"\nRecent Activity: {item.text}")
                print("-" * 40)
    except NoSuchElementException:
        print("Recent Activity section not found.")
    except Exception as e:
        print(f"Error checking Recent Activity: {e}")

    # Step 6: Locate and verify Latest Orders
    try:
        orders_table = chrome_driver.find_element(By.CSS_SELECTOR, "div.card.mb-3 .table tbody")
        order_rows = orders_table.find_elements(By.TAG_NAME, "tr")

        # Loop through all rows and verify order details
        for row in order_rows:
            order_id = row.find_element(By.CSS_SELECTOR, "td.text-end").text
            customer_name = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
            order_status = row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text
            date_added = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text
            total_amount = row.find_element(By.CSS_SELECTOR, "td.text-end:nth-child(5)").text

            # Print order details (you can replace this with assertions for validation)
            print(f"Order ID: {order_id}")
            print(f"Customer: {customer_name}")
            print(f"Status: {order_status}")
            print(f"Date Added: {date_added}")
            print(f"Total: {total_amount}")
            print("-" * 40)

    except NoSuchElementException as e:
        print("Error finding orders table or rows:", e)


def test_compare_product_info(chrome_driver):
    # Truy cập trang chi tiết sản phẩm
    product_url = "http://localhost/demo/index.php?route=product/product&language=en-gb&product_id=40"
    chrome_driver.get(product_url)

    # Lấy thông tin từ trang chi tiết sản phẩm
    product_name = chrome_driver.find_element(By.TAG_NAME, 'h1').text
    price_new = chrome_driver.find_element(By.CSS_SELECTOR, '.price-new').text
    price_new_value = float(price_new.replace('$', '').replace(',', '').strip())  # Convert price to float

    # Lấy thêm thông tin khác từ trang
    brand = chrome_driver.find_element(By.XPATH, "//li[contains(text(), 'Brand')]").text
    product_code = chrome_driver.find_element(By.XPATH, "//li[contains(text(), 'Product Code')]").text
    availability = chrome_driver.find_element(By.XPATH, "//li[contains(text(), 'Availability')]").text

    # Chọn một số lượng ngẫu nhiên từ 1 đến 5
    quantity = random.randint(1, 5)
    quantity_input = chrome_driver.find_element(By.ID, 'input-quantity')
    quantity_input.clear()  # Xóa giá trị cũ
    quantity_input.send_keys(str(quantity))  # Nhập số lượng ngẫu nhiên

    # Nhấn nút "Add to Cart"
    add_to_cart_button = chrome_driver.find_element(By.ID, 'button-cart')
    add_to_cart_button.click()

    # Đợi giỏ hàng được cập nhật
    time.sleep(2)

    # Truy cập vào trang giỏ hàng
    chrome_driver.get("http://localhost/demo/index.php?route=checkout/cart&language=en-gb")

    # In thông tin sản phẩm ra terminal
    print("Product Information:")
    print(f"Name: {product_name}")
    print(f"Price: {price_new}")
    print(f"Brand: {brand}")
    print(f"Product Code: {product_code}")
    print(f"Availability: {availability}")
    print(f"Quantity Added: {quantity}")

    # Nhấn vào nút giỏ hàng để xem chi tiết
    shopping_cart_button = chrome_driver.find_element(By.LINK_TEXT, "Shopping Cart")
    shopping_cart_button.click()

    # Đợi trang giỏ hàng tải
    time.sleep(2)

    # Lấy thông tin từ trang giỏ hàng
    cart_items = chrome_driver.find_elements(By.XPATH, "//div[@id='shopping-cart']//tbody/tr")

    # In thông tin sản phẩm trong giỏ hàng
    print("\nItems in Shopping Cart:")
    for item in cart_items:
        item_name = item.find_element(By.XPATH, ".//td[contains(@class, 'text-start')]//a").text
        item_model = item.find_element(By.XPATH, ".//td[contains(@class, 'text-start') and not(contains(text(), 'Quantity'))]").text
        item_quantity = item.find_element(By.XPATH, ".//td[contains(@class, 'text-start')]//input[@name='quantity']").get_attribute('value')
        item_price = item.find_element(By.XPATH, ".//td[@class='text-end'][1]").text
        item_price_value = float(item_price.replace('$', '').replace(',', '').strip())  # Convert item price to float
        item_total = item.find_element(By.XPATH, ".//td[@class='text-end'][2]").text

        # In thông tin từng sản phẩm
        print(f"Name: {item_name}, Model: {item_model}, Quantity: {item_quantity}, Unit Price: {item_price}, Total: {item_total}")

        # So sánh thông tin sản phẩm
        print("\nComparing product details:")
        print(f"Name: {product_name} vs Name: {item_name}")
        print(f"Price: {price_new} vs Unit Price: {item_price}")
        print(f"Quantity Added: {quantity} vs Quantity: {item_quantity}")

        # So sánh và in ra kết quả
        if product_name == item_name:
            print("Product name matches!")
        else:
            print("Product name does not match!")

        if price_new_value == item_price_value:
            print("Product price matches!")
        else:
            print("Product price does not match!")

        if quantity == int(item_quantity):
            print("Quantities match!")
        else:
            print("Quantities do not match!")

        print("\n")

    # Lấy thông tin tổng giá trong giỏ hàng
    totals = chrome_driver.find_elements(By.XPATH, "//tfoot[@id='checkout-total']//tr")
    for total in totals:
        total_description = total.find_element(By.XPATH, ".//td[contains(@class, 'text-end')][1]").text
        total_value = total.find_element(By.XPATH, ".//td[contains(@class, 'text-end')][2]").text
        print(f"{total_description}: {total_value}")