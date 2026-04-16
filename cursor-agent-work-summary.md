# Cursor 활용 결과 보고서

작성자: 조은비  |   기간: 2026.04.06 ~ 2026.04.16

## 0. 개요

본 보고서는 코딩 에이전트(Cursor AI)를 활용하여 입사 전 수행한 개인 과제 및 프로젝트를 정리·구조화하고,  
동일한 과제를 에이전트 기반으로 재구현하는 과정을 통해 기존 개발 방식과의 차이를 분석한 결과를 정리했습니다.

개발 속도, 코드 구조화 및 관리, 그리고 재사용성 측면에서의 개선 가능성을 직접 체감하며 앞으로의 업무에서 Cursor 활용과 적용 가능성을 확인했습니다.

수행 내용:

- 기존 프로젝트 구조 정리 및 GitHub 체계화
- 코딩 에이전트 기반 과제 재구현
- 기존 방식과의 전/후 비교
- 향후 활용 가능성 도출

---

## 1. 전체 방향

입사 전 수행했던 개인 과제 프로젝트를 하나의 GitHub [repository](https://github.com/eunbijoel/coursework/tree/main)로 정리했습니다.  
이후 학부(알고리즘) 및 대학원(RA) 수행 과제를 중심으로 구조화하고, 동일한 목표에 대해 Cursor AI를 활용한 재구현 결과를 비교했습니다.

---

## 2. [알고리즘](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/README.md)

**주제별 과제 요약**과, Cursor로 **재구현 된 부분 정리** 표


| 주제                                                                                                                             | 설명                                     | Cursor 구현                                                    |
| ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- | ------------------------------------------------------------ |
| [Genetic algorithm](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/Genetic%20Algorithm/README.md)      | 유전 알고리즘 과제, 연속 함수 최적화·TSP 등 개요와 실행 방법. | README 정리. **에이전트로 알고리즘 구조화 및 문서화.**                         |
| [Graph algorithm (Dijkstra)](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/README-Graph-Algorithm.md) | 가중 그래프·최단 경로·기상 구역 시나리오 요약.            | **단일 파이프라인**으로 재구성 및 결과 시각화. 항공 경로 최단 경로 시각화 항공 경로 최단 경로 시각화 |
| [Divide & Conquer algorithm](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/DAC_cursor%20refined.md)   | 분할 정복으로 Shell 연결하는 과제 구현.              | **코드 복잡도 및 시간 단축.** **알고리즘 구조화.** DAC 볼록 껍질 파이프라인 과정 시각화     |


---

## 3. [RA — 데이터 수집·전처리](https://github.com/eunbijoel/coursework/tree/main/grad/RA_data)

연구조교(RA) 기간 **데이터 수집·정리** 과업을 [Previous](https://github.com/eunbijoel/coursework/tree/main/grad/RA_data/Past)(원본)와 [Cursor](https://github.com/eunbijoel/coursework/tree/main/grad/RA_data/Cursor)(에이전트로 재작성한 CLI 도구)로 나누어 정리


| 주제                                                                                                                       | 설명                                                    | Cursor 구현                                                                            |
| ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [FRUS · 웹 (HTML)](https://github.com/eunbijoel/coursework/blob/main/grad/RA_data/Cursor/frus_crawl.py)                   | 미국 국무부 공개 외교사료 FRUS를 **행정부별 문서 수집**                   | **하나의 파이프라인으로 코드 간편화**                                                               |
| [FRUS · XML → CSV](https://github.com/eunbijoel/coursework/blob/main/grad/RA_data/Cursor/frus_xml_to_csv.py)             | TEI를 받아 CSV 단위로 표준화. 웹 전체 크롤 대신 **Git 원문** 사용.       | GitHub **tree API**로 볼륨 목록, raw XML fetch + TEI 파싱, `--max-files`·`--max-docs` 과정 추가 |
| [Author affiliation](https://github.com/eunbijoel/coursework/blob/main/grad/RA_data/Cursor/author_affiliation_enrich.py) | 학술 DB(CSV)의 **저자**에 대해 소속·기관 등 메타 데이터 추가.             | **OpenAlex API**로 저자 검색·소속 후보 (Google Scholar HTML 크롤링은 ToS·안정성 이슈로 API 사용).         |
| [News](https://github.com/eunbijoel/coursework/blob/main/grad/RA_data/Cursor/news_unibook_metadata.py)                   | 통일부 유니북 **URL**에서 서지 6필드(주기사명·서명·권호·발행처·발행일자·페이지) 추출. | 동일 CSS selector를 **한 번에 CLI**로 실행·1행 CSV 저장. 노트북·드라이브 경로 의존 감소.                      |


---

## 4. Cursor 활용으로 배운 점 및 방향성

### 4.1. 개발 프로세스 변화

- 기존: 문제 정의 → 코드 작성 → 디버깅 → 개선 (순차적)
- Cursor 활용: 문제 정의 → 코드 생성 → 결과 확인 → 수정 요청 → 반복 (반복적/대화형)

→ 빠른 시행착오 및 다양한 접근 방식 비교 가능

### 4.2. 코드 이해 및 구조 설계

- 단순 코드 생성이 아니라,
  - 함수 단위 설명
  - 파일 간 구조
  - 데이터 흐름 등을 지속적으로 요청하면서 **코드 구조를 읽고 설계하는 경험**
- 특특히 “왜 이 구조인지”, “어디가 병목인지”를 중심으로 분석하면서 시스템 수준의 이해도 향상

### 4.3. 반복 작업 자동화

- 데이터 전처리 및 API 연동 자동화
- 포맷 변환 및 데이터 수집 효율화
- 다양한 방식의 빠른 실험 가능

### 4.4. 향후 활용 가능성

- Cursor와 같은 코딩 에이전트는 단순 도구를 넘어 **프로세스 자체를 변화시키는 툴**
- 특히 데이터 기반 연구 및 산업 AI 환경에서:
  - 빠른 프로토타이핑
  - 데이터 처리 자동화
  - 실험 기반 반복 개선 구조

---

## 5. 추가 업무

- [open-claw.md](https://github.com/eunbijoel/coursework/blob/main/OPENCLAW_GETTING_STARTED_KO.md) 초안 작성
- EMG 소프트로봇 동향보고서 (04.09~10)
- EDC PPT 수정
- SQL to Python (FewShot-> RAG 학습)
- Catena_X 구현 방안 탐색

