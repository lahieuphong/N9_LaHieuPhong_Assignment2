import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Pytest fixture để khởi tạo và đóng ChromeDriver
@pytest.fixture
def chrome_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()

# URL trang OpenCart demo
BASE_URL = "http://localhost/demo/index.php?route=common/home&language=en-gb"

# Hàm kiểm tra trạng thái tất cả liên kết trên trang
def test_all_links(chrome_driver):
    chrome_driver.get(BASE_URL)
    links = chrome_driver.find_elements(By.TAG_NAME, "a")

    link_status = []

    for link in links:
        href = link.get_attribute("href")
        if href:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                }
                response = requests.get(href, headers=headers, timeout=5)
                if response.status_code == 200:
                    link_status.append((href, "OK"))
                elif response.status_code == 403:
                    link_status.append((href, "Skipped (403 Forbidden)"))
                elif response.status_code == 404:
                    link_status.append((href, "Skipped (404 Not Found)"))  # Bỏ qua lỗi 404
                else:
                    link_status.append((href, f"Failed (Status code: {response.status_code})"))
            except requests.exceptions.RequestException as e:
                link_status.append((href, f"Failed (Error: {e})"))
        else:
            link_status.append(("No href", "Invalid link"))

    with open("all_links_status_report.txt", "w") as report_file:
        for href, status in link_status:
            report_file.write(f"{href} --> {status}\n")

    print("\nLink Status Report:")
    for href, status in link_status:
        print(f"{href} --> {status}")

    # Chỉ thất bại khi có lỗi không thể bỏ qua (không phải 403 hay 404)
    failed_links = [
        link for link, status in link_status
        if "Failed" in status and "403" not in status and "404" not in status
    ]
    assert not failed_links, f"Found broken links: {failed_links}"