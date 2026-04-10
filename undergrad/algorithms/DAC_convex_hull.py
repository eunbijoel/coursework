#!/usr/bin/env python3
"""
Divide-and-Conquer convex hull (교과 과제용 독립 스크립트)

- 알고리즘 라이브러리 미사용 (scipy / shapely 등 없음)
- matplotlib: 시각화만
- random, 수학: 표준 라이브러리
- Merge API: 노트북과 동일하게 upper_lower(hull1,hull2) → merge_half_hulls(...).
  접선 좌표만 orient 브루트포스로 채움 (x_separator 방식은 docstring에 설명).

실행: python dac_convex_hull_standalone.py
"""

from __future__ import annotations

import os
import random
from typing import List, Optional, Set, Tuple

import matplotlib

matplotlib.use(os.environ.get("MPLBACKEND", "Agg"))
import matplotlib.pyplot as plt

Point = Tuple[int, int]


# ---------------------------------------------------------------------------
# 1) 30개 점: x·y 중복 없음, 세 점 공선 없음
# ---------------------------------------------------------------------------
def is_collinear(p1: Point, p2: Point, points: Set[Point]) -> bool:
    x1, y1 = p1
    x2, y2 = p2
    for p3 in points:
        if p3 == p1 or p3 == p2:
            continue
        x3, y3 = p3
        if (y2 - y1) * (x3 - x2) == (y3 - y2) * (x2 - x1):
            return True
    return False


def generate_valid_points(num_points: int, seed: Optional[int] = 42) -> List[Point]:
    if seed is not None:
        random.seed(seed)
    points: Set[Point] = set()
    while len(points) < num_points:
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        point = (x, y)
        valid = True
        for p in points:
            if p[0] == x or p[1] == y or is_collinear(p, point, points):
                valid = False
                break
        if valid:
            points.add(point)
    return list(points)


# ---------------------------------------------------------------------------
# 2) Divide: x 정렬 후 반으로
# ---------------------------------------------------------------------------
def separate_half_planes(points: List[Point]) -> Tuple[List[Point], List[Point]]:
    points_sorted = sorted(points, key=lambda p: p[0])
    mid = len(points_sorted) // 2
    return points_sorted[:mid], points_sorted[mid:]


# ---------------------------------------------------------------------------
# 3) Conquer: Gift wrapping (노트북과 동일 로직, 튜플은 == 로 비교)
# ---------------------------------------------------------------------------
def generate_convex_hull(points: List[Point]) -> List[Point]:
    """노트북과 동일한 Gift-wrapping (객체 동일성 `is` 사용)."""

    def get_orientation(origin: Point, p1: Point, p2: Point) -> int:
        return ((p2[0] - origin[0]) * (p1[1] - origin[1])) - (
            (p1[0] - origin[0]) * (p2[1] - origin[1])
        )

    sorted_points = sorted(points, key=lambda p: (p[0], p[1]))

    start = sorted_points[0]
    min_x = start[0]
    for p in sorted_points[1:]:
        if p[0] < min_x:
            min_x = p[0]
            start = p

    point = start
    hull_points: List[Point] = [start]

    far_point: Optional[Point] = None
    while far_point is not start:
        p1 = None
        for p in sorted_points:
            if p is point:
                continue
            p1 = p
            break

        far_point = p1
        assert far_point is not None

        for p2 in sorted_points:
            if p2 is point or p2 is p1:
                continue
            direction = get_orientation(point, far_point, p2)
            if direction > 0:
                far_point = p2

        hull_points.append(far_point)
        point = far_point

    return hull_points


