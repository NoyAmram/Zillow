from bs4 import BeautifulSoup
import requests
import zillow_config as cfg
import json
import pandas as pd
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


def get_pages_url():
    """ Creates and returns list of unique url for each search page """
    url_list = [cfg.URL + str(i) + '_p/' for i in range(cfg.START_PAGE, cfg.NUM_PAGE)]
    url_list.insert(0, cfg.URL)  # url of first page has no page number
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
    url_pages = get_pages_url()
    data_soup = web_parse(url_pages)
    data = data_scraping(data_soup)
    frame = pd.DataFrame()
    house_df = data_to_frame(data, frame)
    print(house_df)


if __name__ == '__main__':
    main()
