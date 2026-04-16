# Cursor 활용 결과 보고서

작성자: 조은비  |   기간: 2026.04.06 ~2026.04.15

본 문서는 코딩 에이전트(Cursor AI)를 활용해 기존 과제 및 프로젝트를 재구성하고, 동일한 과제를 재수행하며 **개발 방식의 변화 및 효율성**을 검증한 내용을 정리한 보고서입니다:

- 기존 프로젝트 구조 정리 및 GitHub 체계화
- 코딩 에이전트 기반 과제 재구현
- 전/후 비교
- 추후 활용 방안

---

## 1. 전체 방향

1. **입사 전에 수행한 개인 과제** 프로젝트를 하나의 repository로 정리 후
2. **학부** 및 석사과정으로 나누어 상세 페이지를 구조화했고, 동일 목표에 대해 **에이전트로** 작성한 결과 **비교**

---

## 2. [알고리즘 (학부)](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/README.md)

### 2.1 폴더 및 문서 구조화


| 주제                                                                                                                        | 설명                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| [Genetic algorithm](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/Genetic%20Algorithm/README.md) | 유전 알고리즘 과제(Task1·2), 연속 함수 최적화·TSP 등 개요와 실행 방법 정리. Task2 상세는 동일 폴더 `README-Task2.md` 참고. |
| [Graph algorithm](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/README-Graph-Algorithm.md)       | 가중 그래프·최단 경로·기상 구역 시나리오 요약. 예전 Colab 노트북은 `flight_path_optimization`의 OG 노트북으로 이관됨.      |
| [Divide and conquer](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/README-Divide-and-Conquer.md) | 분할 정복 볼록 껍질 등 노트북·개념 요약.                                                                 |


### 2.2 동일 목표 재구현 — 항공 경로 최단 경로 (flight path)


| 구분                          | 링크                                                                                                                                                                               |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **에이전트로 작성한 구현**            | `[flight_path_optimization.py](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/flight_path_optimization/flight_path_optimization.py)`                     |
| 설명·과제 질문 대응 MD              | `[flight_path_optimization_explained.md](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/flight_path_optimization/flight_path_optimization_explained.md)` |
| 결과 그림 (스크립트 실행 시 생성)        | `[flight_path_result.png](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/flight_path_optimization/flight_path_result.png)`                               |
| **이전 버전(같은 유형, 다른 그래프·방식)** | `[Graph%20Algorithm_OG.ipynb](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/flight_path_optimization/Graph%20Algorithm_OG.ipynb)`                       |


### 2.3 Divide & Conquer — 볼록 껍질 (DAC)


| 구분            | 링크                                                                                                                                                          |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 단독 스크립트       | `[dac_convex_hull_standalone.py](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/dac_convex_hull_standalone.py)`                     |
| 설명 MD (mixed) | `[dac_convex_hull_standalone_explained.md](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/dac_convex_hull_standalone_explained.md)` |
| 노트북 원안        | `[Divide%20and%20Conquer.ipynb](https://github.com/eunbijoel/coursework/blob/main/undergrad/algorithms/Divide%20and%20Conquer.ipynb)`                       |


---

## 3. RA — 데이터 수집·전처리

### 3.1 FRUS / 뉴스·스칼라 (RA)


| 구분           | 링크                                                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| 폴더·계획 README | `[grad/ra-scholar-frus-news/README.md](https://github.com/eunbijoel/coursework/blob/main/grad/ra-scholar-frus-news/README.md)` |


### 3.3 “같은 objective” 재작성·비교

- **원칙:** 로컬·비공개 스크립트는 에이전트로 초안·리팩터링 후, **민감 정보 제거**한 버전만 Git에 올리는 식으로 정리 가능.
- flight path처럼 **구버전 노트북 vs 신규 `.py`** 를 나란히 두고 문서에 **역할 차이**만 적어 두면 보고서에 재사용하기 좋음.

---

## 4. Cursor 활용으로 배운 점 및 방향성

### 4.1. 개발 프로세스의 구조적 변화

- 기존 방식: 문제 정의 → 코드 작성 → 디버깅 → 개선 (순차적)
- Cursor 활용: 문제 정의 → 코드 생성 → 결과 확인 → 수정 요청 → 반복 (반복적/대화형)
  - 빠른 시행착오 가능
  - 다양한 접근 방식 비교 용이
  - 코드 품질 개선 속도 증가

### 4.2. 코드 이해 및 구조 설계 역량

- 단순 코드 생성이 아니라,
  - 함수 단위 설명
  - 파일 간 구조
  - 데이터 흐름 등을 지속적으로 요청하면서 **코드 구조를 읽고 설계하는 경험**
- 특히,
  - “왜 이 구조인가?”
  - “어떤 부분이 병목인가?” 를 중심으로 질문하면서 **시스템 레벨 이해도 증가**

### 4.3. 반복 작업 자동화 및 최저화

- 데이터 전처리, API 연결, 포맷 변환 등 반복 작업을 자동화 가능
- 동일한 작업을 다양한 방식으로 빠르게 실험 하는 과정을 통해 시간 단축 및 더 다양한 케이스 검증 가능

### 4.4. 앞으로의 확장 가능성

- Cursor와 같은 코딩 에이전트는 단순 도구가 아니라 **프로세스 자체를 변화시키는 툴**
- 특히 데이터 기반 연구 및 산업 AI 환경에서:
  - 빠른 프로토타이핑
  - 자동화된 데이터 처리
  - 실험 기반 개선 구조를 가능하게 함

---

## 5. 추가: Open Claw 활용법

-  `[docs/open-claw.md](https://github.com/eunbijoel/coursework/blob/main/docs/open-claw.md)` 같은 파일을 만들어 링크를 이 자리에 넣으면 됨.  
- **(초안)** 제목만 두고 본인이 채워 넣을 수 있게 비워 둠.

