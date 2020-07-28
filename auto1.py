#!/bin/python
import urllib.request
import csv
from bs4 import BeautifulSoup
import re
import itertools
import pandas as pd

text_file = open("Autotrader scraping.txt", 'w')
csv_file = open("Autotrader scraping.csv", 'w')


def url_constructor():
    start = "https://www.autotrader.co.uk/car-search?sort=sponsored&radius=1500&"
    postcode = "postcode=M15%204FN"
    middle = "&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&"
    make = "make=TESLA"
    model = "&model=MODEL%20S"
    end = "&page="
    url_string: str = start + postcode + middle + make + model + end
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
            print(result)
        page_number = soup.find('li', attrs={'class': 'paginationMini__count'})
        search_string = str(page_number.get_text)
        num_of_pages = re.search('(\d+)(?!.*\d)', search_string).group(1)
        print(num_of_pages)
    except:
        print("Error getting the listings")
        raise
    return int(num_of_pages)


def txt_to_csv():
    text_file = open("Autotrader scraping.txt", 'r')
    read_file = pd.read_csv(text_file, delimiter='\n')
    read_file.to_csv(csv_file)
    csv_file.close()
    text_file.close()


# def txt_to_xls(): #not working
#     text_file = open("Autotrader scraping.txt", 'r')
#     read_file = pd.read_excel(text_file)
#     print(read_file)
#     read_file.to_excel(xls_file)
#     csv_file.close()
#     text_file.close()

def write_to_file(data):
    text_file.write(str(data))


def write_to_csv(csvData):  # notfinished
    with open('directCSVwrite.csv', 'a') as csvFile:
        writer1 = csv.writer(csvFile)
        writer1.writerow(csvData)
    csvFile.close()


def get_results(url):
    soup = bs_setup(url)
    cars = []
    titles = soup.find_all('h2', attrs={'class': 'listing-title'})
    details = soup.find_all('ul', attrs={'class': 'listing-key-specs'})
    costs = soup.find_all('div', attrs={'class': 'vehicle-price'})
    descriptions = soup.find_all('p', attrs={'class': 'listing-description'})
    atten_grabbers = soup.find_all('p', attrs={'class': 'listing-attention-grabber'})
    for i, (title, detail, cost, description, atten_grabber) in enumerate(zip(titles, details, costs, descriptions, atten_grabbers)):
        cars.append([(title.get_text("|", strip=True)), (detail.get_text("|", strip=True)), (cost.get_text("|", strip=True)), (description.get_text("|", strip=True)), (atten_grabber.get_text("|", strip=True))])
        write_to_csv(cars[i])

    # res = [list(itertools.chain(*i)) for i in zip(titles, details, costs, descriptions, atten_grabbers)]
    # for s in res:
    #     print(*s)

    for title, detail, cost, description, atten_grabber in zip(titles, details, costs, descriptions, atten_grabbers):
        write_to_file("\n --- \n")
        write_to_file("Title: ")
        write_to_file(title.get_text())
        write_to_file(" - \n")
        write_to_file("Details: \n")
        write_to_file(detail.get_text())
        write_to_file(" - \n")
        write_to_file("Cost: \n")
        write_to_file(cost.get_text())
        write_to_file("\n - \n")
        write_to_file("Description: \n")
        write_to_file(description.get_text())
        write_to_file("\n - \n")
        write_to_file("Attention Grabber: \n")
        write_to_file(atten_grabber.get_text())
        write_to_file("\n --- \n")


print('AutoTrader Scraping Tool')
print('##########################\n')

url = url_constructor()

pagination_value = get_pages(url)

for x in range(1, pagination_value):
    get_results(url + str(x))

text_file.close()
txt_to_csv()
