from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config

class BaseScraper:
    """
    Base class for web scrapers.

    Attributes:
        driver: A Selenium WebDriver instance for browser automation.
    """

    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password, login_url):
        """
        Logs into a website using provided credentials.

        Args:
            username: The username for login.
            password: The password for login.
            login_url: The URL of the login page.
        """
        self.driver.get(login_url)
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.NAME, "login[go]").click()
        
        WebDriverWait(self.driver, 30).until(EC.url_contains(config.BASE_URL))
