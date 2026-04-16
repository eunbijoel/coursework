# RA_data

**석사과정 연구조교(RA)** 로 참여하면서 진행한 **데이터 수집·정리 관련 단기 과제·프로젝트**를 정리해둔 폴더입니다.

- Prof. Thomas Steinberger (BTM, KAIST)
- [Then Lab](https://sites.google.com/view/thenlab) Prof. Donghyun Woo (GHSS, KAIST)

## 폴더 구조


| 폴더                   | 설명                       |
| -------------------- | ------------------------ |
| `[Past/](Past/)`     | RA 당시 OG **파일** 보관       |
| `[Cursor/](Cursor/)` | Cursor로 **개선·재작성**한 스크립트 |


---

## Project index


| 프로젝트                                                      | 내용                                                                                                                                                                         | 주요 코드                                                                                        |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| [FRUS · 웹 크롤링](Cursor/frus_crawl.py)                      | **데이터:** 미국 국무부 공개 외교사료 *Foreign Relations of the United States (FRUS)* — 행정부별로 **볼륨 → 목차(섹션) → 문서 번호 구간**을 따라 문서 단위 수집. 페이지 요청이 많고 HTML 파싱 부담이 커 **FRUS XML** 파이프라인으로 전환. | **Cursor:** `[frus_crawl.py](Cursor/frus_crawl.py)`.                                         |
| [FRUS · XML → CSV](Cursor/frus_xml_to_csv.py)             | **데이터:** [HistoryAtState/frus `volumes/*.xml](https://github.com/HistoryAtState/frus/tree/master/volumes)` TEI를 **CSV로 구조화** (웹 전체 크롤 대신 Git 원문 사용).                       | **Cursor:** `[frus_xml_to_csv.py](Cursor/frus_xml_to_csv.py)` GitHub tree로 볼륨 목록, raw XML 파싱 |
| [Author affiliation](Cursor/author_affiliation_enrich.py) | **데이터:** 논문 표의 **저자**에 대해 **소속·기관** 등 메타 보강 (과거: Scholar 검색 아이디어; Cursor판은 **OpenAlex API** 사용).                                                                           | **Cursor:** `[author_affiliation_enrich.py](Cursor/author_affiliation_enrich.py)`.           |
| [News](Cursor/news_unibook_metadata.py)                   | **데이터:** 유니북 **URL**에서 서지 6필드(주기사명·서명·권호·발행처·발행일자·페이지) **한 행 CSV**.                                                                                                        | **Cursor:** `[news_unibook_metadata.py](Past/News.ipynb)`                                    |


### Cursor 스크립트 실행 예시

```text
pip install -r Cursor/requirements.txt

# FRUS HTML (기존)
py -3 Cursor/frus_crawl.py --max-documents 20

# FRUS GitHub XML → CSV (볼륨 목록은 이름순이라 첫 파일이 비어 있을 수 있음 → 확실히 하려면 --files 지정)
py -3 Cursor/frus_xml_to_csv.py --files frus1861.xml --max-docs 500

# 저자 소속 보강 (OpenAlex; --mailto 본인 이메일로 변경 권장)
py -3 Cursor/author_affiliation_enrich.py --input Cursor/samples/authors_sample.csv --limit-rows 2 --mailto mailto:you@kaist.ac.kr

# 유니북 URL 한 건
py -3 Cursor/news_unibook_metadata.py --url "https://unibook.unikorea.go.kr/material/view?..."
```

---

## Cursor 활용 인사이트

### 1. 데이터 접근 및 수집 속도 향상

- Cursor를 활용함으로써 다양한 데이터 소스(API, 웹, 로그 등)에 대한 접근 및 수집 코드 구현 속도가 크게 향상됨.
- 기존에는 구조 파악만 1주일이 걸리던 작업을 에이전트를 통해 **초기 코드 생성 및 구조 설계를 빠르게 확보**.
- 반복적인 데이터 수집 및 전처리 작업이 자동화되면서 **탐색 중심(exploratory) 데이터 접근**이 가능해짐.

### 2. 아이디어의 즉각적인 구현

- 연구 주제 또는 아이디어가 도출되었을 때, 기존에는 설계 → 구현 → 테스트까지 진입 장벽이 높았으나, Cursor 활용 후 아이디어 단계에서 바로 **데이터프레임·스크립트 구현**이 가능.
- 이를 통해 이론적 가설을 빠르게 검증하고 **실험 기반 의사결정**이 가능해짐.

