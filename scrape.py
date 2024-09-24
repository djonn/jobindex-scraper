import requests
import json
from parse import parse

page_number_limit = 5000
file = open("output/output.json", "w")

def build_url(min_date: str, max_date: str, page_number: int, categories: list[int]):
    subid = ("").join(f"&subid={x}" for x in categories) if categories != None else ""
    return (
        "https://www.jobindex.dk/jobsoegning?"
        + "&maxdate="
        + max_date
        + "&mindate="
        + min_date
        + "&page="
        + str(page_number)
        + "&archive=1"
        + subid
    )

def write_to_file(datapoint):
    file.write(json.dumps(datapoint))
    file.write(",\n")


def scrape(max_date, min_date, page_number, categories):
    url = build_url(min_date, max_date, page_number, categories)

    print("fetching data from url: {0}".format(url))
    page = requests.get(url)

    if len(page.content) > 0:
        return parse(page.content, write_to_file)

    return True


def format_date(date):
    return ("").join((date).split("-"))


def url_format_date(date):
    return ("").join(date.split("-"))


def run(page_number, min_date, max_date, categories):
    while page_number <= page_number_limit:

        is_done = scrape(
            page_number=page_number, max_date=max_date, min_date=min_date, categories=categories
        )

        if is_done:
            print("DONE!")
            return
        
        page_number += 1


if __name__ == '__main__':
    file.write("[\n")
    run(
        page_number=1,
        min_date="20240801",
        max_date="20240901",
        categories=[11,8,85] # Bygge- og anlægsteknik, Elektroteknik, Maskinteknik
    )
    file.write("]")