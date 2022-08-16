from db_config import db_password, db_root

# for main zillow_site_scraping
HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

START_PAGE = 2
NUM_PAGE = 20
CITY = 'San-Diego'
STATE = 'CA'
COUNTRY = 'USA'
BASE_URL = 'https://www.zillow.com/homes/'

# for connection to MySQL
SQL_PASS = db_password
SQL_ROOT = db_root

# for requests from APIs
SCHOOLS_BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools.json"
SCHOOLS_API_KEY = "15YccxZXn0RXq0DaoQiTOdRDmA4gFywaNoUtQdhn"

AQI_URL = "http://api.airvisual.com/v2/city"
AQI_API_KEY = "8cb2912f-80f0-4e27-808d-0b3d290ac3ad"

# logger file
LOG_FILE = 'logs.log'
