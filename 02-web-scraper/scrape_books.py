#!/usr/bin/env python3
"""
Politely scrape book listings from books.toscrape.com (practice site).

Extracts title, price, and availability for the first ~20 books
and writes them to output/books.csv.
"""

from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"
OUTPUT_CSV = OUTPUT_DIR / "books.csv"

BASE_URL = "https://books.toscrape.com/"
CATALOGUE_URL = "https://books.toscrape.com/catalogue/page-1.html"
USER_AGENT = (
    "FreelancePortfolioDemo/1.0 (+https://github.com/example/python-automation-demos; "
    "educational scrape of books.toscrape.com)"
)
TARGET_COUNT = 20
TIMEOUT_SECONDS = 20


def fetch(url: str) -> str:
    """GET a page with a polite User-Agent; raise on HTTP errors."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(url, headers=headers, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    response.encoding = response.apparent_encoding or "utf-8"
    return response.text


def parse_books(html: str, limit: int) -> list[dict[str, str]]:
    """Parse product cards into title / price / availability dicts."""
    soup = BeautifulSoup(html, "html.parser")
    books: list[dict[str, str]] = []

    for article in soup.select("article.product_pod"):
        if len(books) >= limit:
            break

        title_el = article.select_one("h3 a")
        price_el = article.select_one("p.price_color")
        avail_el = article.select_one("p.instock.availability")

        title = (title_el.get("title") or title_el.get_text(strip=True)) if title_el else ""
        price = price_el.get_text(strip=True) if price_el else ""
        availability = (
            " ".join(avail_el.get_text(strip=True).split()) if avail_el else ""
        )

        if not title:
            continue

        books.append(
            {
                "title": title,
                "price": price,
                "availability": availability,
            }
        )

    return books


def write_csv(rows: list[dict[str, str]], path: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "availability"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    print(f"Fetching {CATALOGUE_URL} ...")
    try:
        html = fetch(CATALOGUE_URL)
    except requests.RequestException as exc:
        print(f"Catalogue page failed ({exc}); trying homepage ...", file=sys.stderr)
        try:
            time.sleep(1)
            html = fetch(BASE_URL)
        except requests.RequestException as exc2:
            print(f"Error: could not fetch books.toscrape.com: {exc2}", file=sys.stderr)
            return 1

    books = parse_books(html, TARGET_COUNT)
    if not books:
        print("Error: no books parsed from page HTML.", file=sys.stderr)
        return 1

    write_csv(books, OUTPUT_CSV)
    print(f"Wrote {len(books)} books -> {OUTPUT_CSV}")
    for i, book in enumerate(books[:3], start=1):
        print(f"  {i}. {book['title']} | {book['price']} | {book['availability']}")
    if len(books) > 3:
        print(f"  ... and {len(books) - 3} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
