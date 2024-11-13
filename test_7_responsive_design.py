import time
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


@pytest.fixture
def chrome_driver():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    # Quit the driver after test
    driver.quit()

@pytest.fixture
def firefox_driver():
    # Initialize Chrome WebDriver
    firefox_driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    yield firefox_driver
    # Quit the driver after test
    firefox_driver.quit()


def test_open_home_page_chrome(chrome_driver):
    try:
        # Mở trang web
        chrome_driver.get('http://localhost/demo/index.php?route=common/home&language=en-gb')
        time.sleep(5)  # Đợi trang tải xong

        # Kiểm tra tiêu đề trang
        if chrome_driver.title == "Your Store":  # Thay tiêu đề trang cụ thể nếu cần
            print("\nTrang web đã mở thành công!")
        else:
            print("\nTrang web không mở thành công.")

        # Kiểm tra sự tồn tại của hình ảnh
        img_element = chrome_driver.find_element(By.CSS_SELECTOR, "img[alt='Your Store']")

        # Kiểm tra thuộc tính src của thẻ img
        img_src = img_element.get_attribute("src")
        if img_src == "http://localhost/demo/image/catalog/opencart-logo.png":
            print("Hình ảnh đã tải thành công!")
        else:
            print("Hình ảnh không tải thành công.")

    except Exception as e:
        print(f"Đã có lỗi xảy ra: {e}")

    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

    time.sleep(5)

def test_open_home_page_firefox(firefox_driver):
    try:
        # Mở trang web
        firefox_driver.get('http://localhost/demo/index.php?route=common/home&language=en-gb')

        # Chờ cho đến khi hình ảnh xuất hiện trên trang (timeout 10 giây)
        img_element = WebDriverWait(firefox_driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt='Your Store']"))
        )

        # Kiểm tra thuộc tính src của thẻ img
        img_src = img_element.get_attribute("src")
        if img_src == "http://localhost/demo/image/catalog/opencart-logo.png":
            print("Hình ảnh đã tải thành công!")
        else:
            print("Hình ảnh không tải thành công.")

        # Kiểm tra tiêu đề trang
        if firefox_driver.title == "Your Store":  # Thay tiêu đề trang cụ thể nếu cần
            print("Trang web đã mở thành công!")
        else:
            print("Trang web không mở thành công.")

    except Exception as e:
        print(f"Đã có lỗi xảy ra: {e}")

    firefox_driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

    time.sleep(5)


def test_check_text_on_widgets(chrome_driver):
    print("Starting test_check_text_on_widgets")
    widget_selectors = ['button', 'div', 'span', 'p', '.widget-class']  # Modify selectors as needed

    # Open the page
    chrome_driver.get('http://localhost/demo/index.php?route=common/home&language=en-gb')
    chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        # Sleep for a few seconds to ensure page is loaded
        time.sleep(3)  # Wait for 5 seconds (adjust the duration if needed)

        for selector in widget_selectors:
            elements_with_text = chrome_driver.find_elements(By.CSS_SELECTOR, selector)

            # Print separator for each widget selector to make results more readable
            print(f"\nChecking elements for selector: {selector}")

            for element in elements_with_text:
                text = element.text.strip()  # Remove extra spaces

                # If text is empty, skip this element and do not print anything
                if not text:
                    # print(f"  - Element: {selector} has no text.")
                    continue  # Skip further checks for this element

                # Print non-empty text
                print(f"  - Element: {selector} contains text: '{text}'")

                # Check if the element is displayed and contains visible text
                assert element.is_displayed(), f"Error: Element {selector} is not displayed."

    except Exception as e:
        pytest.fail(f"Error checking text on widget elements: {str(e)}")


# Dùng parametrize để kiểm tra với các kích thước màn hình khác nhau
@pytest.mark.parametrize("width, height", [
    (320, 480),  # Thiết bị màn hình nhỏ, vd: iPhone 4s
    (480, 800),  # Thiết bị Android nhỏ, vd: Motorola Moto E, Sony Xperia U
    (600, 1024), # Màn hình tablet cỡ nhỏ, vd: iPad Mini 1, Amazon Kindle Fire
    (768, 1280), # Màn hình tablet, vd: iPad 2, Samsung Galaxy Tab 10.1
    (1366, 768), # Laptop phổ thông, vd: HP Pavilion, Lenovo IdeaPad
    (1920, 1080), # Màn hình Full HD, vd: laptop Dell XPS 13, TV Full HD
    (2560, 1440), # Màn hình Quad HD, vd: Samsung Galaxy S6, MacBook Pro
    (3840, 2160)  # Màn hình 4K, vd: Dell XPS 15
])

