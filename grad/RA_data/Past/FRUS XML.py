# ==========================================
#   FRUS (Foreign Relations of the U.S.) 전체 데이터 크롤링 및 정제 파이프라인
#   - 공식 GitHub XML 이용 (1861~1980)
#   - 웹사이트 기반 누락값 보완
#   - 문서별 시간, 장소, 본문, 소속 행정부 자동 판별
# ==========================================

import requests, re, time
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET
import pandas as pd

# ---------- [1] GitHub XML 기반 메인 파서 ----------
ns = {'tei': 'http://www.tei-c.org/ns/1.0'}  # XML 네임스페이스
all_documents = []

for file_name in file_list:  # e.g., ["frus1861.xml", ..., "frus1977-80v30.xml"]
    url = f"https://raw.githubusercontent.com/HistoryAtState/frus/master/volumes/{file_name}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch: {file_name}")
            continue

        root = ET.fromstring(response.content)
        tei_header = root.find("tei:teiHeader", ns)
        volume_name = "Unknown Volume"
        if tei_header is not None:
            title_stmt = tei_header.find("tei:fileDesc/tei:titleStmt", ns)
            if title_stmt is not None:
                for title in title_stmt.findall("tei:title", ns):
                    if title.attrib.get("type") == "series" and title.text:
                        volume_name = title.text.strip()

        volume_id = root.attrib.get("{http://www.w3.org/XML/1998/namespace}id", file_name.replace(".xml", ""))
        body = root.find("tei:text/tei:body", ns)
        if body is None:
            continue

        for comp in body.findall(".//tei:div[@type='compilation']", ns):
            contents_title_elem = comp.find("tei:head", ns)
            contents_title = contents_title_elem.text.strip() if contents_title_elem is not None else "Unknown Section"

            for doc in comp.findall(".//tei:div[@type='document']", ns):
                doc_id = doc.attrib.get("{http://www.w3.org/XML/1998/namespace}id", "Unknown")
                date_elem = doc.find(".//tei:date", ns)
                doc_time = date_elem.attrib.get("when") if date_elem is not None and 'when' in date_elem.attrib else (
                    date_elem.text.strip() if date_elem is not None and date_elem.text else "Unknown Date")

                places = []
                for place in doc.findall(".//tei:placeName", ns):
                    text_parts = [place.text] if place.text else []
                    text_parts += [ET.tostring(e, encoding='unicode', method='text') for e in list(place)]
                    combined = " ".join(filter(None, [t.strip() for t in text_parts]))
                    if combined:
                        places.append(combined)
                doc_place = ", ".join(places) if places else "No Place"

                paragraphs = doc.findall(".//tei:p", ns)
                doc_text = "\n".join([p.text.strip() for p in paragraphs if p.text])

                doc_link = f"https://history.state.gov/historicaldocuments/{volume_id}/{doc_id}"

                all_documents.append({
                    "Volume Name": volume_name,
                    "Contents Title": contents_title,
                    "Document Number": doc_id,
                    "Document Time": doc_time,
                    "Document Place": doc_place,
                    "Document Content": doc_text,
                    "Document Link": doc_link
                })
    except Exception as e:
        print(f"❌ Error in {file_name}: {e}")
        continue

df = pd.DataFrame(all_documents)

# ---------- [2] 누락된 문서 크롤링 보완 (웹페이지 기반) ----------
base_url = "https://history.state.gov"

def scrape_document(url, doc_num, administration, volume):
    response = requests.get(base_url + url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.content, 'html.parser')

    title_tag = soup.find(['h3', 'h4'], class_='tei-head7')
    title = title_tag.get_text(strip=True) if title_tag else "No Title"

    time_tag = soup.find('span', class_='tei-date')
    document_time = time_tag.get_text(strip=True) if time_tag else "No Time"
    document_time = re.sub(r"\s+", " ", document_time).replace("—", "-").replace("p.m.", "pm").replace("a.m.", "am")
    try:
        document_time = datetime.strptime(document_time, "%B %d, %Y").strftime("%Y-%m-%d")
    except:
        document_time = "Invalid Time Format"

    place_tag = soup.find('span', class_='tei-hi3')
    document_place = place_tag.get_text(strip=True) if place_tag else "No Place"

    content_tag = soup.find('div', id='content-inner')
    tei_p3_paragraphs = content_tag.find_all('p', class_='tei-p3') if content_tag else []

    def clean_text(p):
        for footnote in p.find_all(rel="footnote"): footnote.decompose()
        for pb1 in p.find_all(class_='tei-pb1'): pb1.decompose()
        return p.get_text(" ", strip=True)

    content = " ".join([clean_text(p) for p in tei_p3_paragraphs]) if tei_p3_paragraphs else "No Content"
    content = re.sub(r'\s+', ' ', content).strip()

    return {
        "Administration": administration,
        "Volume Name": volume,
        "Contents Title": title,
        "Document Number": f"d{doc_num}",
        "Document Time": document_time,
        "Document Place": document_place,
        "Document Content": content,
        "Document Link": base_url + url
    }

# 예시 실행 코드
administration = "John F. Kennedy"
volume = "Foreign Relations of the United States, 1961–1963, Volume VI, Kennedy-Khrushchev Exchanges"
base_path = "/historicaldocuments/frus1961-63v06"
documents = []
for i in range(1, 121):
    print(f"Scraping doc {i}...")
    result = scrape_document(f"{base_path}/d{i}", i, administration, volume)
    if result:
        documents.append(result)
df_web = pd.DataFrame(documents)

# ---------- [3] Document Time을 기반으로 행정부 할당 ----------
presidents = [
    ("Abraham Lincoln", "1861-03-04", "1865-04-15"),
    ("Andrew Johnson", "1865-04-15", "1869-03-04"),
    ...,
    ("Gerald Ford", "1974-08-09", "1977-01-20"),
    ("Jimmy Carter", "1977-01-20", "1981-01-20")
]
term_df = pd.DataFrame(presidents, columns=["Administration", "Start", "End"])
term_df["Start"] = pd.to_datetime(term_df["Start"])
term_df["End"] = pd.to_datetime(term_df["End"])

def get_administration(doc_date):
    for _, row in term_df.iterrows():
        if pd.notnull(doc_date) and row["Start"] <= doc_date <= row["End"]:
            return row["Administration"]
    return "Unknown"

df["Document Time Parsed"] = pd.to_datetime(df["Document Time"], errors='coerce')
df["Administration"] = df["Document Time Parsed"].apply(get_administration)
df.drop(columns=["Document Time Parsed"], inplace=True)
