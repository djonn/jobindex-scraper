# Jobindex Scraper

Scrapes [Jobindex](https://www.jobindex.dk/) using python and BeautifulSoup.
Based on work from [Pedro Madruga](https://github.com/pmadruga/jobindex-scraper).

Additionally counts occurences of adjectives in the found job listings.
Uses ["Det Centrale Ordregister" COR (en: The Central Word Register)](https://ordregister.dk/) for a list of adjectives.

## Setup (linux)

- `python -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`

## Run

- Set time interval, categories and areas in "scraper/scrape.py"
- `source .venv/bin/activate` (if not done already)
- `python scraper/scrape.py` to start scraping jobindex
- `python analysis/analyzer.py` to find adjectives and count them by listing category