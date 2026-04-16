"""
Zotero 논문 표(CSV)의 저자 열을 바탕으로 OpenAlex에서 소속·ID 등을 추가가

Google Scholar 자동 크롤은 ToS·안정성 이슈로 사용하지 않고,
OpenAlex API(https://openalex.org) 공개 엔드포인트를 사용.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

OPENALEX_AUTHORS = "https://api.openalex.org/authors"


def _mailto_param(mailto: str) -> str:
    return re.sub(r"^mailto:", "", mailto).strip()


def search_author(
    session: requests.Session,
    query: str,
    publication_year: str | float | int | None,
    mailto: str,
) -> dict | None:
    """저자 검색 후 첫 후보 반환. publication_year 가 있으면 counts_by_year 로 약하게 필터."""
    params: dict[str, str] = {
        "search": query,
        "per-page": "5",
        "mailto": _mailto_param(mailto),
    }
    r = session.get(OPENALEX_AUTHORS, params=params, timeout=60)
    if r.status_code != 200:
        return None
    data = r.json()
    results = data.get("results") or []
    if not results:
        return None

    y: int | None = None
    if publication_year is not None and str(publication_year).strip() not in ("", "nan"):
        try:
            y = int(float(publication_year))
        except (TypeError, ValueError):
            y = None

    if y is not None:
        for a in results:
            counts = a.get("counts_by_year") or []
            years = [int(c["year"]) for c in counts if "year" in c]
            if years and min(years) - 2 <= y <= max(years) + 2:
                return a
    return results[0]


def extract_affiliation(author_obj: dict) -> tuple[str | None, str | None, str | None, str | None]:
    inst = author_obj.get("last_known_institution") or {}
    inst_name = inst.get("display_name")
    country = inst.get("country_code")
    oid = author_obj.get("id")
    display = author_obj.get("display_name")
    return display, inst_name, country, oid


def run(
    input_path: Path,
    output_path: Path,
    author_col: str,
    year_col: str | None,
    limit_rows: int | None,
    sleep_sec: float,
    mailto: str,
) -> int:
    df = pd.read_csv(input_path)
    if author_col not in df.columns:
        print(f"Column not found: {author_col}", file=sys.stderr)
        return 1

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "author-affiliation-enrich/1.0 (OpenAlex; RA_data/Cursor)",
        }
    )

    oa_names: list[str | None] = []
    oa_affil: list[str | None] = []
    oa_country: list[str | None] = []
    oa_ids: list[str | None] = []

    n = len(df) if limit_rows is None else min(len(df), limit_rows)
    for i in range(n):
        raw = df.iloc[i][author_col]
        if pd.isna(raw) or str(raw).strip() == "":
            oa_names.append(None)
            oa_affil.append(None)
            oa_country.append(None)
            oa_ids.append(None)
            continue

        year_val = None
        if year_col and year_col in df.columns:
            year_val = df.iloc[i][year_col]

        q = str(raw).strip()
        obj = search_author(session, q, year_val, mailto)
        if obj is None:
            oa_names.append(None)
            oa_affil.append(None)
            oa_country.append(None)
            oa_ids.append(None)
        else:
            disp, inst, country, oid = extract_affiliation(obj)
            oa_names.append(disp)
            oa_affil.append(inst)
            oa_country.append(country)
            oa_ids.append(oid)
        time.sleep(sleep_sec)

    out = df.iloc[:n].copy()
    out["openalex_author_name"] = oa_names
    out["openalex_affiliation"] = oa_affil
    out["openalex_institution_country"] = oa_country
    out["openalex_author_id"] = oa_ids

    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Wrote {len(out)} rows to {output_path}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Enrich author rows using OpenAlex author search.")
    p.add_argument("--input", type=Path, required=True, help="Input CSV (e.g. FINALdata.csv)")
    p.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV (default: Cursor/result/finaldata_openalex.csv)",
    )
    p.add_argument("--author-column", default="Author 1", help="Column with primary author string")
    p.add_argument(
        "--year-column",
        default="Publication Year",
        help="Year column for disambiguation (empty string to disable)",
    )
    p.add_argument("--limit-rows", type=int, default=None, help="Process only first N rows (test).")
    p.add_argument("--sleep", type=float, default=0.2, help="Delay between OpenAlex requests.")
    p.add_argument(
        "--mailto",
        default="mailto:user@example.com",
        help="Contact for OpenAlex polite pool — replace with your email.",
    )
    args = p.parse_args()

    out_path = args.output or (Path(__file__).resolve().parent / "result" / "finaldata_openalex.csv")
    year_col = args.year_column.strip() if args.year_column else None
    return run(
        args.input,
        out_path,
        args.author_column,
        year_col,
        args.limit_rows,
        args.sleep,
        args.mailto,
    )


if __name__ == "__main__":
    raise SystemExit(main())
