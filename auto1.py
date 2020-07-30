#!/bin/python
import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd

make = 'Tesla'
model = 'Model S'
car_results = []

def url_constructor():
    start = "https://www.autotrader.co.uk/car-search?sort=sponsored&radius=1500&"
    postcode = "postcode=M15%204FN"
    middle = "&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New"
    car_make = "&make=" + make.replace(" ", "%20")
    car_model = "&model=" + model.replace(" ", "%20")
    end = "&page="
    url_string: str = start + postcode + middle + car_make + car_model + end
    return url_string


def bs_setup(url):
    req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
    con = urllib.request.urlopen(req)
    html = con.read()
    soup = BeautifulSoup(html, features="html.parser")
    return soup


def get_pages(url):
    soup = bs_setup(url)
    try:
        results = soup.find('h1', attrs={'class': 'search-form__count'})
        for result in results.children:
            print(result + "...")
        page_number = soup.find('li', attrs={'class': 'paginationMini__count'})
        search_string = str(page_number.get_text)
        num_of_pages = re.search('(\d+)(?!.*\d)', search_string).group(1)
        print(num_of_pages + " pages of results...\n")
    except:
        print("Error getting the listings")
        raise
    return int(num_of_pages)


def write_csv(data, filename):
    pd.DataFrame(data, columns = ["Title", "Details", "Cost", "Descriptions", "Attention Grabber"]).to_csv(filename, index=True)


def get_results(url):
    soup = bs_setup(url)
    titles = soup.find_all('h2', attrs={'class': 'listing-title'})
    details = soup.find_all('ul', attrs={'class': 'listing-key-specs'})
    costs = soup.find_all('div', attrs={'class': 'vehicle-price'})
    descriptions = soup.find_all('p', attrs={'class': 'listing-description'})
    atten_grabbers = soup.find_all('p', attrs={'class': 'listing-attention-grabber'})
    for i, (title, detail, cost, description, atten_grabber) in enumerate(zip(titles, details, costs, descriptions, atten_grabbers)):
        car_results.append([(title.get_text("|", strip=True)), (detail.get_text("|", strip=True)), (cost.get_text()), (description.get_text("|", strip=True)), (atten_grabber.get_text("|", strip=True))])

print('AutoTrader Scraping Tool')
print('##########################\n')

url = url_constructor()
pagination_value = get_pages(url)

for x in range(1, pagination_value):
    get_results(url + str(x))

write_csv(car_results, "file.csv")
print('##########################\n')