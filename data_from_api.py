import requests
import zillow_config as cfg
import json
import pandas as pd


def get_data_from_api(api_url, parameters):
    """ Receives API url and relevant parameters for query (including API key).
     Using request, send request and extract content.
      Returns data in json format"""
    response = requests.get(api_url, parameters)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        pass
        # to implement logger info


def api_data_to_frame(api_data):
    """ Receives content from API, according to query.
         Extracts the data to create data frame relevant to table """
    frame = pd.read_json(api_data, orient='index')
    return frame


def get_air_quality_data(aqi_data):
    if aqi_data['status'] == 'fail':
        # logger
        return None
    return aqi_data['data']['current']['pollution']['aqius']


def main():
    """ Starting function of the program, calls above functions """
    # adding information for schools table from API
    schools_data = get_data_from_api(cfg.SCHOOLS_URL, cfg.SCHOOLS_PARAMETERS)
    schools_df = api_data_to_frame(schools_data)

    # adding information for area table from API
    aqi_data = get_data_from_api(cfg.AQI_URL, cfg.AQI_PARAMETERS)
    aqi_for_city = get_air_quality_data(aqi_data)


if __name__ == '__main__':
    main()
