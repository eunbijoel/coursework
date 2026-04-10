# 알고리즘 과제 (Undergraduate Algorithms)

이 폴더는 **알고리즘** 강의 정리 파일입니다.
---

## 목차

| # | 주제 | 이동 |
|---|------|------|
| 1 | **Genetic algorithm** | [이동](Genetic%20Algorithm) |
| 2 | **Graph algorithm** (Dijkstra 등) | [이동](#2-graph-algorithm-그래프--다익스트라) |
| 3 | **Divide and conquer** | [이동](#3-divide-and-conquer-분할-정복) |


---

## 프로젝트 구조 (요약)

```text
algorithms/
├── README.md                 ← 이 파일 (전체 안내)
├── Divide and Conquer.ipynb  분할 정복 볼록 껍질
├── Graph Algorithm.ipynb     가중 그래프 + Dijkstra + 시나리오 시각화
└── Genetic Algorithm/
    ├── README.md             Task 1 (연속 함수 GA)
    ├── Task1.ipynb
    └── Task 2.ipynb
```

---

## 2. Graph algorithm (그래프 · 다익스트라)

### 무엇을 하나요?

- 공항(또는 지점) **좌표 데이터**를 읽고, 지점 간 **가중 무방향 그래프**를 만듭니다.
- 변의 가중치는 위·경도로부터 **`haversine` 패키지**로 구한 **지표상 거리(예: 미터)** 에 가깝게 둡니다(구면 대원 거리).
- **`Dijkstra`** 로 최단 경로(또는 목표 도착 시 조기 종료에 가까운 우선순위 큐 탐색)를 구현하고, **부모 포인터**로 경로를 복원합니다.
- **“나쁜 기상” 영역**을 다각형 등으로 두면, 그 구간을 통과하는 간선 비용을 키우거나 우회하도록 **`dijkstra(G, start, goal, bad_regions)`** 형태로 실험합니다.
- `represent(...)` 로 **지도상 경로·금지 구역**을 함께 그립니다.

### 코드에서 자주 나오는 이름

| 이름 | 역할 |
|------|------|
| 그래프 클래스 | 정점·간선·가중치 추가, 이웃 조회 |
| `dijkstra` | 시작·목표, `bad_regions` 옵션 |
| `make_path` | 부모 배열로부터 경로 리스트 |
| `calculate_path_distance` | 경로 총 거리 |
| `represent` | 데이터프레임 + 그래프 + 경로 + bad 영역 시각화 |

## 3. Divide and conquer (분할 정복)

### 무엇을 하나요?

- **평면 위 점들**의 **볼록 껍질(convex hull)** 을 **분할 정복**으로 구합니다.
- 점 생성 조건: **서로 다른 x**, **서로 다른 y**, **일직선상 세 점 없음(비공선)** 등으로 과제 조건을 맞춥니다.

### 흐름 (노트북 구조)

1. **Divide:** x 좌표로 정렬한 뒤 **반평면으로 분할** (`separate_half_planes` 등).
2. **Conquer:** 각 쪽에서 **작은 볼록 껍질** 생성 (`generate_convex_hull`, 방향 판별 등).
3. **Merge:** 두 볼록 껍질을 **상·하 접선** 아이디어로 합치는 단계 (`upper_lower` 등).
4. 결과를 **matplotlib**으로 표시.
