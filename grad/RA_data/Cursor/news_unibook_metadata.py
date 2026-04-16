"""
통일부 유니북(unibook) 자료 URL에서 서지 6필드를 한 행 CSV로 저장.

Past/News.ipynb 와 동일 CSS selector 사용.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

SELECTORS = {
    "주기사명": "div.biblio_info > div.info_list > dl:nth-of-type(1) > dd",
    "서명": "div.biblio_info > div.info_list > dl:nth-of-type(2) > dd",
    "권호": "div.biblio_info > div.info_list > dl:nth-of-type(3) > dd",
    "발행처": "div.biblio_info > div.info_list > dl:nth-of-type(4) > dd",
    "발행일자": "div.biblio_info > div.info_list > dl:nth-of-type(5) > dd",
    "페이지": "div.biblio_info > div.info_list > dl:nth-of-type(6) > dd",
}


def fetch_row(url: str, timeout: int = 60) -> dict[str, str | None]:
    r = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "news-unibook-metadata/1.0 (research; RA_data/Cursor)"},
    )
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")
    out: dict[str, str | None] = {}
    for key, sel in SELECTORS.items():
        els = soup.select(sel)
        out[key] = els[0].get_text(strip=True) if els else None
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="Scrape one Unibook material page into a 1-row metadata CSV.")
    p.add_argument("--url", required=True, help="Full unibook.unikorea.go.kr material view URL")
    p.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output CSV path (default: Cursor/result/news_row.csv)",
    )
    args = p.parse_args()
    out_path = args.output or (Path(__file__).resolve().parent / "result" / "news_row.csv")

    try:
        row = fetch_row(args.url)
    except Exception as e:
        print(f"Failed: {e}", file=sys.stderr)
        return 1

    df = pd.DataFrame([row])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
