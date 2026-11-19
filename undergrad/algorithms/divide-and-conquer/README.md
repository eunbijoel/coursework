# Divide and Conquer — `Divide and Conquer.ipynb` 상세 설명

> 평면 위 **무작위 점**들이 주어졌을 때 **볼록 껍질(convex hull)** 을 구하는 과제입니다.  
> **분할 정복(Divide and Conquer)** 으로 점 집합을 **왼쪽/오른쪽**으로 나눈 뒤, 각각에 Shell을 만들고, **두** Shell**을 이어 붙이는(merge)** 단계까지 노트북에 구현되어 있습니다.

---

## 1. 분할 정복

### 정의

- **볼록 껍질**은 주어진 점들을 모두 포함하는 **가장 작은 볼록 다각형**을 이루는 꼭짓점(및 순서)입니다.
- 응용으로는 **충돌 검사**, **범위 요약**, **기하 알고리즘의 전처리** 등에서 자주 쓰입니다.

### 왜 naive 한 방법만으로는 부담이 될 수 있나?

- 점이 n개일 때 **모든 부분집합·모든 순서**를 시도하는 방식은 지나치게 느립니다.
- **분할 정복**은 “전체를 한 번에” 풀지 않고:
  1. **Divide:** 점을 두 그룹으로 나누고
  2. **Conquer:** 각 그룹의 볼록 껍질을 구한 뒤
  3. **Merge:** 두 볼록 껍질을 **하나의 볼록 껍질**로 합칩니다.

이렇게 하면 **문제 크기가 반으로 줄어드는 구조**를 만들 수 있고, 핵심 난이도는 **두 볼록 다각형을 올바르게 합치는 merge**에 있습니다.

---

## 2. 입력 점 생성: 과제 조건 맞추기

노트북은 `generate_valid_points(num_points)` 로 **정수 좌표** 점을 뽑습니다.


| 조건                       | 이유(과제 관점)                           |
| ------------------------ | ----------------------------------- |
| **서로 다른 x**              | 수직선에 두 점이 겹치는 퇴화 케이스 감소             |
| **서로 다른 y**              | 수평선에 두 점이 겹치는 퇴화 케이스 감소             |
| **세 점이 한 직선 위에 없음(비공선)** | 볼록 껍질 경계에서 “한 변에 여러 점이 겹치는” 모호함을 줄임 |


**공선 판별**은 `is_collinear(p1, p2, points)` 에서  
(y_2-y_1)(x_3-x_2) = (y_3-y_2)(x_2-x_1)  
형태의 **외적(cross product)이 0인지**로 검사합니다(정수 연산).

---

## 3. Divide: 반평면으로 나누기

### `separate_half_planes(points)`

1. 점을 **x 좌표로 정렬**합니다.
2. `mid_index = len // 2` 로 **앞쪽 절반 / 뒤쪽 절반**으로 잘라 **두 개의 half-plane** 으로 둡니다.

이때 “물리적 반평면”이 아니라, **정렬 후 인덱스 기준 왼쪽·오른쪽 묶음**입니다. 시각화에서는 `plot_half_planes` 로 색을 달리해 보여 줍니다.

---

## 4. Conquer: 한쪽 점 집합의 볼록 껍질 — `generate_convex_hull`

### 알고리즘 성격

노트북의 `generate_convex_hull` 은 점을 **lexicographic 정렬**한 뒤, 가장 왼쪽(동률이면 아래) 점에서 출발해, 반복적으로 **“가장 왼쪽으로 도는” 다음 점**을 고르는 **Gift wrapping / Jarvis march** 계열의 **껍질을 따라가는** 방식입니다.

내부 도우미:

- `**get_orientation(origin, p1, p2)`**  
외적에 해당하는 값  
(p_2-o)\times(p_1-o) 부호로, `p2` 가 `p1` 보다 origin 기준 **반시계 방향**에 있으면 양수로 두고 `far_point` 를 갱신합니다.

### 루프 구조(요지)

1. `sorted_points` 에서 **시작점** `start` 를 잡습니다.
2. 현재 점 `point` 에서, 다른 모든 후보 `p2` 에 대해 `get_orientation(point, far_point, p2) > 0` 이면 **더 바깥쪽(반시계)** 으로 도는 점으로 `far_point` 를 바꿉니다.
3. `hull_points` 에 추가하고 `point = far_point` 로 이동합니다.
4. **다시 `start` 로 돌아올 때까지** 반복합니다.

