# Jobindex Scraper

Scrapes [Jobindex](https://www.jobindex.dk/) using python and BeautifulSoup.
Based on work from [Pedro Madruga](https://github.com/pmadruga/jobindex-scraper).

## Setup (linux)

- `python -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`

## Run

- Set time interval, categories and areas in "scraper/scrape.py"
- `source .venv/bin/activate` (if not done already)
- `python scraper/scrape.py`
