import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re, os
from tqdm import tqdm
from datetime import datetime

# Base URL
admin_names = ["eisenhower", "kennedy", "johnson", "nixon-ford"]
'''["eisenhower", "kennedy", "johnson", "nixon-ford"]'''
base_url = "https://history.state.gov/historicaldocuments/"
documents = []

def get_administration_name(admin_name):
    response = requests.get(base_url + admin_name)
    soup = BeautifulSoup(response.content, 'html.parser')
    admin_title_tag = soup.find('h1', {'class': 'titleStmt1', 'data-template': 'frus:administration-name'})
    if admin_title_tag:
        admin_title = admin_title_tag.text.strip()
        admin_name_cleaned = re.sub(r'\(.*?\)', '', admin_title).strip()  # Remove year range in parenthesis and clean
        return admin_name_cleaned
    else:
        return "Unknown Administration"

def scrape_administration(admin_name):
    ret = []
    response = requests.get(base_url +  admin_name)
    soup = BeautifulSoup(response.content, 'html.parser')

    c = soup.find_all('a', {'data-template': 'app:parse-params'})
    for i in range(len(c)):
        if len(re.findall("Volume", c[i].text.split(', ')[-1])):
            ret.append((c[i]['href'], c[i].text.split(', ')[-1].strip("\n").strip(" "), c[i].text.split(', ')[0].strip("\n").strip(" ")))
        elif len(c[i].text.split(', ')) > 1 and len(re.findall("Volume", c[i].text.split(', ')[-2])):
            ret.append((c[i]['href'], c[i].text.split(', ')[-2].strip("\n").strip(" "), c[i].text.split(', ')[0].strip("\n").strip(" ")+"("+c[i].text.split(', ')[-1].strip("\n").strip(" ")+")"))
        else:
            ret.append((c[i]['href'], "No volume info", c[i].text.split(', ')[0].strip("\n").strip(" ")))

    return ret

def scrape_volume(volume_name):
    ret = []
    response = requests.get(base_url + volume_name)
    soup = BeautifulSoup(response.content, 'html.parser')

    for i in range(1, 1000000):
        c = soup.find('a', id="toc-comp%d"%(i))
        if c is None:
            break
        if c.next_sibling is None:
            continue
        docs_id = re.findall("\d+", c.next_sibling)
        if len(docs_id) == 2:
            ret.append((c.text, list(map(int, docs_id))))

    return ret


def scrape_document(url, doc_num, content_title, administration, year, volume):
    # Get the page content
    response = requests.get(base_url + url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the document title
    title_tag = soup.find(['h3', 'h4'], class_='tei-head7')  # Title is in <h3> or <h4>
    title = title_tag.get_text(strip=True) if title_tag else "No Title"

   # Extract the document time (within <span> with class "tei-date")
    time_tag = soup.find('span', class_='tei-date')
    document_time = time_tag.get_text(strip=True) if time_tag else "No Time"
    document_time = re.sub(r"\s+", " ", document_time).strip("\n").strip().replace("—", " ").replace("p.m.", "pm").replace("a.m.", "am")
    if document_time != "No Time":
      try:
        if len(document_time.split(" ")) == 3:
            document_time = str(datetime.strptime(document_time, "%B %d, %Y")).split(" ")[0]
            document_timeHMS = document_time
        else:
            document_time = str(datetime.strptime(document_time, "%B %d, %Y %I %p"))
            document_timeHMS = document_time.split(" ")[0]
      except ValueError:
          document_time = "Invalid Time Format"
          document_timeHMS = "Invalid Time Format"
    else:
        document_timeHMS = document_time

    # Extract the document place (within <span> with class "tei-hi3")
    place_tag = soup.find('span', class_='tei-hi3')
    document_place = place_tag.get_text(strip=True) if place_tag else "No Place"
    
    # Extract the document content (within <div> with id "content-inner" or "content-container")
    content_tag = soup.find('div', id='content-inner')
    tei_p3_paragraphs = content_tag.find_all('p', class_='tei-p3') if content_tag else []
    def remove_footnote_and_pb1_text(element):
        for footnote in element.find_all(rel="footnote"):
            footnote.decompose()
        for pb1 in element.find_all(class_='tei-pb1'):
            pb1.decompose()
        return element.get_text(" ", strip=True)
    content = " ".join(
        [remove_footnote_and_pb1_text(p) for p in tei_p3_paragraphs]
    ).replace("\n", " ") if tei_p3_paragraphs else "No Content"
    content = re.sub(r'\s+', ' ', content).strip()

    #Year column
    year = document_time.split("-")[0] if document_time != "Invalid Time Format" else "Unknown Year"

    # Add document to list with the corresponding content title
    return {
        "Administration": get_administration_name(adm),
        "Year": year,
        "Volume": volume,
        "Contents Title": content_title,
        "Document Title": re.sub(r"\s+", " ", title).strip("\n").strip(),
        "Document Number": f"Document {doc_num}",
        "Document Time": re.sub(r"\s+", " ", document_time).strip("\n").strip(),
        "Document Place":  re.sub(r"\s+", " ", document_place).strip("\n").strip(),
        "Document Content": content,
        "Document Link": base_url + url
    }

for adm in admin_names:
    administration = get_administration_name(adm)
    volumes = scrape_administration(adm)
    for href, volume, name_doc in volumes:
        volume = volume.replace("/", ",")
        name_doc = re.sub(r"\s+", " ", name_doc).strip("\n").strip()
        if os.path.exists("./result/%s_%s_%s.csv"%(adm, name_doc, volume)):
            continue
        data = []
        documents = scrape_volume(href)
        year_match = re.search(r'(\d{4})', volume)  # Extract year from volume name (e.g., "Volume I, 1929")
        year = year_match.group(1) if year_match else "Unknown"
        for highest_content_name, idx_doc in documents:
            highest_content_name = re.sub(r"\s+", " ", highest_content_name).strip("\n").strip()
            print(f"Scraping '{highest_content_name}' content in '{name_doc}, {volume}' of '{adm}'")
            start_doc, end_doc = idx_doc
            for doc_num in tqdm(range(start_doc, end_doc + 1)):
                url = f"%s/d{doc_num}" % (href)
                data.append(scrape_document(url, doc_num, highest_content_name, adm, year, volume))

        df = pd.DataFrame(data)
        if not len(df):
            print("Error in crawling %s_%s_%s"%(adm, name_doc, volume))
            continue
        df['Year'] = df['Year'].replace("Unknown Year", None)  # Replace "Unknown" with NaN for ffill
        df['Year'] = df['Year'].ffill()  # Forward-fill the missing years
        df.to_csv("./result/%s_%s_%s.csv"%(adm, name_doc, volume), index=False)
