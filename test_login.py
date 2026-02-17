import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestLogin:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Setup Chrome Driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://practicetestautomation.com/practice-test-login/")
        self.driver.implicitly_wait(5)
        yield
        self.driver.quit()

    # 1. POSITIVE TEST: Valid Credentials
    def test_login_success(self):
        self.driver.find_element(By.ID, "username").send_keys("student")
        self.driver.find_element(By.ID, "password").send_keys("Password123")
        self.driver.find_element(By.ID, "submit").click()
        
        # Verify success by checking URL and Success Message
        assert "practicetestautomation.com/logged-in-successfully/" in self.driver.current_url
        success_text = self.driver.find_element(By.TAG_NAME, "h1").text
        assert "Logged In Successfully" in success_text

    # 2. NEGATIVE TEST: Invalid Password
    def test_login_invalid_password(self):
        self.driver.find_element(By.ID, "username").send_keys("student")
        self.driver.find_element(By.ID, "password").send_keys("wrong_pass")
        self.driver.find_element(By.ID, "submit").click()
        
        error_msg = self.driver.find_element(By.ID, "error").text
        assert "Your password is invalid!" in error_msg

    # 3. NEGATIVE TEST: Invalid Username
    def test_login_invalid_username(self):
        self.driver.find_element(By.ID, "username").send_keys("incorrect_user")
        self.driver.find_element(By.ID, "password").send_keys("Password123")
        self.driver.find_element(By.ID, "submit").click()
        
        error_msg = self.driver.find_element(By.ID, "error").text
        assert "Your username is invalid!" in error_msg

    # 4. NEGATIVE TEST: Empty Fields
    def test_login_empty_fields(self):
        # Leave fields blank and click submit
        self.driver.find_element(By.ID, "submit").click()
        
        # Checking if error message appears (site specific behavior)
        error_msg = self.driver.find_element(By.ID, "error").text
        assert error_msg is not None
