"""
FRUS (history.state.gov/historicaldocuments) 웹 스크래퍼 — Cursor 개선판.

Past/FRUS crawl.py 와 동일한 CSV 스키마·파일명 규칙을 유지하되,
requests.Session, 행정부 표시명 1회 조회, CLI로 속도·재현성을 높였습니다.
실행 전 사이트 정책·robots.txt 를 확인하고, --max-documents 로 소량 테스트를 권장합니다.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://history.state.gov/historicaldocuments/"
DEFAULT_ADMINS = ["eisenhower", "kennedy", "johnson", "nixon-ford"]
# 문서 페이지 요청 간 기본 간격 (서버 부하 완화; Past 버전은 간격 없음)
DEFAULT_REQUEST_SLEEP_SEC = 0.25


def get_administration_name(session: requests.Session, admin_slug: str) -> str:
    r = session.get(BASE_URL + admin_slug, timeout=60)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")
    tag = soup.find("h1", {"class": "titleStmt1", "data-template": "frus:administration-name"})
    if tag:
        return re.sub(r"\(.*?\)", "", tag.text.strip()).strip()
    return "Unknown Administration"


def scrape_administration(session: requests.Session, admin_slug: str) -> list[tuple[str, str, str]]:
    r = session.get(BASE_URL + admin_slug, timeout=60)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")
    out: list[tuple[str, str, str]] = []
    for c in soup.find_all("a", {"data-template": "app:parse-params"}):
        parts = c.text.split(", ")
        if len(parts) < 1:
            continue
        if len(re.findall("Volume", parts[-1])):
            out.append((c["href"], parts[-1].strip("\n").strip(" "), parts[0].strip("\n").strip(" ")))
        elif len(parts) > 1 and len(re.findall("Volume", parts[-2])):
            out.append(
                (
                    c["href"],
                    parts[-2].strip("\n").strip(" "),
                    parts[0].strip("\n").strip(" ") + "(" + parts[-1].strip("\n").strip(" ") + ")",
                )
            )
        else:
            out.append((c["href"], "No volume info", parts[0].strip("\n").strip(" ")))
    return out


def scrape_volume(session: requests.Session, volume_href: str) -> list[tuple[str, list[int]]]:
    r = session.get(BASE_URL + volume_href, timeout=60)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")
    ret: list[tuple[str, list[int]]] = []
    for i in range(1, 1_000_000):
        c = soup.find("a", id="toc-comp%d" % i)
        if c is None:
            break
        if c.next_sibling is None:
            continue
        docs_id = re.findall(r"\d+", str(c.next_sibling))
        if len(docs_id) == 2:
            ret.append((c.text, list(map(int, docs_id))))
    return ret


def scrape_document(
    session: requests.Session,
    rel_url: str,
    doc_num: int,
    content_title: str,
    administration_display: str,
    volume_safe: str,
    request_sleep_sec: float,
) -> dict:
    time.sleep(request_sleep_sec)
    r = session.get(BASE_URL + rel_url, timeout=60)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "html.parser")

    title_tag = soup.find(["h3", "h4"], class_="tei-head7")
    title = title_tag.get_text(strip=True) if title_tag else "No Title"

    time_tag = soup.find("span", class_="tei-date")
    document_time = time_tag.get_text(strip=True) if time_tag else "No Time"
    document_time = (
        re.sub(r"\s+", " ", document_time)
        .strip("\n")
        .strip()
        .replace("—", " ")
        .replace("p.m.", "pm")
        .replace("a.m.", "am")
    )
    if document_time != "No Time":
        try:
            if len(document_time.split(" ")) == 3:
                document_time = str(datetime.strptime(document_time, "%B %d, %Y")).split(" ")[0]
            else:
                document_time = str(datetime.strptime(document_time, "%B %d, %Y %I %p"))
        except ValueError:
            document_time = "Invalid Time Format"
    else:
        pass

    place_tag = soup.find("span", class_="tei-hi3")
    document_place = place_tag.get_text(strip=True) if place_tag else "No Place"

    content_tag = soup.find("div", id="content-inner")
    tei_p3 = content_tag.find_all("p", class_="tei-p3") if content_tag else []

    def remove_footnote_and_pb1_text(element):
        for footnote in element.find_all(rel="footnote"):
            footnote.decompose()
        for pb1 in element.find_all(class_="tei-pb1"):
            pb1.decompose()
        return element.get_text(" ", strip=True)

    content = (
        " ".join([remove_footnote_and_pb1_text(p) for p in tei_p3]).replace("\n", " ")
        if tei_p3
        else "No Content"
    )
    content = re.sub(r"\s+", " ", content).strip()

    year = document_time.split("-")[0] if document_time != "Invalid Time Format" else "Unknown Year"

    return {
        "Administration": administration_display,
        "Year": year,
        "Volume": volume_safe,
        "Contents Title": content_title,
        "Document Title": re.sub(r"\s+", " ", title).strip("\n").strip(),
        "Document Number": f"Document {doc_num}",
        "Document Time": re.sub(r"\s+", " ", document_time).strip("\n").strip(),
        "Document Place": re.sub(r"\s+", " ", document_place).strip("\n").strip(),
        "Document Content": content,
        "Document Link": BASE_URL + rel_url,
    }


def run(
    output_dir: Path,
    admin_slugs: list[str],
    max_documents: int | None,
    skip_existing: bool,
    request_sleep_sec: float,
) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update(
        {"User-Agent": "FRUS-academic-scraper/1.0 (+https://history.state.gov; research use)"}
    )

    scraped = 0
    stop_all = False

    for adm in admin_slugs:
        if stop_all:
            break
        administration_display = get_administration_name(session, adm)
        volumes = scrape_administration(session, adm)
        for href, volume, name_doc in volumes:
            if max_documents is not None and scraped >= max_documents:
                return 0

            volume_safe = volume.replace("/", ",")
            name_doc_clean = re.sub(r"\s+", " ", name_doc).strip("\n").strip()
            out_name = f"{adm}_{name_doc_clean}_{volume_safe}.csv"
            out_path = output_dir / out_name

            if skip_existing and out_path.exists():
                continue

            documents = scrape_volume(session, href)
            rows: list[dict] = []

            for highest_content_name, idx_doc in documents:
                if stop_all:
                    break
                highest_content_name = re.sub(r"\s+", " ", highest_content_name).strip("\n").strip()
                start_doc, end_doc = idx_doc
                for doc_num in tqdm(
                    range(start_doc, end_doc + 1),
                    desc=f"{adm} / {name_doc_clean[:36]}",
                    leave=False,
                ):
                    if max_documents is not None and scraped >= max_documents:
                        stop_all = True
                        break
                    rel_url = f"{href}/d{doc_num}"
                    rows.append(
                        scrape_document(
                            session,
                            rel_url,
                            doc_num,
                            highest_content_name,
                            administration_display,
                            volume_safe,
                            request_sleep_sec,
                        )
                    )
                    scraped += 1

            if not rows:
                print(f"No rows for {out_name}", file=sys.stderr)
                continue

            df = pd.DataFrame(rows)
            df["Year"] = df["Year"].replace("Unknown Year", None)
            df["Year"] = df["Year"].ffill()
            df.to_csv(out_path, index=False, encoding="utf-8-sig")
            print(f"Wrote {out_path} ({len(df)} rows)")
            if stop_all:
                return 0

    return 0


def main(argv: list[str] | None = None) -> int:
    default_out = Path(__file__).resolve().parent / "result"
    p = argparse.ArgumentParser(
        description="Scrape FRUS documents from history.state.gov into CSV (same layout as Past/FRUS crawl.py)."
    )
    p.add_argument("--output-dir", type=Path, default=default_out, help=f"CSV output directory (default: {default_out})")
    p.add_argument("--admin", action="append", dest="admins", help="Administration slug (repeatable). Default: 4 post-war sets.")
    p.add_argument("--max-documents", type=int, default=None, help="Stop after this many documents (test / throttle).")
    p.add_argument("--no-skip-existing", action="store_true", help="Overwrite CSV if file already exists.")
    p.add_argument(
        "--sleep",
        type=float,
        default=DEFAULT_REQUEST_SLEEP_SEC,
        help=f"Seconds between document HTTP requests (default: {DEFAULT_REQUEST_SLEEP_SEC}).",
    )
    args = p.parse_args(argv)

    sleep_sec = max(0.0, args.sleep)
    admins = args.admins if args.admins else list(DEFAULT_ADMINS)
    return run(
        args.output_dir,
        admins,
        args.max_documents,
        skip_existing=not args.no_skip_existing,
        request_sleep_sec=sleep_sec,
    )


if __name__ == "__main__":
    raise SystemExit(main())
