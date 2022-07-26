from bs4 import BeautifulSoup
import requests
import zillow_config as cfg
import json
import pandas as pd
from tqdm import tqdm
import argparse
import warnings
warnings.filterwarnings('ignore')


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
    return city, state, num_pages


def get_pages_url(url, end_page):
    """ Creates and returns list of unique url for each search page """
    url_list = [url + str(i) + '_p/' for i in range(cfg.START_PAGE, end_page)]
    url_list.insert(0, url)  # url of first page has no page number
    return url_list


def web_parse(url_pages):
    """ Receives list of urls differentiate with page numbers.
     Using requests.Session() send request for each url.
     Content extracted for each response text using BeautifulSoup library """
    with requests.Session() as session:
        response_list = [session.get(url, headers=cfg.HEADER) for url in tqdm(url_pages)]
    soup_list = [BeautifulSoup(response.text, 'html.parser') for response in tqdm(response_list)]
    return soup_list


def data_scraping(web_soup_list):
    """ Receives list of soup objects, extract the content using json
        and returns list of all data, dictionary for each house """
    all_data = [json.loads(
        web_soup.select_one("script[data-zrr-shared-data-key]")
        .contents[0]
        .strip("!<>-")) for web_soup in tqdm(web_soup_list)]
    return all_data


def data_to_frame(web_data, frame):
    """ Receives site content from search pages, according to provided number of pages to extract from.
        The data containing all information for each house as dictionary.
         Extracts the data to create data frame """
    for data in web_data:
        for item in data['cat1']['searchResults']['listResults']:
            frame = frame.append(item, ignore_index=True)
    return frame


def main():
    """ Starting function of the program, calls above functions """
    arguments = get_arguments()
    search_url = cfg.BASE_URL + arguments[0] + ',_' + arguments[1] + '_rb/'
    url_pages = get_pages_url(search_url, arguments[2])
    data_soup = web_parse(url_pages)
    data = data_scraping(data_soup)
    frame = pd.DataFrame()
    house_df = data_to_frame(data, frame)
    print(house_df)


if __name__ == '__main__':
    main()
