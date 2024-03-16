from BaseScraper import BaseScraper
import config
from bs4 import BeautifulSoup
from utils import safe_int_convert, extract_attribute
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RatingScraper(BaseScraper):
    """
    A scraper for extracting boxer ratings from BoxRec.

    Attributes:
        driver: A Selenium WebDriver instance for browser automation.
    """

    def navigate_and_extract(self):
        """
        Navigates to each division URL and extracts boxer information.

        Returns:
            A list of dictionaries containing information about boxers.
        """
        all_boxers_info = []
        for division_index, division_info in enumerate(config.RATINGS_URL):
            self.driver.get(division_info['url'])  # Navigate to the specified URL
            
            # Wait for the ratings table to be loaded
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'ratingsResults'))
            )
            
            page_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            boxers_info_generator = self.extract_boxers_info(page_soup)
            for boxer_info in boxers_info_generator:
                all_boxers_info.append(boxer_info)
            print(f"\nDivision {division_index + 1} - {division_info['division']}:")
            for boxer in all_boxers_info:
                print(f"{boxer['rank']}. Name: {boxer['name']}, Nationality: {boxer['nationality']}, Record: {boxer['record']['wins']}-{boxer['record']['losses']}-{boxer['record']['draws']}, Age: {boxer['age']}, Last 6: {boxer['last_6']}, Rating: {boxer['rating']}, Profile Link: {boxer['profile_link']}")
        return all_boxers_info

    def extract_boxers_info(self, page_soup):
        """
        Extracts information about boxers from a page.

        Args:
            page_soup: BeautifulSoup object of the page.

        Yields:
            Boxer information as a dictionary.
        """
        table = page_soup.find('table', {'id': 'ratingsResults'})
        rows = table.find_all('tr')[1:]  # Adjusted to dynamically process rows
        valid_boxers_count = 0
        for row in rows:
            if valid_boxers_count >= config.BOXERS_TO_SCRAPE:
                break
            if len(row.find_all('td')) > 5:
                boxer_info = self.extract_boxer_info(row)
                if boxer_info:
                    yield boxer_info
                    valid_boxers_count += 1

    def extract_boxer_info(self, row):
        """
        Extracts information about a boxer from a table row.

        Args:
            row: A BeautifulSoup object representing a table row.

        Returns:
            A dictionary containing the boxer's information, or None if the row is invalid.
        """
        cells = row.find_all('td')
        if len(cells) <= 5:
            return None  # Skip invalid rows
        try:
            # Check for the champion's crown icon
            if cells[0].find('i', class_='fas fa-crown'):
                rank = 1
            else:
                # Extract rank from the span for non-champion boxers
                rank_span = cells[0].find('span', style=lambda value: value and 'font-weight:bold' in value)
                if rank_span:
                    rank = int(rank_span.text.strip('#'))
                else:
                    rank = None  # Fallback in case rank span is not found
            boxer_info = {
                'rank': rank,
                'name': cells[1].find('a', class_='personLink').text.strip(),
                'nationality': extract_attribute(cells[1], 'span', 'flag-icon', split_char='-', index=-1),
                'record': self.extract_record(cells[3]),
                'age': safe_int_convert(cells[4].text.strip()),
                'last_6': self.extract_last_6(cells[5]),
                'rating': self.extract_rating(cells[2]),
                'profile_link': config.BASE_URL + cells[1].find('a', class_='personLink')['href']
            }
        except (AttributeError, IndexError) as e:
            print(f"Error extracting data for a row: {e}")
            return None
        return boxer_info

    def extract_record(self, cell):
        """
        Extracts the win-loss-draw record of a boxer from a table cell.

        Args:
            cell: A BeautifulSoup object representing a table cell.

        Returns:
            A dictionary with keys 'wins', 'losses', and 'draws', mapping to the boxer's record.
        """
        return {key: safe_int_convert(span.text) for key, span in zip(['wins', 'losses', 'draws'], cell.find_all('span'))}

    def extract_rating(self, cell):
        """
        Extracts the rating of a boxer from a table cell.

        Args:
            cell: A BeautifulSoup object representing a table cell.

        Returns:
            A string representing the boxer's rating out of 5.
        """
        stars_filled = len(cell.find_all('i', class_='fas fa-star star-icon -star'))
        stars_half_filled = len(cell.find_all('i', class_='fas fa-star-half star-icon -star'))
        # No need to count stars_non_filled as we're fixing the total to 5
        rating = stars_filled + 0.5 * stars_half_filled
        return f"{rating}/5"

    def extract_last_6(self, cell):
        """
        Extracts the last 6 fight outcomes of a boxer from a table cell.

        Args:
            cell: A BeautifulSoup object representing a table cell.

        Returns:
            A string representing the last 6 fight outcomes (W for win, L for loss, D for draw, N for no contest).
        """
        last_6_fights = cell.find_all('img')
        return ''.join([
            'W' if 'l6w.svg' in fight['src'] else 
            'L' if 'l6l.svg' in fight['src'] else 
            'D' if 'l6d.svg' in fight['src'] else 
            'N' for fight in last_6_fights
        ])

    def safe_int_convert(self, value):
        """
        Safely converts a value to an integer.

        Args:
            value: The value to convert.

        Returns:
            The integer value, or 0 if conversion fails.
        """
        try:
            return int(value)
        except ValueError:
            return 0  # Returning 0 instead of None for better consistency in data types
