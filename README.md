# Data mining project based on Zillow
## 

[![a pic from zillow website - is it okay to take pic like this? ](https://s.zillowstatic.com/pfs/static/footer-art.svg)](https://s.zillowstatic.com/pfs/static/footer-art.svg)


Zillow is an American tech real-estate marketplace company. In their website www.zillow.com it lists information of different types of real-estate properties such as houses, apartments, villas, to rent and to buy. In addition, Zillow also has their own tool 'Zestimate' to estimate the value of real-estate properties. 



## What data is scraped? 

- Prices of real-estate properties in San Francisco, CA, USA 
- real-estate types: Townhouse, house, apartment 
- Size of the properties: quantity of bedrooms, bathrooms and total area. 
- Addresses of the properties 
- links of the properties 
- maybe zestimate value?
- xxxxx

## Requirements for this data scraping:
- requests~=2.28.1
- bs4~=0.0.1
- beautifulsoup4~=4.11.1

## How did we scrape the data? 
Data scraping is done by using python package BeautifulSoup, Requests and bs4. First a list of configs is shown as below: 
```python
URL = "https://www.zillow.com/homes/San-Francisco,-CA_rb/"

HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

PATTERN = "https://www.zillow.com"
```
We start with a function web_parse(), which reveives URL that needs to be parsed. Then by using 'response.status_code == 200', we check if the request is successful and the server responds with the data we are requesting. If the server responded, a soup object would be created and returned. 

```python
def web_parse(url):
    """ Receives URL, create soup object using BeautifulSoup library"""
    response = requests.get(url, headers=cfg.HEADER)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
```
After creating soup object, function data_scraping() is used to scrape data for each house. Package Json is used and data for each item is returned in dictionary form.

```python
def data_scraping(web_soup):
    """ Receives soup object, extract the content using json and returns data for each house as dictionary """
    data = json.loads(
        web_soup.select_one("script[data-zrr-shared-data-key]")
        .contents[0]
        .strip("!<>-")
    )
    all_data = data['cat1']['searchResults']['listResults']
    return all_data
```


## Some insights

## License 
