#!/bin/python
"""Command-line tool for scraping AutoTrader listings."""

import argparse
import logging
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from flask import Flask
from example_blueprint import example_blueprint
from datetime import date


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(example_blueprint)


def url_constructor(make: str, model: str, postcode: str = "M15 4FN") -> str:
    """Construct the base search URL for AutoTrader."""
    base = "https://www.autotrader.co.uk/car-search?"
    params = {
        "sort": "sponsored",
        "radius": 1500,
        "postcode": postcode,
        "onesearchad": ["Used", "Nearly New", "New"],
        "make": make,
        "model": model,
        "page": "",
    }
    return base + urlencode(params, doseq=True)


def bs_setup(url: str) -> BeautifulSoup:
    """Fetch *url* and return a BeautifulSoup parser."""
    response = requests.get(url, headers={"User-Agent": "Magic Browser"}, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_pages(url: str) -> int:
    """Return the total number of result pages for the base URL."""
    soup = bs_setup(url)
    try:
        results = soup.find("h1", attrs={"class": "search-form__count"})
        for result in results.children:
            logger.info("%s...", result)
        page_number = soup.find("li", attrs={"class": "paginationMini__count"})
        search_string = str(page_number.get_text)
        num_of_pages = re.search(r"(\d+)(?!.*\d)", search_string).group(1)
        logger.info("%s pages of results...", num_of_pages)
        return int(num_of_pages)
    except AttributeError as exc:
        logger.exception("Error getting the number of pages")
        raise exc


def write_csv(data, filename: str) -> None:
    """Write scraped *data* to a CSV file named *filename*."""
    logger.info("Writing results to CSV file...")
    pd.DataFrame(
        data,
        columns=["Title", "Details", "Cost", "Descriptions", "Attention Grabber"],
    ).to_csv(filename, index=True)


def get_results(url: str, pages: int):
    """Scrape result pages and return a list of car details."""
    logger.info("Parsing results...")
    car_results = []
    for x in range(1, pages + 1):
        soup = bs_setup(f"{url}{x}")
        titles = soup.find_all("h2", attrs={"class": "listing-title"})
        details = soup.find_all("ul", attrs={"class": "listing-key-specs"})
        costs = soup.find_all("div", attrs={"class": "vehicle-price"})
        descriptions = soup.find_all("p", attrs={"class": "listing-description"})
        atten_grabbers = soup.find_all("p", attrs={"class": "listing-attention-grabber"})
        for title, detail, cost, description, atten_grabber in zip(
            titles, details, costs, descriptions, atten_grabbers
        ):
            if all([title, detail, cost, description, atten_grabber]):
                car_results.append(
                    [
                        title.get_text("|", strip=True),
                        detail.get_text("|", strip=True),
                        cost.get_text(),
                        description.get_text("|", strip=True),
                        atten_grabber.get_text("|", strip=True),
                    ]
                )
    return car_results


def parse_args():
    """Parse command-line arguments for make and model."""
    parser = argparse.ArgumentParser(description="AutoTrader scraping tool")
    parser.add_argument("make", help="Car make to search for")
    parser.add_argument("model", help="Car model to search for")
    return parser.parse_args()


def main() -> None:
    """Run the scraper using command-line arguments."""
    args = parse_args()
    today = date.today()
    filename = f"{args.make}_{args.model}_{today}.csv"
    logger.info("Searching for %s %s", args.make, args.model)
    built_url = url_constructor(args.make, args.model)
    pagination_value = get_pages(built_url)
    car_results = get_results(built_url, pagination_value)
    write_csv(car_results, filename)
    logger.info("Complete! Results written to %s", filename)


if __name__ == "__main__":
    main()

