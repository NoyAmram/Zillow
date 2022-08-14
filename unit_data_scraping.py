from bs4 import BeautifulSoup
import requests
import zillow_config as cfg
import json
import pandas as pd

url_page = ""


def data_parse(url_page):
    """ Receives one url, each represents house link from the main search scraping.
     Using request, send request for each url and extract content using BeautifulSoup library.
      Returns soup object"""
    response = requests.get(url_page, headers=cfg.HEADER)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def scrape_price_history(soup): #Noy
    """ Receives soup object, extract the content of price_history
            and returns list/dictionary of the data """
    pass


def scrape_features(soup): #Jia
    """ Receives soup object, extract the content of features (beds, baths,
    common_walls, parking_space) and returns list/dictionary of the data """
    pass


def scrape_monthly_cost(soup): #Noy
    """ Receives soup object, extract the content of monthly_cost for this unit
     and returns list/dictionary of the data """
    pass


def scrape_nearby_schools(soup): #Jia
    """ Receives soup object, extract the content of nearby_schools for this unit
         and returns list/dictionary of the data """
    pass


def main():
    """ Starting function of the program, calls above functions """
    data_parse(url_page)


if __name__ == '__main__':
    main()
