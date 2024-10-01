from os import path, makedirs
import json
import re

file_path = path.dirname(path.abspath(__file__))
wordlist_path = path.join(file_path, "cor1.02.tsv")
categories_path = path.join(file_path, "category_to_subid_mapping.json")

export_path = path.abspath(path.join(file_path, path.pardir, "output"))
listings_path = path.join(export_path, "scraped_data.json")
result_path = path.join(export_path, "adjective_counts_by_category.json")

def create_adjective_lookup():
    adjective_lookup = {}

    with open(wordlist_path, "r") as input:
        for line in input:
            cells = line.strip("\n").split("\t")

            lemma = cells[1]
            types = cells[3]
            fullform = cells[4]

            if "adj" in types:
                adjective_lookup[fullform] = lemma

    return adjective_lookup


def load_category_mappings():
    with open(categories_path, "r") as file:
        categories = json.load(file)
    return categories


def load_listings():
    category_mappings = load_category_mappings()

    with open(listings_path, "r") as file:
        listings = json.load(file)

    for listing in listings:
        listing["category"] = category_mappings.get(str(listing["category"]))

    return listings


def write_to_file(datapoint):
    makedirs(path.dirname(result_path), exist_ok=True)
    file = open(result_path, "w")
    file.write(json.dumps(datapoint, indent=2, ensure_ascii=False))


def find_adjectives(listing: list[object], lookup: dict[str, str]):
    description = listing["description"]

    found = []

    for fullform in lookup.values():
        check = rf"\b{fullform}\b"
        if re.search(check, description, re.IGNORECASE):
            found.append(lookup[fullform])

    return found


def count(words: list[str]) -> object:
    result = {}

    for word in words:
        result[word] = result.get(word, 0) + 1

    return result


def analyze(listings, lookup):
    category_adjectives = {}

    i=0
    n=len(listings)

    for listing in listings:
        i=i+1
        print(f"({i}/{n}) Analysing \"{listing['title']}\"")

        adjectives = find_adjectives(listing, lookup)
        combined = category_adjectives.get(listing["category"], []) + adjectives
        category_adjectives[listing["category"]] = combined

    print()

    category_adjectives_counted = {}
    for category in category_adjectives:
        adjectives_counted = count(category_adjectives[category])
        category_adjectives_counted[category] = adjectives_counted
        print(f"\"{category}\" contains {len(category_adjectives[category])} adjectives with {len(adjectives_counted)} being unique")

    return category_adjectives_counted


if __name__ == "__main__":
    lookup = create_adjective_lookup()
    listings = [x for x in load_listings() if x.get("description")]

    adjective_counts_by_category = analyze(listings, lookup)

    write_to_file(adjective_counts_by_category)
