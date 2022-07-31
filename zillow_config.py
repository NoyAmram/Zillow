from db_config import db_password, db_root

HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

START_PAGE = 2
NUM_PAGE = 20
CITY = 'San-Diego'
STATE = 'CA'
BASE_URL = 'https://www.zillow.com/homes/'

SQL_PASS = db_password
SQL_ROOT = db_root
