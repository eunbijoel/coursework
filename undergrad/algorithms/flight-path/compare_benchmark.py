#!/usr/bin/env python3
"""Quick benchmark: flight_path_optimization.py vs notebook-style logic (embedded data)."""

from __future__ import annotations

import time

# --- Import production .py implementation ---
import flight_path_optimization as fpo

# --- Notebook graph frozen from Graph Algorithm_OG.ipynb cell outputs (IATA, km) ---
# g[node] = set of (neighbor, weight_km)
NOTEBOOK_G = {
    "CJU": {("CJJ", 367.96727230059986), ("ICN", 437.6144234862817), ("PUS", 291.20743894500595)},
    "ICN": {("CJJ", 123.49657750039117), ("YNY", 206.71158605818974)},
    "CJJ": {("ICN", 123.49657750039117), ("KPO", 190.1964114912266), ("PUS", 214.45396265229365)},
    "PUS": {("CJJ", 214.45396265229365), ("KPO", 99.92598886731854)},
    "KPO": {("CJJ", 190.1964114912266), ("PUS", 99.92598886731854), ("YNY", 239.98884640443018)},
    "YNY": set(),
}

NOTEBOOK_COORDS = {
    "ICN": (126.4498, 37.4465),
    "CJU": (126.4928, 33.5111),
    "CJJ": (127.4989, 36.7164),
    "YNY": (128.6689, 38.0611),
    "KPO": (129.4205, 35.9879),
    "PUS": (128.9381, 35.1794),
}

BAD = [(128.7, 36.6), (128.7, 37.6), (129.3, 37.6), (129.3, 36.6)]


def notebook_style_dijkstra_sampled_edges(
    G: dict, start: str, goal: str, bad_regions: list
) -> tuple[dict | None, float]:
    """Simplified port of notebook: PriorityQueue, sample-based bad-region check."""
    import heapq

    def calculate_line_equation(a, b):
        import numpy as np

        ax, ay = a
        bx, by = b
        if abs(bx - ax) < 1e-15:
            # vertical — notebook original can divide by zero; use y-sweep
            y0, y1 = min(ay, by), max(ay, by)
            return [(ax, y) for y in np.arange(y0, y1, 0.05)]
        slope = (by - ay) / (bx - ax)
        intercept = ay - (slope * ax)
        if ax < bx:
            return [(x, slope * x + intercept) for x in np.arange(ax, bx, 0.05)]
        return [(x, slope * x + intercept) for x in np.arange(bx, ax, 0.05)]

    def is_point_in_bad_area(points, bad):
        xmin, xmax = min(bad[0][0], bad[2][0]), max(bad[0][0], bad[2][0])
        ymin, ymax = min(bad[0][1], bad[1][1]), max(bad[0][1], bad[1][1])
        for point in points:
            x, y = point
            if xmin <= x <= xmax and ymin <= y <= ymax:
                return True
        return False

    visited = set()
    cost = {start: 0.0}
    parent = {start: None}
    pq = [(0.0, start)]

    while pq:
        _, vertex = heapq.heappop(pq)
        if vertex in visited:
            continue
        visited.add(vertex)
        if vertex == goal:
            break
        for neighbor, distance in G[vertex]:
            if neighbor in visited:
                continue
            v_cor = NOTEBOOK_COORDS[vertex]
            n_cor = NOTEBOOK_COORDS[neighbor]
            points = calculate_line_equation(v_cor, n_cor)
            crosses = any(is_point_in_bad_area(points, bad) for bad in bad_regions)
            if crosses:
                continue
            old = cost.get(neighbor, float("inf"))
            new_c = cost[vertex] + distance
            if new_c < old:
                cost[neighbor] = new_c
                parent[neighbor] = vertex
                heapq.heappush(pq, (new_c, neighbor))

    if goal not in parent:
        return None, float("nan")
    path = []
    v = goal
    while v is not None:
        path.append(v)
        v = parent[v]
    path.reverse()
    dist = 0.0
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        for nb, w in G[a]:
            if nb == b:
                dist += w
                break
    return parent, dist


def main() -> None:
    n = 5000
    t0 = time.perf_counter()
    for _ in range(n):
        g = fpo.build_weighted_graph(block_weather=False)
        fpo.astar(g, 1, 4, lambda u, gv: fpo.haversine_km(fpo.NODES[u], fpo.NODES[gv]))
    t_py_clear = (time.perf_counter() - t0) / n

    t0 = time.perf_counter()
    for _ in range(n):
        g = fpo.build_weighted_graph(block_weather=True)
        fpo.astar(g, 1, 4, lambda u, gv: fpo.haversine_km(fpo.NODES[u], fpo.NODES[gv]))
    t_py_severe = (time.perf_counter() - t0) / n

    n_nb = 2000
    t0 = time.perf_counter()
    for _ in range(n_nb):
        notebook_style_dijkstra_sampled_edges(NOTEBOOK_G, "CJU", "YNY", [])
    t_nb_clear = (time.perf_counter() - t0) / n_nb

    t0 = time.perf_counter()
    for _ in range(n_nb):
        notebook_style_dijkstra_sampled_edges(NOTEBOOK_G, "CJU", "YNY", [BAD])
    t_nb_severe = (time.perf_counter() - t0) / n_nb

    _, d_nb_clear = notebook_style_dijkstra_sampled_edges(NOTEBOOK_G, "CJU", "YNY", [])
    _, d_nb_sev = notebook_style_dijkstra_sampled_edges(NOTEBOOK_G, "CJU", "YNY", [BAD])

    c_clear, p_clear = fpo.astar(
        fpo.build_weighted_graph(False),
        1,
        4,
        lambda u, gv: fpo.haversine_km(fpo.NODES[u], fpo.NODES[gv]),
    )
    c_sev, p_sev = fpo.astar(
        fpo.build_weighted_graph(True),
        1,
        4,
        lambda u, gv: fpo.haversine_km(fpo.NODES[u], fpo.NODES[gv]),
    )

    print("=== Correctness (single run) ===")
    print(f"  .py clear:    {c_clear:.3f} km  path {p_clear}")
    print(f"  .py severe:   {c_sev:.3f} km  path {p_sev}")
    print(f"  nb clear:     {d_nb_clear:.3f} km  (expected ~631.12 from notebook output)")
    print(f"  nb severe:    {d_nb_sev:.3f} km  (expected ~644.33 from notebook output)")
    print()
    print("=== Mean time per call (rough) ===")
    print(f"  fpo A* clear   {t_py_clear*1e6:.1f} us  (n={n})")
    print(f"  fpo A* severe  {t_py_severe*1e6:.1f} us  (n={n})")
    print(f"  nb Dijkstra clear   {t_nb_clear*1e6:.1f} us  (n={n_nb}, +numpy sampling)")
    print(f"  nb Dijkstra severe  {t_nb_severe*1e6:.1f} us  (n={n_nb})")


if __name__ == "__main__":
    main()
