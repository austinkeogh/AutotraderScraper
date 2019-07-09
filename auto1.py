#!/bin/python
import urllib.request
import sys
import csv
from bs4 import BeautifulSoup
from time import gmtime, strftime

urlx="https://www.autotrader.co.uk/car-search?sort=sponsored&radius=1500&postcode=M15%204FN&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&make=TESLA&model=MODEL%20S&page="

#make = "TESLA"
#model = "MODEL%20S"

output_file = open("Autotrader scraping.txt",'w')

def write_to_file(data):
    output_file.write(str(data))

def write_to_csv(csvData): # notfinished
    #csvData = [['Person', 'Age'], ['Peter', '22'], ['Jasmine', '21'], ['Sam', '24']]
    with open('person.csv', 'w') as csvFile:
        dialect = csv.excel_tab
        writer = csv.writer(csvFile)
        writer.writerow(csvData)
        print(csvData)
    csvFile.close()

def get_results(url):
    #req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    req = urllib.request.FancyURLopener({"http":"http://127.0.0.1:8080"}).open(url).read().decode("utf-8")
    print(req)
    con = urllib.request.urlopen( req )
    print (con)
    html=con.read()
    print (html)
    soup = BeautifulSoup(html, features="html.parser")
    
    try: 
        listings = soup.find_all('div', attrs={'class': 'js-search-results'})

    except:
        print("Error getting the listings")
        raise
    for listing in listings:
        details = listing.find_all('ul', attrs={'class': 'listing-key-specs'})
        costs = listing.find_all('div', attrs={'class': 'vehicle-price'})
        descriptions = listing.find_all('p', attrs={'class': 'listing-description'})
        for detail, cost, description in zip (details, costs, descriptions):
            write_to_file("\n - \n")
            write_to_file(detail.get_text())
            write_to_file(cost.get_text())
            write_to_file("\n")
            write_to_file(description.get_text())
            write_to_file("\n - \n")

print ('###### AutoTrader Scraping Tool')
print ('##########################################################################\n')
for x in range (1, 15):
    get_results(urlx + str(x))
output_file.close()
#txt_to_csv

