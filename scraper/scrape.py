import requests
import json
from parse import parse, parse_archive_description

page_number_limit = 100

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
    file = open("output/scraped_data.json", "w")
    file.write(json.dumps(datapoint, indent=2))

def scrape_search_page(max_date, min_date, page_number, categories, area) -> tuple[bool, list[object]]:
    url = build_url(min_date, max_date, page_number, categories, area)

    print("fetching data from url: {0}".format(url))
    page = requests.get(url)

    if len(page.content) > 0:
        was_last_page, postings = parse(page.content)
        return was_last_page, postings

    return True, []

def scrape_archived_listing(listing):
    url = listing["archive_link"]

    print("fetching data from url: {0}".format(url))
    page = requests.get(url)

    if len(page.content) > 0:
        listing["description"] = parse_archive_description(page.content)


def scrape_search(page_number, min_date, max_date, categories, area):
    all_listings: list[object] = []

    while page_number <= page_number_limit:

        is_done, listings_in_page = scrape_search_page(
            page_number=page_number, max_date=max_date, min_date=min_date, categories=categories, area=area
        )

        all_listings = all_listings + listings_in_page

        if is_done:
            break
        
        page_number += 1

    print(f"Found {len(all_listings)} from search")
    return all_listings


if __name__ == '__main__':
    categories=[11,8,85] # Bygge- og anlægsteknik, Elektroteknik, Maskinteknik
    areas=[8] # Aarhus Kommune

    all_listings: list[object] = []

    for category in categories:
        for area in areas:
            search_listings = scrape_search(
                page_number=1,
                min_date="20240801",
                max_date="20240901",
                categories=[category], # Bygge- og anlægsteknik, Elektroteknik, Maskinteknik
                area=[area] # Aarhus Kommune
            )
            for listing in search_listings:
                listing["category"] = category
                listing["area"] = area

            all_listings = all_listings + search_listings


    for listing in all_listings:
        scrape_archived_listing(listing)

    write_to_file(all_listings)