#!/usr/bin/env python3
"""
Clean messy sales CSV data for client handoff.

Normalizes headers, trims whitespace, parses dates to ISO,
drops exact duplicates, and fills/flags missing values.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
INPUT_CSV = ROOT / "sample_data" / "messy_sales.csv"
OUTPUT_DIR = ROOT / "output"
CLEAN_CSV = OUTPUT_DIR / "clean_sales.csv"
SUMMARY_TXT = OUTPUT_DIR / "summary_report.txt"

HEADER_MAP = {
    "orderid": "order_id",
    "order_id": "order_id",
    "customername": "customer_name",
    "customer_name": "customer_name",
    "orderdate": "order_date",
    "order_date": "order_date",
    "product": "product",
    "quantity": "quantity",
    "unitprice": "unit_price",
    "unit_price": "unit_price",
    "region": "region",
}

DATE_FORMATS = (
    "%m/%d/%Y",
    "%m/%d/%y",
    "%Y-%m-%d",
    "%d-%b-%Y",
    "%b %d %Y",
    "%B %d %Y",
    "%Y/%m/%d",
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%m-%d-%Y",
    "%Y.%m.%d",
    "%d.%m.%Y",
)


def normalize_header(name: str) -> str:
    cleaned = re.sub(r"\s+", " ", str(name).strip()).lower()
    key = re.sub(r"[^a-z0-9_]", "", cleaned.replace(" ", ""))
    return HEADER_MAP.get(key, cleaned.replace(" ", "_"))


def parse_one_date(value) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = re.sub(r"\s+", " ", str(value).strip())
    if not text or text.lower() in {"nan", "none", "nat"}:
        return None
    for fmt in DATE_FORMATS:
        try:
            return pd.to_datetime(text, format=fmt).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            continue
    # Last resort: let pandas infer without dayfirst bias
    parsed = pd.to_datetime(text, errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed.strftime("%Y-%m-%d")


def trim_series(series: pd.Series) -> pd.Series:
    return series.map(
        lambda x: re.sub(r"\s+", " ", str(x).strip())
        if x is not None and not (isinstance(x, float) and pd.isna(x)) and str(x).lower() != "nan"
        else pd.NA
    )


def clean(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    stats: dict = {
        "rows_in": len(df),
        "duplicates_removed": 0,
        "nulls_filled": {},
        "nulls_flagged": {},
    }

    df = df.copy()
    df.columns = [normalize_header(c) for c in df.columns]

    # Trim all non-numeric text-like columns
    for col in df.columns:
        if col in ("quantity", "unit_price", "order_id"):
            continue
        df[col] = trim_series(df[col])
        df[col] = df[col].replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})

    if "order_date" in df.columns:
        df["order_date"] = df["order_date"].map(parse_one_date)

    for col in ("quantity", "unit_price", "order_id"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    before = len(df)
    df = df.drop_duplicates()
    stats["duplicates_removed"] = before - len(df)

    if "customer_name" in df.columns:
        n = int(df["customer_name"].isna().sum())
        if n:
            df["customer_name"] = df["customer_name"].fillna("UNKNOWN")
            stats["nulls_filled"]["customer_name"] = n

    if "region" in df.columns:
        n = int(df["region"].isna().sum())
        if n:
            df["region"] = df["region"].fillna("UNKNOWN")
            stats["nulls_filled"]["region"] = n

    if "quantity" in df.columns:
        n = int(df["quantity"].isna().sum())
        if n:
            fill = df["quantity"].median()
            if pd.isna(fill):
                fill = 1
            df["quantity"] = df["quantity"].fillna(fill).astype(int)
            stats["nulls_filled"]["quantity"] = n
        else:
            df["quantity"] = df["quantity"].astype(int)

    if "unit_price" in df.columns:
        n = int(df["unit_price"].isna().sum())
        if n:
            if "product" in df.columns:
                df["unit_price"] = df.groupby("product")["unit_price"].transform(
                    lambda s: s.fillna(s.median())
                )
            overall = df["unit_price"].median()
            df["unit_price"] = df["unit_price"].fillna(overall)
            stats["nulls_filled"]["unit_price"] = n
        df["unit_price"] = df["unit_price"].round(2)

    if "order_date" in df.columns:
        n = int(df["order_date"].isna().sum())
        if n:
            stats["nulls_flagged"]["order_date"] = n

    if "product" in df.columns:
        n = int(df["product"].isna().sum())
        if n:
            df["product"] = df["product"].fillna("UNKNOWN")
            stats["nulls_filled"]["product"] = n

    if "order_id" in df.columns:
        df["order_id"] = df["order_id"].astype("Int64")

    preferred = [
        "order_id",
        "customer_name",
        "order_date",
        "product",
        "quantity",
        "unit_price",
        "region",
    ]
    cols = [c for c in preferred if c in df.columns] + [
        c for c in df.columns if c not in preferred
    ]
    df = df[cols].reset_index(drop=True)

    stats["rows_out"] = len(df)
    return df, stats


def write_summary(stats: dict) -> None:
    lines = [
        "Sales CSV Cleaning Summary",
        "=" * 40,
        f"Rows in:              {stats['rows_in']}",
        f"Rows out:             {stats['rows_out']}",
        f"Duplicates removed:   {stats['duplicates_removed']}",
        "",
        "Nulls filled:",
    ]
    if stats["nulls_filled"]:
        for col, n in stats["nulls_filled"].items():
            lines.append(f"  - {col}: {n}")
    else:
        lines.append("  (none)")

    lines.append("")
    lines.append("Nulls flagged (left blank):")
    if stats["nulls_flagged"]:
        for col, n in stats["nulls_flagged"].items():
            lines.append(f"  - {col}: {n}")
    else:
        lines.append("  (none)")

    lines.append("")
    lines.append("Notes:")
    lines.append("  - Headers normalized to snake_case")
    lines.append("  - Whitespace trimmed; dates converted to ISO YYYY-MM-DD")
    lines.append("  - Exact duplicate rows dropped")
    lines.append("  - Missing names/regions filled with UNKNOWN")
    lines.append("  - Missing quantity/price filled with medians")
    SUMMARY_TXT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    raw = pd.read_csv(INPUT_CSV)
    cleaned, stats = clean(raw)
    cleaned.to_csv(CLEAN_CSV, index=False)
    write_summary(stats)
    print(f"Wrote {CLEAN_CSV} ({stats['rows_out']} rows)")
    print(f"Wrote {SUMMARY_TXT}")
    print(
        f"In={stats['rows_in']} Out={stats['rows_out']} "
        f"Dupes={stats['duplicates_removed']}"
    )


if __name__ == "__main__":
    main()
