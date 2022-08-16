import requests
import zillow_config as cfg
import pandas as pd
from us_state_dictionary import abbrev_to_us_state
import log

logger = log.setup_custom_logger(__name__)


def get_parameter(input_city, input_state):
    try:
        state = abbrev_to_us_state[input_state]
    except KeyError:
        logger.warning(f'Given state argument %s does not match any known state in dictionary', input_state)
        pass
    else:
        city = ' '.join(input_city.split('-'))
        aqi_parameters = {
            "city": city,
            "state": state,
            "country": cfg.COUNTRY,
            "key": cfg.AQI_API_KEY
        }
        return aqi_parameters


def get_data_from_api(api_url, parameters):
    """ Receives API url and relevant parameters for query (including API key).
     Using request, send request and extract content.
      Returns data in json format"""
    response = requests.get(api_url, params=parameters)
    if response.status_code == 200:
        data = response.json()
        logger.info(f'Successful response from API: %s', api_url)
        return data
    else:
        logger.error(f'Unsuccessful response from from API: %s', api_url)


def api_data_to_frame(api_data):
    """ Receives content from API, according to query.
         Extracts the data to create data frame relevant to table """
    frame = pd.read_json(api_data, orient='index')
    return frame


def get_air_quality_data(aqi_data):
    if aqi_data['status'] == 'fail':
        logger.error(f'API fail to give valid data, check warnings for given arguments')
        return
    logger.info("Successful to get data from API")
    return aqi_data['data']['current']['pollution']['aqius']


def get_aqi_table(search_city, search_state):
    """ Function will be called from Zillow main, receives query city and state.
    Calls relevant functions to get data from the API.
    Returns data of air quality index for query city in data frame"""
    aqi_data = get_data_from_api(cfg.AQI_URL, get_parameter(input_city=search_city, input_state=search_state))
    aqi_for_city = get_air_quality_data(aqi_data)
    aqi_df = pd.DataFrame({'city': [search_city], 'AQI': [aqi_for_city]})
    return aqi_df


def get_school_table():
    """ Function will be called from Zillow main, receives query city.
    Calls relevant functions to get data from the API.
    Returns data of schools for query city in data frame"""
    # adding information for schools table from API
    #schools_data = get_data_from_api(cfg.SCHOOLS_URL, cfg.SCHOOLS_PARAMETERS)
    #schools_df = api_data_to_frame(schools_data)
    pass