def test_check_ui_on_large_screen(chrome_driver, width, height):
    # Ghi lại thời gian bắt đầu tải trang
    start_time = time.time()

    # Thiết lập kích thước cửa sổ trình duyệt
    chrome_driver.set_window_size(width, height)
    print(f"\n\nKiểm tra với độ phân giải: {width}x{height}")

    # Mở trang web
    chrome_driver.get('http://localhost/demo/index.php?route=common/home&language=en-gb')  # URL bạn muốn kiểm tra

    # Đảm bảo trang đã tải xong
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Tính thời gian tải trang
    load_time = time.time() - start_time
    print(f"\nThời gian tải trang: {load_time:.2f} giây")

    # Kiểm tra xem thời gian tải có vượt quá 3 giây không
    assert load_time < 3, f"\nTrang tải quá lâu: {load_time:.2f} giây"

    # Kiểm tra các yếu tố quan trọng không bị kéo dài, chồng chéo
    try:
        # Kiểm tra xem phần tử header và footer có hiển thị đầy đủ không
        header = chrome_driver.find_element(By.TAG_NAME, 'header')
        footer = chrome_driver.find_element(By.TAG_NAME, 'footer')

        # Kiểm tra kích thước của header và footer
        print(f"\nHeader Height: {header.size['height']}")  # In chiều cao của header
        print(f"Footer Height: {footer.size['height']}")  # In chiều cao của footer

        assert header.size['height'] > 0, "Header bị ẩn hoặc không hiển thị đúng"
        assert footer.size['height'] > 0, "Footer bị ẩn hoặc không hiển thị đúng"

        # Kiểm tra các phần tử chính trên trang (thay bằng selector phù hợp)
        try:
            elements = chrome_driver.find_elements(By.CSS_SELECTOR, '.container')  # Thay đổi selector nếu cần
            print(f"Số lượng phần tử chính tìm thấy: {len(elements)}")  # In số lượng phần tử chính
            assert len(elements) > 0, "Các phần tử chính không hiển thị đúng"
        except Exception as e:
            pytest.fail(f"Không tìm thấy phần tử chính trên trang: {str(e)}")

    except Exception as e:
        pytest.fail(f"Kiểm tra giao diện thất bại: {str(e)}")

    # Kiểm tra tổng thể: chiều cao của trang không được vượt quá một giới hạn nào đó
    body_scroll_height = chrome_driver.execute_script("return document.body.scrollHeight")  # Lấy chiều cao trang
    window_inner_height = chrome_driver.execute_script("return window.innerHeight")  # Lấy chiều cao cửa sổ trình duyệt

    # Giới hạn chiều cao cho phép (có thể điều chỉnh tùy thuộc vào thiết bị)
    max_allowed_height = window_inner_height * 10  # Giới hạn chiều cao có thể được điều chỉnh, thử gấp 7 lần

    # In thông tin ra terminal để kiểm tra
    print(f"Chiều cao trang: {body_scroll_height}")
    print(f"Chiều cao cửa sổ trình duyệt: {window_inner_height}")
    print(f"Giới hạn chiều cao cho phép: {max_allowed_height}")

    # Kiểm tra xem chiều cao của trang có vượt quá giới hạn cho phép không
    assert body_scroll_height <= max_allowed_height, \
        f"Trang bị kéo dài quá nhiều ngoài vùng hiển thị. Chiều cao trang: {body_scroll_height}, " \
        f"Chiều cao cửa sổ: {window_inner_height}, Giới hạn cho phép: {max_allowed_height}"

    # Kiểm tra và cuộn trang nếu cần thiết
    if body_scroll_height > window_inner_height:
        print(f"Trang có thanh cuộn, cuộn xuống...")
        chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Cuộn trang xuống dưới cùng

    # Kiểm tra lại sau khi cuộn trang: đảm bảo không có thanh cuộn thừa hoặc phần tử bị thiếu
    body_scroll_height_after = chrome_driver.execute_script("return document.body.scrollHeight")
    print(f"Chiều cao trang sau khi cuộn: {body_scroll_height_after}")
    assert body_scroll_height_after <= max_allowed_height, \
        f"Sau khi cuộn, trang vẫn bị kéo dài quá nhiều ngoài vùng hiển thị. " \
        f"Chiều cao trang: {body_scroll_height_after}, Giới hạn cho phép: {max_allowed_height}"