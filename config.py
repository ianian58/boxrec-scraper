# Configuration for BoxRecScraper

# Login credentials
LOGIN_URL = "https://boxrec.com/en/login"
USERNAME = "garciian58@icloud.com"
PASSWORD = "Cortiz1229"

# Rating URLs to scrape. It will s
RATINGS_URL = [
    {"url": "https://boxrec.com/en/ratings/M/box-pro/Heavyweight", "division": "Heavyweight"},
]
BASE_URL = "https://boxrec.com"  # Added base URL for easier configuration

SCRAPER_TYPES = {
    'ratings': 'ratings',
    'boxer': 'boxer_profile'
}

# Number of boxers to scrape per category
# Note: The limit is 50 due to the website's constraints.
BOXERS_TO_SCRAPE = 3