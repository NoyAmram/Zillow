from bs4 import BeautifulSoup
import requests
import zillow_config as cfg
import json
import pandas as pd
from tqdm import tqdm
import argparse
import data_from_api
from insert_data_to_db import data_from_scraper_to_db, data_from_api_school_to_db,\
    data_from_api_AQI_to_db
import log
import warnings
warnings.filterwarnings('ignore')

logger = log.setup_custom_logger(__name__)


def get_arguments():
    """Receives and return input of search query from the user """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('city', nargs='?', const=1, default=cfg.CITY, type=str)
    parser.add_argument('state', nargs='?', const=1, default=cfg.STATE, type=str)
    parser.add_argument('pages_number', nargs='?', const=1, default=cfg.NUM_PAGE, type=int)
    args = parser.parse_args()
    city = args.city
    state = args.state
    num_pages = args.pages_number
    logger.info(f'Successfully pass query arguments: %s,%s,%s', city, state, num_pages)
    return city, state, num_pages


def get_pages_url(url, start_page, end_page):
    """ Creates and returns list of unique url for each search page """
    url_list = [url + str(i) + '_p/' for i in range(start_page, end_page)]
    logger.info(f'Successfully create url_list from page %s to page %s', start_page, end_page)
    if start_page == cfg.START_PAGE:
        url_list.insert(0, url)  # url of first page has no page number
        logger.info(f'Successfully create url for first page')
    return url_list


def web_parse(url_pages):
    """ Receives list of urls differentiate with page numbers.
     Using requests.Session() send request for each url.
     Content extracted for each response text using BeautifulSoup library """
    with requests.Session() as session:
        response_list = [session.get(url, headers=cfg.HEADER) for url in tqdm(url_pages)]
    for i, r in enumerate(response_list):
        if r.status_code != 200:
            logger.error(f'Server response failed with status code: %s, at index: %s', r.status_code, i)
    soup_list = [BeautifulSoup(response.text, 'html.parser') for response in tqdm(response_list)]
    for soup in soup_list:
        if soup.select_one("script[data-zrr-shared-data-key]") is None:
            logger.warning(f'Website returns None object, '
                           f'this will cause possible future problem')
    return soup_list


def data_scraping(web_soup_list):
    """ Receives list of soup objects, extract the content using json
        and returns list of all data, dictionary for each house """
    try:
        all_data = [json.loads(
            web_soup.select_one("script[data-zrr-shared-data-key]")
            .contents[0]
            .strip("!<>-")) for web_soup in tqdm(web_soup_list)]
    except TypeError as scrape_error:
        logger.error(f"Data return as None, error raised {scrape_error}."
                     f"passing without content extraction")
        pass
    else:
        return all_data


def data_to_frame(web_data, frame):
    """ Receives site content from search pages, according to provided number of pages to extract from.
        The data containing all information for each house as dictionary.
         Extracts the data to create data frame """
    for data in web_data:
        try:
            for item in data['cat1']['searchResults']['listResults']:
                frame = frame.append(item, ignore_index=True)
        except TypeError as frame_error:
            logger.error(f"The following error was raised: {frame_error}."
                         f"Continue without adding to DataFrame.")
            pass
    logger.info("Successfully create data frame of all search pages")
    return frame


def main():
    """ Starting function of the program, calls above functions
     and activate script functions for API data and data_base creation."""
    arguments = get_arguments()
    search_url = cfg.BASE_URL + arguments[0] + ',_' + arguments[1] + '_rb/'
    for page in range(cfg.START_PAGE, arguments[2], cfg.BATCH):
        # default is scrape all 20 pages, 2 each time
        url_pages = get_pages_url(search_url, page, page+cfg.BATCH)
        data_soup = web_parse(url_pages)
        data = data_scraping(data_soup)
        frame = pd.DataFrame()
        house_df = data_to_frame(data, frame)
        data_from_scraper_to_db(house_df)
    school_df = data_from_api.get_school_table(arguments[1])
    data_from_api_school_to_db(school_df)
    aqi_df = data_from_api.get_aqi_table(arguments[0], arguments[1])
    data_from_api_AQI_to_db(aqi_df)


if __name__ == '__main__':
    main()

