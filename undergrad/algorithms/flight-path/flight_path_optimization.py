#!/usr/bin/env python3
"""
Flight path optimization: Jeju (node 1) → Yangyang (node 4)
Fixed graph: nodes 3 and 4 are not adjacent. Weather polygon from assignment.
A* with haversine heuristic; Dijkstra for cross-check.
"""

from __future__ import annotations

import heapq
import math
import os
from typing import Callable, Dict, List, Optional, Set, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon

Point = Tuple[float, float]

# Earth radius for haversine (km)
R_EARTH_KM = 6371.0

# --- Fixed graph (assignment): lon, lat in degrees ---
NODES: Dict[int, Point] = {
    1: (126.5, 33.5),  # Jeju International Airport
    2: (126.5, 37.45),
    3: (127.5, 36.7),
    4: (128.7, 38.1),  # Yangyang International Airport
    5: (128.9, 35.2),
    6: (129.4, 36.0),
}

# Undirected edges as adjacency (assignment graph; **3 and 4 are not connected**)
ADJ: Dict[int, List[int]] = {
    1: [2, 3, 5],
    2: [1, 3, 4],
    3: [1, 2, 5, 6],  # no edge 3–4
    4: [2, 6],
    5: [1, 3, 6],
    6: [3, 4, 5],
}

# Display names for plot (coordinates ≈ metro / airport region)
CITY_NAME: Dict[int, str] = {
    1: "Jeju",
    2: "Incheon",
    3: "Daejeon",
    4: "Yangyang",
    5: "Busan",
    6: "Ulsan",
}

# Severe weather: axis-aligned rectangle (lon, lat), closed polygon order
WEATHER_POLYGON: List[Point] = [
    (128.7, 36.6),
    (128.7, 37.6),
    (129.3, 37.6),
    (129.3, 36.6),
]


def haversine_km(a: Point, b: Point) -> float:
    """Great-circle distance between two (lon, lat) points in degrees."""
    lon1, lat1 = map(math.radians, a)
    lon2, lat2 = map(math.radians, b)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(min(1.0, math.sqrt(h)))
    return R_EARTH_KM * c


def _orient(a: Point, b: Point, c: Point) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _on_segment(a: Point, b: Point, p: Point, eps: float = 1e-12) -> bool:
    return (
        min(a[0], b[0]) - eps <= p[0] <= max(a[0], b[0]) + eps
        and min(a[1], b[1]) - eps <= p[1] <= max(a[1], b[1]) + eps
        and abs(_orient(a, b, p)) < 1e-9
    )


def segments_intersect(p1: Point, p2: Point, q1: Point, q2: Point) -> bool:
    """True if closed segments share a point (proper or endpoint touch)."""
    o1 = _orient(p1, p2, q1)
    o2 = _orient(p1, p2, q2)
    o3 = _orient(q1, q2, p1)
    o4 = _orient(q1, q2, p2)

    def sgn(x: float) -> int:
        if x > 1e-9:
            return 1
        if x < -1e-9:
            return -1
        return 0

    if sgn(o1) != sgn(o2) and sgn(o3) != sgn(o4):
        return True
    if sgn(o1) == 0 and _on_segment(p1, p2, q1):
        return True
    if sgn(o2) == 0 and _on_segment(p1, p2, q2):
        return True
    if sgn(o3) == 0 and _on_segment(q1, q2, p1):
        return True
    if sgn(o4) == 0 and _on_segment(q1, q2, p2):
        return True
    return False


def segment_hits_weather_box(p1: Point, p2: Point, poly: List[Point]) -> bool:
    """
    Forbidden if the flight segment intersects the closed weather rectangle
    (including boundary) in a way that would require entering the area.
    We treat: any intersection with the closed polygon region as blocked.
    """
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    def inside_closed(p: Point) -> bool:
        return xmin <= p[0] <= xmax and ymin <= p[1] <= ymax

    if inside_closed(p1) or inside_closed(p2):
        return True

    rect_corners = [
        (xmin, ymin),
        (xmax, ymin),
        (xmax, ymax),
        (xmin, ymax),
    ]
    for i in range(4):
        a, b = rect_corners[i], rect_corners[(i + 1) % 4]
        if segments_intersect(p1, p2, a, b):
            return True
    return False


def build_weighted_graph(block_weather: bool) -> Dict[int, List[Tuple[int, float]]]:
    """Adjacency with edge weights (km). Drop edges that cross weather if block_weather."""
    g: Dict[int, List[Tuple[int, float]]] = {n: [] for n in NODES}
    seen: Set[Tuple[int, int]] = set()
    for u in ADJ:
        for v in ADJ[u]:
            if u > v:
                continue
            if (u, v) in seen:
                continue
            seen.add((u, v))
            a, b = NODES[u], NODES[v]
            if block_weather and segment_hits_weather_box(a, b, WEATHER_POLYGON):
                continue
            w = haversine_km(a, b)
            g[u].append((v, w))
            g[v].append((u, w))
    return g


def astar(
    graph: Dict[int, List[Tuple[int, float]]],
    start: int,
    goal: int,
    heuristic: Callable[[int, int], float],
) -> Tuple[Optional[float], Optional[List[int]]]:
    """A*; returns (total_cost_km, path) or (None, None) if unreachable."""
    open_heap: List[Tuple[float, float, int]] = []
    heapq.heappush(open_heap, (heuristic(start, goal), 0.0, start))
    came_from: Dict[int, int] = {}
    g_score: Dict[int, float] = {start: 0.0}

    while open_heap:
        _f, g, u = heapq.heappop(open_heap)
        if g > g_score.get(u, float("inf")) + 1e-9:
            continue  # stale heap entry
        if u == goal:
            path = [u]
            while path[-1] != start:
                path.append(came_from[path[-1]])
            path.reverse()
            return g, path

        for v, w in graph.get(u, []):
            tentative = g_score[u] + w
            if tentative < g_score.get(v, float("inf")):
                came_from[v] = u
                g_score[v] = tentative
                h = heuristic(v, goal)
                heapq.heappush(open_heap, (tentative + h, tentative, v))

    return None, None