# ---------------------------------------------------------------------------
# 4) Merge: 공통 접선(upper / lower tangent) + 두 볼록 다각형 이어 붙이기
# ---------------------------------------------------------------------------
def orient(a: Point, b: Point, c: Point) -> int:
    """>0 이면 c가 벡터 a→b 기준 반시계(왼쪽). y축 위로 갈수록 큰 좌표."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def hull_to_ccw_ring(hull_raw: List[Point]) -> List[Point]:
    """Gift wrapping 결과를 중복 없이 반시계(CCW) 순서의 닫힌 링으로."""
    if len(hull_raw) < 2:
        return hull_raw[:]
    h = hull_raw[:]
    if h[0] == h[-1]:
        h = h[:-1]
    if len(h) < 3:
        return h
    n = len(h)
    s = 0
    for i in range(n):
        s += h[i][0] * h[(i + 1) % n][1] - h[(i + 1) % n][0] * h[i][1]
    if s < 0:
        h = h[::-1]
    return h


def walk_arc(
    hull: List[Point], start_i: int, end_i: int, forward: bool
) -> List[Point]:
    """hull[start_i]에서 hull[end_i]까지, forward면 인덱스 증가 방향으로 한 바퀴 안쪽 호."""
    n = len(hull)
    out: List[Point] = []
    i = start_i
    for _ in range(n + 2):
        out.append(hull[i])
        if i == end_i:
            break
        if forward:
            i = (i + 1) % n
        else:
            i = (i - 1 + n) % n
    else:
        raise RuntimeError("walk_arc: could not reach end")
    return out


def pick_outer_arc_between(
    hull: List[Point], i_a: int, i_b: int, *, is_left_polygon: bool
) -> List[Point]:
    """
    두 꼭짓점 사이 호가 두 갈래일 때, L∪R 전체 볼록 껍질의 **바깥**에 오는 호만 고른다.

    - **왼쪽 half (L)**: 바깥은 **서쪽** 가장자리 → x가 더 작은 쪽 호 (min x, Σx 최소)
    - **오른쪽 half (R)**: 바깥은 **동쪽** 가장자리 → x가 더 큰 쪽 호 (max x, Σx 최대)

    직전에 둘 다 min x만 쓰면 R에서 안쪽(서쪽) 호가 골라져 오른쪽이 꺾인다.
    """
    fwd = walk_arc(hull, i_a, i_b, True)
    bwd = walk_arc(hull, i_a, i_b, False)

    def west_chain_key(arc: List[Point]) -> Tuple[int, int]:
        return (min(p[0] for p in arc), sum(p[0] for p in arc))

    def east_chain_key(arc: List[Point]) -> Tuple[int, int]:
        return (max(p[0] for p in arc), sum(p[0] for p in arc))

    if is_left_polygon:
        return fwd if west_chain_key(fwd) <= west_chain_key(bwd) else bwd
    return fwd if east_chain_key(fwd) >= east_chain_key(bwd) else bwd


def upper_lower(hull1: List[Point], hull2: List[Point]) -> Tuple[Tuple[Point, Point], Tuple[Point, Point]]:
    """
    노트북과 같은 반환 형식:
    - upper_bound = (hull1 위 접점, hull2 위 접점)
    - lower_bound = (hull2 아래 접점, hull1 아래 접점)  ← merge_half_hulls 가 lower_bound[0]을 hull2, [1]을 hull1로 씀

    노트북 원안은 x_separator 와 모든 쌍의 직선이 x_separator 에 만나는지로 후보를 모은 뒤
    y 로 정렬해 끝점을 고르는 방식인데, 공통 접선이 아닐 수 있어 같은 형식으로
    '진짜' 상·하 접선만 브루트포스로 고른다.
    """
    p_up, q_up = find_upper_tangent_bruteforce(hull1, hull2)
    p_lo, q_lo = find_lower_tangent_bruteforce(hull1, hull2)
    upper_bound = (p_up, q_up)
    lower_bound = (q_lo, p_lo)
    return upper_bound, lower_bound


def find_upper_tangent_bruteforce(L: List[Point], R: List[Point]) -> Tuple[Point, Point]:
    """
    위쪽 공통 접선: p∈L, q∈R 에 대해, 나머지 모든 점 r이 직선 pq의 아래 또는 위에 있지 않게
    (orient(p,q,r) > 0 인 r이 없음 → 아무도 pq보다 '위'에 없음).
    """
    pts = L + R
    candidates: List[Tuple[Point, Point]] = []
    for p in L:
        for q in R:
            if all(
                orient(p, q, r) <= 0
                for r in pts
                if r != p and r != q
            ):
                candidates.append((p, q))
    if not candidates:
        raise RuntimeError("upper tangent not found")
    return max(candidates, key=lambda pq: (min(pq[0][1], pq[1][1]), max(pq[0][1], pq[1][1])))


def find_lower_tangent_bruteforce(L: List[Point], R: List[Point]) -> Tuple[Point, Point]:
    """아래쪽 공통 접선: 모든 r에 대해 orient(p,q,r) >= 0 (pq 아래에 다른 점이 없음)."""
    pts = L + R
    candidates = []
    for p in L:
        for q in R:
            if all(
                orient(p, q, r) >= 0
                for r in pts
                if r != p and r != q
            ):
                candidates.append((p, q))
    if not candidates:
        raise RuntimeError("lower tangent not found")
    return min(candidates, key=lambda pq: (max(pq[0][1], pq[1][1]), pq[0][0] + pq[1][0]))


def merge_half_hulls(
    hull1: List[Point],
    hull2: List[Point],
    upper_bound: Tuple[Point, Point],
    lower_bound: Tuple[Point, Point],
) -> List[Point]:
    """
    안정적인 merge:
    - hull1: 왼쪽 half hull (CCW)
    - hull2: 오른쪽 half hull (CCW)
    - upper_bound = (hull1의 위 접점, hull2의 위 접점)
    - lower_bound = (hull2의 아래 접점, hull1의 아래 접점)

    핵심:
    각 hull에서 두 접점 사이의 경로는 2개가 있는데,
    그중 전체 CH에 포함되는 **바깥쪽 arc**만 선택해서 이어 붙인다.
    """

    # upper / lower tangent endpoint unpack
    p_up, q_up = upper_bound      # p_up in hull1, q_up in hull2
    q_lo, p_lo = lower_bound      # q_lo in hull2, p_lo in hull1

    # 각 hull에서 접점 인덱스 찾기
    i_up = hull1.index(p_up)
    i_lo = hull1.index(p_lo)

    j_up = hull2.index(q_up)
    j_lo = hull2.index(q_lo)

    # L: lower→upper 바깥 = 서쪽 호 / R: upper→lower 바깥 = 동쪽 호
    left_chain = pick_outer_arc_between(hull1, i_lo, i_up, is_left_polygon=True)
    right_chain = pick_outer_arc_between(hull2, j_up, j_lo, is_left_polygon=False)

    # 이어 붙이기
    merged = left_chain + right_chain

    # 중복 정리
    cleaned = []
    for p in merged:
        if not cleaned or cleaned[-1] != p:
            cleaned.append(p)

    # 시작점과 끝점이 다르면 닫기
    if cleaned[0] != cleaned[-1]:
        cleaned.append(cleaned[0])

    return cleaned


def merge_half_hulls_outer_fallback(
    L_ccw: List[Point],
    R_ccw: List[Point],
    p_up: Point,
    q_up: Point,
    p_lo: Point,
    q_lo: Point,
) -> List[Point]:
    """노트북 순회가 꼬일 때(접선은 맞는데 CCW 호 가정이 어긋날 때) 바깥쪽 호만 이어 붙인다."""
    i_lo = L_ccw.index(p_lo)
    i_up = L_ccw.index(p_up)
    j_up = R_ccw.index(q_up)
    j_lo = R_ccw.index(q_lo)
    chain_l = pick_outer_arc_between(L_ccw, i_lo, i_up, is_left_polygon=True)
    chain_r = pick_outer_arc_between(R_ccw, j_up, j_lo, is_left_polygon=False)
    merged = chain_l + chain_r
    merged.append(merged[0])
    return merged


def dac_convex_hull(points: List[Point]) -> List[Point]:
    """Divide → conquer each half → upper_lower + merge_half_hulls (노트북 형식)."""
    h1, h2 = separate_half_planes(points)
    raw_a = generate_convex_hull(h1)
    raw_b = generate_convex_hull(h2)
    hull1_ccw = hull_to_ccw_ring(raw_a)
    hull2_ccw = hull_to_ccw_ring(raw_b)

    upper_bound, lower_bound = upper_lower(hull1_ccw, hull2_ccw)
    try:
        merged = merge_half_hulls(hull1_ccw, hull2_ccw, upper_bound, lower_bound)
    except RuntimeError:
        p_up, q_up = upper_bound
        q_lo, p_lo = lower_bound
        merged = merge_half_hulls_outer_fallback(
            hull1_ccw, hull2_ccw, p_up, q_up, p_lo, q_lo
        )
    return merged


def _hull_ring_for_plot(hull: List[Point]) -> List[Point]:
    """Gift wrapping 결과가 [start, ..., start] 형태일 때 닫힌 선분용으로 마지막 중복 제거."""
    if len(hull) >= 2 and hull[0] == hull[-1]:
        return hull[:-1]
    return hull


# ---------------------------------------------------------------------------
# 시각화: 한 figure에 2×2 패널 (흐름을 옆으로 나란히)
# ---------------------------------------------------------------------------
def plot_pipeline(
    points: List[Point],
    half1: List[Point],
    half2: List[Point],
    hull1: List[Point],
    hull2: List[Point],
    merged: List[Point],
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    fig.suptitle("DAC Convex Hull — pipeline", fontsize=14)

    def scatter_pts(ax, pts, c, label, plot_hull=None, hc="k"):
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        ax.scatter(xs, ys, c=c, s=40, zorder=3)
        if plot_hull:
            hx = [p[0] for p in plot_hull] + [plot_hull[0][0]]
            hy = [p[1] for p in plot_hull] + [plot_hull[0][1]]
            ax.plot(hx, hy, color=hc, linewidth=1.5)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, alpha=0.3)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend([label], loc="upper right")

    # (0,0) 전체 점
    ax = axes[0, 0]
    scatter_pts(ax, points, "tab:blue", "30 points")

    # (0,1) 반평면
    ax = axes[0, 1]
    ax.scatter([p[0] for p in half1], [p[1] for p in half1], c="tab:blue", label="half 1", s=40)
    ax.scatter([p[0] for p in half2], [p[1] for p in half2], c="tab:red", label="half 2", s=40)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title("Divide: x-sort → left / right")

        # (1,0) 각 half 볼록 껍질 — 전체 점 + half 내부(껍질 위가 아닌) 점 + 껍질
    ax = axes[1, 0]
    r1 = _hull_ring_for_plot(hull1)
    r2 = _hull_ring_for_plot(hull2)
    h1_set = set(r1)
    h2_set = set(r2)
    interior1 = [p for p in half1 if p not in h1_set]
    interior2 = [p for p in half2 if p not in h2_set]

    ax.scatter(
        [p[0] for p in points],
        [p[1] for p in points],
        c="lightgray",
        s=28,
        alpha=0.85,
        zorder=1,
        label="all points",
    )
    if interior1:
        ax.scatter(
            [p[0] for p in interior1],
            [p[1] for p in interior1],
            c="tab:blue",
            s=45,
            alpha=0.55,
            marker="o",
            zorder=2,
            label="half1 inside (not on hull)",
        )
    if interior2:
        ax.scatter(
            [p[0] for p in interior2],
            [p[1] for p in interior2],
            c="tab:red",
            s=45,
            alpha=0.55,
            marker="o",
            zorder=2,
            label="half2 inside (not on hull)",
        )

    h1x = [p[0] for p in r1] + [r1[0][0]]
    h1y = [p[1] for p in r1] + [r1[0][1]]
    h2x = [p[0] for p in r2] + [r2[0][0]]
    h2y = [p[1] for p in r2] + [r2[0][1]]
    ax.plot(h1x, h1y, "-o", color="tab:blue", markersize=7, zorder=4, label="hull left")
    ax.plot(h2x, h2y, "-o", color="tab:red", markersize=7, zorder=4, label="hull right")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best", fontsize=8)
    ax.set_title("Conquer: hull per half (+ all points & interior)")
    # (1,1) merge 결과
    ax = axes[1, 1]
    scatter_pts(ax, points, "lightgray", "all points")
    rm = _hull_ring_for_plot(merged)
    mx = [p[0] for p in rm] + [rm[0][0]]
    my = [p[1] for p in rm] + [rm[0][1]]
    ax.plot(mx, my, "-", color="darkgreen", linewidth=2, label="merged hull (DAC)")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_title("Merge: upper_lower + merge_half_hulls")

    plt.tight_layout()
    out = os.path.join(os.path.dirname(__file__), "dac_convex_hull_pipeline.png")
    plt.savefig(out, dpi=150)
    print(f"Saved figure: {out}")
    if os.environ.get("MPLBACKEND", "Agg") != "Agg":
        plt.show()
    plt.close()


def main() -> None:
    points = generate_valid_points(30, seed=42)
    half1, half2 = separate_half_planes(points)
    hull1 = generate_convex_hull(half1)
    hull2 = generate_convex_hull(half2)

    try:
        merged = dac_convex_hull(points)
    except (ValueError, IndexError, RuntimeError) as e:
        print("Merge 단계에서 예외:", e)
        print("→ 전체 점에 대해 generate_convex_hull 로 볼록 껍질을 그립니다 (비교·백업).")
        merged = generate_convex_hull(points)

    print("점 개수:", len(points))
    print("왼쪽 half:", len(half1), " 오른쪽 half:", len(half2))
    print("hull (left) 꼭짓점 수:", len(hull1))
    print("hull (right) 꼭짓점 수:", len(hull2))
    print("merged hull 꼭짓점 수:", len(merged))

    plot_pipeline(points, half1, half2, hull1, hull2, merged)


if __name__ == "__main__":
    main()
