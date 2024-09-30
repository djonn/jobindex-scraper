import requests
import json
from parse import parse, parse_archive_description

page_number_limit = 100
file = open("output/output.json", "w")
job_listings = []

def build_url(min_date: str, max_date: str, page_number: int, categories: list[int], area: list[int]):
    subid = ("").join(f"&subid={x}" for x in categories) if categories != None else ""
    geoareaid = ("").join(f"&geoareaid={x}" for x in area) if area != None else ""
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
        + geoareaid
    )

def write_to_file(datapoint):
    file.write(json.dumps(datapoint, indent=2))

def remember(datapoint):
    job_listings.append(datapoint)

def scrape_search_page(max_date, min_date, page_number, categories, area):
    url = build_url(min_date, max_date, page_number, categories, area)

    print("fetching data from url: {0}".format(url))
    page = requests.get(url)

    if len(page.content) > 0:
        return parse(page.content, remember)

    return True

def scrape_archived_listing(listing):
    url = listing["archive_link"]

    print("fetching data from url: {0}".format(url))
    page = requests.get(url)

    if len(page.content) > 0:
        listing["description"] = parse_archive_description(page.content)


def scrape_search(page_number, min_date, max_date, categories, area):
    while page_number <= page_number_limit:

        is_done = scrape_search_page(
            page_number=page_number, max_date=max_date, min_date=min_date, categories=categories, area=area
        )

        if is_done:
            print("finished scraping search")
            break
        
        page_number += 1

    print(f"Found {len(job_listings)} from search")


if __name__ == '__main__':
    scrape_search(
        page_number=1,
        min_date="20240801",
        max_date="20240901",
        categories=[11,8,85], # Bygge- og anlægsteknik, Elektroteknik, Maskinteknik
        area=[8] # Aarhus Kommune
    )

    for listing in job_listings:
        scrape_archived_listing(listing)

    write_to_file(job_listings)