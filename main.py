import undetected_chromedriver as uc
from BaseScraper import BaseScraper
from RatingScraper import RatingScraper
import config

if __name__ == "__main__":
    options = uc.ChromeOptions()
    # Add any Chrome options you need
    driver = uc.Chrome(options=options)

    base_scraper = BaseScraper(driver)
    base_scraper.login(config.USERNAME, config.PASSWORD, config.LOGIN_URL)

    # Use the URL from the RATINGS_URL[0] dictionary
    rating_scraper = RatingScraper(driver)
    boxers_info = rating_scraper.navigate_and_extract()

    driver.quit()