**주의:** 이 함수는 **한쪽 half-plane 안의 점들만** 넣어 쓸 때(노트북의 `hull_half_plane1`, `hull_half_plane2`) **그 부분집합의 볼록 껍질**을 구합니다.

---

## 5. Merge: 두 볼록 껍질 잇기 — `upper_lower` + `merge_half_hulls`

왼쪽 점들의 볼록 껍질 `hull1` 과 오른쪽의 `hull2` 가 있을 때, 전체 볼록 껍질은 **두 다각형을 잇는 “다리(bridge)”** 를 찾아 경계를 이어 붙이는 문제로 바뀝니다.

### `upper_lower(hull1, hull2)`

1. **분리축** `x_separator` 를
  `hull1` 의 **최대 x** 와 `hull2` 의 **최소 x** 의 **중점**으로 둡니다(두 덩어리가 좌·우로 갈라졌다는 가정).
2. `hull1` 의 점과 `hull2` 의 점의 **모든 쌍**에 대해 직선을 그었을 때, 그 직선이 `x_separator` 와 만나는 **y** 를 계산합니다.
3. 교차가 유효한 쌍에 대해, **위쪽/아래쪽** 후보를 모아 정렬한 뒤, **상·하 접선**에 해당하는 극값 쌍 `(upper_bound, lower_bound)` 를 뽑습니다.

이 단계는 교육용으로 **브루트포스에 가깝게** 짜여 있으며, 일반적인 O(n) **two-pointer tangent merge** 보다는 무겁지만, **작은 half-hull** 에서는 동작을 보기 좋습니다.

### `merge_half_hulls(hull1, hull2, upper_bound, lower_bound)`

- `upper_bound` / `lower_bound` 가 각각 **어느 꼭짓점에서 이어지는지**를 `index` 로 찾습니다.
- **한쪽 hull의 경계를 따라** `lower_bound` 까지, 다시 **다른 쪽**을 따라 **닫힌 다각형**이 되도록 점들을 `merged_hull` 리스트에 순서대로 넣습니다(노트북은 `% len(hull)` 로 **순환 인덱스**를 씁니다).

---

## 6. 시각화와 한 가지 주의점

- 반평면·각 half-hull 은 **색이 다른 plot** 으로 확인합니다.
- 마지막 셀에서는 **전체 점 `points`** 에 대해 다시 `generate_convex_hull(points)` 를 호출해 그립니다.  
이는 **전체 집합에 대한 Jarvis-style 껍질**을 그린 것이고, **앞에서 `merge_half_hulls` 로 만든 `merged_hull`** 과는 **같은 결과가 나와야 정상**이지만, 구현·점 배치에 따라 **검증용으로 두 결과를 비교**해 보는 것이 좋습니다.

---

## 7. 복잡도(직관)


| 단계                               | 노트북 구현 기준 직관                                           |
| -------------------------------- | ------------------------------------------------------ |
| 정렬·분할                            | O(n \log n)                                            |
| 각 half 에서 `generate_convex_hull` | 점 수 m에 대해 **Gift wrapping** 은 최악 O(m^2) 에 가깝게 동작할 수 있음 |
| `upper_lower` 의 모든 쌍             | O(                                                     |
| **전체**                           | 교육용·토이 크기(예: 30점)에는 충분                                 |


과제 목적이 **정확한 최적 O(n \log n) merge** 구현이라면, 표준 교과서의 **sorted merge of convex polygons** 를 추가로 공부하면 좋습니다.

---

## 8. 실행 방법

```bash
pip install matplotlib
```

- `random` 만 쓰면 되므로 **별도 데이터 파일은 없습니다.**
- 셀을 **위에서 아래로** 실행하면 됩니다.

---

## 9. 참고 자료 (노트북 Resources)

- [Convex hull in Python (startupnextdoor)](https://startupnextdoor.com/computing-convex-hull-in-python/)  
- [GeeksforGeeks — Convex Hull using Divide and Conquer](https://www.geeksforgeeks.org/convex-hull-using-divide-and-conquer-algorithm/)  
- [Two-finger convex hull merging (blog)](https://jayjingyuliu.wordpress.com/2018/01/24/algorithm-two-finger-convex-hull-merging-algorithm/)

---

## 10. 한 줄 요약

**점을 x 기준으로 반으로 나누고, 각각 볼록 껍질(Gift wrapping 스타일)을 만든 뒤, 좌·우 볼록 다각형을 잇는 상·하 경계를 찾아 한 바퀴로 이어 전체 볼록 껍질을 완성한다.**