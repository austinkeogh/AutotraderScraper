#!/bin/python
import urllib.request
from bs4 import BeautifulSoup
import re
import pandas as pd
from flask import Flask
from example_blueprint import example_blueprint
from datetime import date
import os

app = Flask(__name__)
app.register_blueprint(example_blueprint)

######## Add the make and model specified here ########
make = 'Tesla'
model = 'model s'
car_results = []
########################################################

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
        print("Error getting the number of pages")
        raise
    return int(num_of_pages)


def write_csv(data, filename):
    print("Writing results to CSV file...")
    pd.DataFrame(data, columns = ["Title", "Details", "Cost", "Descriptions", "Attention Grabber"]).to_csv(filename, index=True)


def get_results(url, pages):
    print("Parsing results...\n")
    l = pages
    printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
    for x in range(1, pages):
        soup = bs_setup(url + str(x))
        titles = soup.find_all('h2', attrs={'class': 'listing-title'})
        details = soup.find_all('ul', attrs={'class': 'listing-key-specs'})
        costs = soup.find_all('div', attrs={'class': 'vehicle-price'})
        descriptions = soup.find_all('p', attrs={'class': 'listing-description'})
        atten_grabbers = soup.find_all('p', attrs={'class': 'listing-attention-grabber'})
        printProgressBar(x + 1, l, prefix='Progress:', suffix='Complete', length=50)
        for i, (title, detail, cost, description, atten_grabber) in enumerate(zip(titles, details, costs, descriptions, atten_grabbers)):
            car_results.append([(title.get_text("|", strip=True)), (detail.get_text("|", strip=True)), (cost.get_text()), (description.get_text("|", strip=True)), (atten_grabber.get_text("|", strip=True))])


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def main():
    """
    MAIN... the final maintear, these are the voyages of the mainship mainterprise, its maintaing mission...
    """
    print('AutoTrader Scraping Tool\n')
    print('##########################\n')

    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")
    print("d1 =", d1)
    print(make, model)
    filename = (make + "_" + model + "_" + d1 + ".csv")
    print(filename)
    built_url = url_constructor()
    pagination_value = get_pages(built_url)
    get_results(built_url, pagination_value)

    write_csv(car_results, "file.csv")
    os.rename(r'file.csv', r'file'+(str(date.today()) + '.csv'))
    print("complete!\n")
    print('##########################\n')


if __name__ == "__main__":
    main()

