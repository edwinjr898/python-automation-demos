# Freelance Portfolio — Python Automation & Web Demos

Polished, hireable demos for a **Python + JS/TS + web frontend** freelancer — plus a **real-client restaurant site** case study as production proof. Each project is self-contained with a README (and runnable entry point where applicable).

| # | Folder | Stack | What it shows |
|---|--------|-------|----------------|
| 1 | [`01-spreadsheet-cleaner/`](01-spreadsheet-cleaner/) | Python, pandas | Clean messy CSVs → client-ready exports + summary |
| 2 | [`02-web-scraper/`](02-web-scraper/) | Python, requests, BeautifulSoup | Polite public-page scrape → structured CSV |
| 3 | [`03-invoice-estimator/`](03-invoice-estimator/) | HTML / CSS / JS | Zero-build client quote tool |
| 4 | [`04-inka-brasas-case-study/`](04-inka-brasas-case-study/) | HTML, CSS, JS, Python, Netlify | Real-client restaurant marketing site ([inkabrasas.com](https://inkabrasas.com)) |

## Suggested GitHub repo name

`python-automation-demos`

(or `freelance-python-web-demos` if you want the frontend demos + restaurant proof in the name)

## Quick start

```bash
# Demo 1
cd 01-spreadsheet-cleaner && pip install -r requirements.txt && python clean_sales.py

# Demo 2
cd ../02-web-scraper && pip install -r requirements.txt && python scrape_books.py

# Demo 3 — open in a browser
cd ../03-invoice-estimator && python -m http.server 8080

# Case study 4 — public write-up only (live site linked in README)
# open 04-inka-brasas-case-study/README.md
```

## Portfolio tips

- Pin a short Loom or GIF of each demo running
- Swap sample data for anonymized client-shaped examples (with permission)
- Link this repo from your Upwork / LinkedIn / personal site as proof of delivery quality
- Point prospects at the live Inka Brasas site as real hospitality / restaurant work
