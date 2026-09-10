# Web Scraper (Books Demo)

Polite Python scraper for [books.toscrape.com](https://books.toscrape.com/) — a site built for scraping practice.

## What it does

- Fetches the first catalogue page with a clear User-Agent
- Extracts **title**, **price**, and **availability** for ~20 books
- Writes `output/books.csv`
- Handles network/HTTP errors cleanly (exit code + message)

## How to run

```bash
cd 02-web-scraper
pip install -r requirements.txt
python scrape_books.py
```

Requires outbound HTTPS access to `books.toscrape.com`.

## Client use cases

- **Price monitoring** — track public product pages over time
- **Lead / listing lists** — collect structured data from public directories
- **Competitor research** — summarize publicly visible catalogue info

## Ethics & terms of service

Only scrape **public** pages you are allowed to access. Respect `robots.txt`, rate limits, and each site’s Terms of Service. Prefer official APIs when available. This demo targets a practice site designed for scraping — production work should get explicit client/legal clearance first.
