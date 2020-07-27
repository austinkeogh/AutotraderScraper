#!/bin/python
import urllib.request
import sys
import csv
from bs4 import BeautifulSoup
from time import gmtime, strftime
import pandas as pd

urlx="https://www.autotrader.co.uk/car-search?sort=sponsored&radius=1500&postcode=M15%204FN&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&make=TESLA&model=MODEL%20S&page="

#make = "TESLA"
#model = "MODEL%20S"

text_file = open("Autotrader scraping.txt",'w')
csv_file = open("Autotrader scraping.csv",'w')
xls_file = open("Autotrader scraping.xls",'w')

def txt_to_csv():
    text_file = open("Autotrader scraping.txt", 'r')
    read_file = pd.read_csv(text_file, delimiter='\n')
    print(read_file)
    read_file.to_csv(csv_file)
    csv_file.close()

def txt_to_xls(): #not working
    text_file = open("Autotrader scraping.txt", 'r')
    read_file = pd.read_excel(text_file)
    print(read_file)
    read_file.to_excel(xls_file)
    csv_file.close()

def write_to_file(data):
    text_file.write(str(data))

def write_to_csv(csvData): # notfinished
    with open('person.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(csvData)
        print(csvData)
    csvFile.close()

def get_results(url):
    req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
    #req = urllib.request.FancyURLopener({"http":"http://127.0.0.1:8080"}).open(url).read().decode("utf-8")
    #print(req)
    con = urllib.request.urlopen( req )
    #print (con)
    html=con.read()
    #print (html)
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
print(text_file)
text_file.close()
txt_to_csv()


