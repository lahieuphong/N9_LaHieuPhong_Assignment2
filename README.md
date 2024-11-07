# OpenCart Selenium Test Suite Setup Guide

## Prerequisites
- Python 3.8 or higher
- PyCharm IDE
- Google Chrome Browser
- OpenCart running locally at http://localhost/demo/

## Environment Setup

	1. Clone the repository to your local machine
	2. Open PyCharm and create a new project
	3. Open the project terminal in PyCharm and install required packages:

```bash
pip install pytest
pip install selenium
pip install webdriver-manager
```

## Project Structure
	selenium_tests/
	├── chrome_1_login_logout.py
	├── chrome_2_form_submission.py
	├── chrome_3_navigation.py
	├── chrome_4_data_validation.py
	├── chrome_5_error_handling.py
	├── chrome_6_search_functionality.py
	├── chrome_7_responsive_design.py
	└── requirements.txt

##	Setting Up Test Environment
	1. Open PyCharm and go to File > Settings > Project > Python Interpreter
	2. Click the gear icon and select "Add"
	3. Choose "Virtual Environment" and click "OK"
	4. Wait for PyCharm to create and configure the virtual environment

##	Running Tests
### Method 1: Running Individual Test Files
	1. Right-click on any test file (e.g., chrome_1_login_logout.py)
	2. Select "Run 'pytest in chrome_1...'"
### Method 2: Running from Terminal
	1. Open PyCharm terminal
	2. Navigate to the project directory
	3. Run individual test files:
```bash
pytest chrome_1_login_logout.py -v
```
### Method 3: Running All Tests
	To run all test files:
```bash
pytest -v
```

## Test Account Credentials
```python
Email: hieuphong144@gmail.com
Password: 21112003
```

## Notes
	Ensure OpenCart is running at http://localhost/demo/ before running tests
	Tests include intentional delays (time.sleep()) for demonstration purposes
	Each test file focuses on specific functionality:
		chrome_1: Login/Logout functionality
		chrome_2: Contact form submission
		chrome_3: Navigation testing
		chrome_4: Data validation
		chrome_5: Error handling
		chrome_6: Search functionality
		chrome_7: Responsive design testing

## Troubleshooting
	1. ChromeDriver Error: If you get a ChromeDriver error, ensure Chrome browser is up to date
	2. Connection Error: Verify OpenCart is running at http://localhost/demo/
	3. Import Error: Make sure all required packages are installed in your virtual environment

## Additional Configuration
	Create a pytest.ini file in the project root:
```ini
[pytest]
python_files = chrome_*.py
python_functions = test_*
addopts = -v
```

## Contact
	* Email - Your Email
	* Project Link: LINK GITHUB

--- THE END ---
