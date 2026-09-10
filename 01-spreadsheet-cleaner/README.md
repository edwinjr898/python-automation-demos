# Spreadsheet Cleaner (Sales CSV)

Python demo that turns a messy sales export into a clean, analysis-ready CSV.

## What it does

- Normalizes column headers to consistent `snake_case`
- Trims whitespace and collapses extra spaces
- Parses mixed date formats into ISO `YYYY-MM-DD`
- Drops exact duplicate rows
- Fills or flags missing values (medians for numbers, `UNKNOWN` for labels)

## How to run

```bash
cd 01-spreadsheet-cleaner
pip install -r requirements.txt
python clean_sales.py
```

Outputs:

- `output/clean_sales.csv` — cleaned data
- `output/summary_report.txt` — row counts, duplicates removed, nulls handled

Sample input lives in `sample_data/messy_sales.csv`.

## Why a client would hire this

Operations, finance, and marketing teams often receive exports with inconsistent headers, mixed dates, duplicates, and blank cells. A short custom cleaner saves hours of manual Excel work and makes data safe for dashboards, invoicing, or CRM imports. Freelancers can adapt this pattern to any recurring CSV/Excel cleanup job.
