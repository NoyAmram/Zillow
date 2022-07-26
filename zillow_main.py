import os
import sys
from bs4 import BeautifulSoup
import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# import chromedriver_autoinstaller
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
import zillow_config as cfg
import json


# def set_driver():
#     chromedriver_autoinstaller.install()
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome()
#     return driver


def web_parse(url):
    """ Receives  URL extracts to complete ,using BeautifulSoup library"""
    # response = requests.get(url, headers=cfg.HEADER)
    # if response.status_code == 200:
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     return soup
    with requests.Session() as session:
        response = session.get(url, headers=cfg.HEADER)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def data_scraping(web_soup):
    """ Receives soup object, extract the content using json and returns data for each house as dictionary """
    data = json.loads(
        web_soup.select_one("script[data-zrr-shared-data-key]")
        .contents[0]
        .strip("!<>-")
    )
    all_data = data['cat1']['searchResults']['listResults']
    return all_data


def select_data(web_data):
    """ Receives site content containing all data for each house as dictionary.
     Extracts from the data: price, address, area, room number and link for each house """
    for i in range(len(web_data)):
        address = web_data[i]['address']
        area = web_data[i]['area']
        bed_rooms = web_data[i]['beds']
        bath_rooms = web_data[i]['baths']

        # some items have the 'price' key nested inside units key, while others have simply inside data key
        try:
            price = web_data[i]['units'][0]['price']
        except KeyError:
            price = web_data[i]['price']

        link = web_data[i]['detailUrl']
        # Some links do not contain the starting website url, inserting pattern of https://www.zillow.com
        if 'http' not in link:
            link_to_buy = cfg.PATTERN + link
        else:
            link_to_buy = link

        print(f"{address} | {price} | {link_to_buy} | {area} sqft | {bed_rooms} bed rooms | {bath_rooms} bath rooms")


def main():
    """ Starting function of the program, calls above functions """
    data_soup = web_parse(cfg.URL)
    data = data_scraping(data_soup)
    print(data)
    # select_data(data)


if __name__ == '__main__':
    main()