def dijkstra(
    graph: Dict[int, List[Tuple[int, float]]],
    start: int,
    goal: int,
) -> Tuple[Optional[float], Optional[List[int]]]:
    """Dijkstra for comparison / tie-check."""
    dist: Dict[int, float] = {start: 0.0}
    prev: Dict[int, int] = {}
    pq: List[Tuple[float, int]] = [(0.0, start)]
    visited: Set[int] = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if u == goal:
            break
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    if goal not in dist:
        return None, None
    path = [goal]
    while path[-1] != start:
        path.append(prev[path[-1]])
    path.reverse()
    return dist[goal], path


def plot_results(
    clear_path: List[int],
    severe_path: Optional[List[int]],
    clear_cost: float,
    severe_cost: Optional[float],
    out_path: str,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 8))

    poly = MplPolygon(
        WEATHER_POLYGON,
        closed=True,
        facecolor="crimson",
        edgecolor="darkred",
        alpha=0.35,
        linewidth=1.5,
        label="Severe weather (forbidden)",
    )
    ax.add_patch(poly)

    # Draw all nominal edges (light)
    drawn: Set[Tuple[int, int]] = set()
    for u in ADJ:
        for v in ADJ[u]:
            if u > v:
                continue
            if (u, v) in drawn:
                continue
            drawn.add((u, v))
            x1, y1 = NODES[u]
            x2, y2 = NODES[v]
            blocked = segment_hits_weather_box(NODES[u], NODES[v], WEATHER_POLYGON)
            style = {"color": "gray", "linestyle": "--", "alpha": 0.6, "linewidth": 1.0}
            if blocked:
                style = {"color": "tomato", "linestyle": "--", "alpha": 0.9, "linewidth": 1.2}
            ax.plot([x1, x2], [y1, y2], **style)

    def plot_path(path: List[int], color: str, lw: float, label: str) -> None:
        xs = [NODES[i][0] for i in path]
        ys = [NODES[i][1] for i in path]
        ax.plot(xs, ys, "-", color=color, linewidth=lw, marker="o", markersize=8, label=label)

    plot_path(clear_path, "navy", 2.5, f"Clear shortest (~{clear_cost:.1f} km)")
    if severe_path:
        plot_path(severe_path, "darkgreen", 2.2, f"Severe shortest (~{severe_cost:.1f} km)")
    else:
        ax.plot([], [], "-", color="darkgreen", label="Severe: no path")

    # Offset labels slightly so they do not sit on top of each other
    label_xy: Dict[int, Tuple[int, int]] = {
        1: (8, 8),
        2: (-52, 8),
        3: (8, -18),
        4: (8, 8),
        5: (8, -18),
        6: (8, 8),
    }
    for nid, (x, y) in NODES.items():
        ax.scatter([x], [y], c="black", s=120, zorder=5)
        city = CITY_NAME[nid]
        ox, oy = label_xy.get(nid, (8, 8))
        ax.annotate(
            f"{nid}: {city}",
            (x, y),
            textcoords="offset points",
            xytext=(ox, oy),
            fontsize=9,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="0.7", alpha=0.92),
        )

    ax.set_xlabel("Longitude (deg)")
    ax.set_ylabel("Latitude (deg)")
    ax.set_title("Flight path graph — clear vs severe weather")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper left", fontsize=9)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved figure: {out_path}")


def main() -> None:
    start, goal = 1, 4
    h = lambda u, g: haversine_km(NODES[u], NODES[g])

    g_clear = build_weighted_graph(block_weather=False)
    g_severe = build_weighted_graph(block_weather=True)

    c_cost, c_path = astar(g_clear, start, goal, h)
    assert c_path is not None
    d_cost, d_path = dijkstra(g_clear, start, goal)
    assert abs((c_cost or 0) - (d_cost or 0)) < 1e-6 and c_path == d_path

    s_cost, s_path = astar(g_severe, start, goal, h)
    d_s_cost, d_s_path = dijkstra(g_severe, start, goal)
    if s_cost is not None:
        assert abs(s_cost - d_s_cost) < 1e-6 and s_path == d_s_path

    out_png = os.path.join(os.path.dirname(__file__), "flight_path_result.png")
    plot_results(c_path, s_path, c_cost, s_cost, out_png)

    def path_str(path: List[int]) -> str:
        parts = [f"{n} ({CITY_NAME[n]})" for n in path]
        return " -> ".join(parts)

    print("=== Clear weather ===")
    print(f"  Shortest distance: {c_cost:.3f} km")
    print(f"  Path: {path_str(c_path)}")

    print("=== Severe weather (edges through polygon removed) ===")
    if s_path:
        print(f"  Shortest distance: {s_cost:.3f} km")
        print(f"  Path: {path_str(s_path)}")
    else:
        print("  No path from 1 to 4.")

    # List blocked edges for report
    print("\nEdges removed under severe weather (segment intersects closed weather box):")
    for u in sorted(ADJ.keys()):
        for v in ADJ[u]:
            if u < v:
                if segment_hits_weather_box(NODES[u], NODES[v], WEATHER_POLYGON):
                    print(f"  ({u}-{v})")


if __name__ == "__main__":
    main()
