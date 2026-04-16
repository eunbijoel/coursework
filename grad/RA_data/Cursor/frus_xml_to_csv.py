"""
HistoryAtState/frus GitHub `volumes/*.xml` → 단일(또는 분할) CSV.

Past/FRUS XML.py 의 [1] TEI 파서 로직과 동일한 컬럼 스키마를 유지합니다.
원본: https://github.com/HistoryAtState/frus/tree/master/volumes
"""

from __future__ import annotations

import argparse
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm

RAW_BASE = "https://raw.githubusercontent.com/HistoryAtState/frus/master/volumes/"
GITHUB_TREE = "https://api.github.com/repos/HistoryAtState/frus/git/trees/master"
NS = {"tei": "http://www.tei-c.org/ns/1.0"}


def list_volume_xmls(session: requests.Session, max_files: int | None) -> list[str]:
    """Git tree API로 volumes/ 아래 .xml 목록 수집."""
    r = session.get(f"{GITHUB_TREE}?recursive=1", timeout=120)
    r.raise_for_status()
    data = r.json()
    names: list[str] = []
    for item in data.get("tree", []):
        path = item.get("path", "")
        if path.startswith("volumes/") and path.endswith(".xml") and item.get("type") == "blob":
            names.append(path.split("/", 1)[-1])
    names.sort()
    if max_files is not None:
        names = names[: max_files]
    return names


def parse_volume_xml(content: bytes, file_name: str) -> list[dict]:
    all_documents: list[dict] = []
    root = ET.fromstring(content)
    tei_header = root.find("tei:teiHeader", NS)
    volume_name = "Unknown Volume"
    if tei_header is not None:
        title_stmt = tei_header.find("tei:fileDesc/tei:titleStmt", NS)
        if title_stmt is not None:
            for title in title_stmt.findall("tei:title", NS):
                if title.attrib.get("type") == "series" and title.text:
                    volume_name = title.text.strip()

    volume_id = root.attrib.get("{http://www.w3.org/XML/1998/namespace}id", file_name.replace(".xml", ""))
    body = root.find("tei:text/tei:body", NS)
    if body is None:
        return all_documents

    for comp in body.findall(".//tei:div[@type='compilation']", NS):
        contents_title_elem = comp.find("tei:head", NS)
        if contents_title_elem is not None and contents_title_elem.text:
            contents_title = contents_title_elem.text.strip()
        else:
            contents_title = "Unknown Section"

        for doc in comp.findall(".//tei:div[@type='document']", NS):
            doc_id = doc.attrib.get("{http://www.w3.org/XML/1998/namespace}id", "Unknown")
            date_elem = doc.find(".//tei:date", NS)
            if date_elem is not None and date_elem.attrib.get("when"):
                doc_time = date_elem.attrib["when"]
            elif date_elem is not None and date_elem.text:
                doc_time = date_elem.text.strip()
            else:
                doc_time = "Unknown Date"

            places: list[str] = []
            for place in doc.findall(".//tei:placeName", NS):
                text_parts = [place.text] if place.text else []
                text_parts += [ET.tostring(e, encoding="unicode", method="text") for e in list(place)]
                combined = " ".join(filter(None, [t.strip() for t in text_parts if t]))
                if combined:
                    places.append(combined)
            doc_place = ", ".join(places) if places else "No Place"

            paragraphs = doc.findall(".//tei:p", NS)
            doc_text = "\n".join([p.text.strip() for p in paragraphs if p.text])

            doc_link = f"https://history.state.gov/historicaldocuments/{volume_id}/{doc_id}"

            all_documents.append(
                {
                    "Volume Name": volume_name,
                    "Contents Title": contents_title,
                    "Document Number": doc_id,
                    "Document Time": doc_time,
                    "Document Place": doc_place,
                    "Document Content": doc_text,
                    "Document Link": doc_link,
                    "Source Xml File": file_name,
                }
            )
    return all_documents


def run(
    output_path: Path,
    max_files: int | None,
    max_docs_total: int | None,
    sleep_sec: float,
    files_override: list[str] | None,
) -> int:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "frus-xml-to-csv/1.0 (research; RA_data/Cursor)",
            "Accept": "application/vnd.github+json",
        }
    )

    if files_override:
        xml_names = files_override
    else:
        xml_names = list_volume_xmls(session, max_files)

    if not xml_names:
        print("No XML files found.", file=sys.stderr)
        return 1

    rows: list[dict] = []
    for name in tqdm(xml_names, desc="XML volumes"):
        if max_docs_total is not None and len(rows) >= max_docs_total:
            break
        url = RAW_BASE + name
        try:
            r = session.get(url, timeout=120)
            if r.status_code != 200:
                print(f"Skip {name}: HTTP {r.status_code}", file=sys.stderr)
                continue
            docs = parse_volume_xml(r.content, name)
            if not docs:
                print(f"No document rows parsed from {name} (empty or unsupported TEI body).", file=sys.stderr)
            if max_docs_total is not None:
                remain = max_docs_total - len(rows)
                if remain <= 0:
                    break
                docs = docs[:remain]
            rows.extend(docs)
        except Exception as e:
            print(f"Error {name}: {e}", file=sys.stderr)
        time.sleep(sleep_sec)

    df = pd.DataFrame(rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Wrote {len(df)} rows to {output_path}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Convert HistoryAtState/frus TEI XML volumes to CSV.")
    p.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "result" / "frus_xml_documents.csv",
        help="Output CSV path",
    )
    p.add_argument("--max-files", type=int, default=None, help="Process at most N volume XML files (after sort).")
    p.add_argument("--max-docs", type=int, default=None, help="Stop after N total document rows (across files).")
    p.add_argument("--sleep", type=float, default=0.15, help="Seconds between volume downloads.")
    p.add_argument(
        "--files",
        nargs="+",
        default=None,
        help="Explicit XML filenames only (e.g. frus1861.xml), skip GitHub tree listing.",
    )
    args = p.parse_args()
    return run(
        args.output,
        args.max_files,
        args.max_docs,
        args.sleep,
        args.files,
    )


if __name__ == "__main__":
    raise SystemExit(main())
