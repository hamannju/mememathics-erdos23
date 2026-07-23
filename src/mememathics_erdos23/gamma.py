"""Exact checks around the maximum-cut Γ reduction for Erdős Problem #23.

For a maximum cut of a triangle-free graph G, let B be the crossing-edge graph
and M the monochromatic-edge graph. The open transfer inequality isolated in
Ferudun (2026) is

    Γ(B, M) = Σ_{uv in M} (dist_B(u, v) + 1)^2 <= |V|^2.

This module does not assume the inequality. It verifies finite instances and
solves the fixed-B extremal MILP used for adversarial testing.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Iterator, Mapping, Sequence

import networkx as nx
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

Edge = tuple[int, int]
WeightedBadEdge = tuple[int, int, int]


@dataclass(frozen=True)
class GammaInstanceReport:
    order: int
    b_edges: int
    m_edges: int
    gamma: int
    valid: bool
    errors: tuple[str, ...]

    @property
    def ratio(self) -> float:
        return self.gamma / (self.order * self.order) if self.order else 0.0


def _normalise_edge(edge: Edge) -> Edge:
    u, v = edge
    if u == v:
        raise ValueError("loops are not allowed")
    return (u, v) if u < v else (v, u)


def _normalised_graph(graph: nx.Graph) -> nx.Graph:
    if graph.is_directed() or graph.is_multigraph():
        raise TypeError("a finite simple undirected graph is required")
    return nx.convert_node_labels_to_integers(graph, ordering="sorted")


def nontrivial_cuts(order: int) -> Iterator[frozenset[int]]:
    """Yield each nontrivial cut once, fixing vertex 0 outside the chosen side."""
    if order <= 1:
        return
    for mask in range(1, 1 << (order - 1)):
        yield frozenset(i + 1 for i in range(order - 1) if mask & (1 << i))


def cut_size(graph: nx.Graph, side: frozenset[int] | set[int]) -> int:
    return sum((u in side) != (v in side) for u, v in graph.edges())


def candidate_bad_edges(b_graph: nx.Graph) -> list[WeightedBadEdge]:
    """Return same-side pairs at B-distance at least four.

    In a connected bipartite cut graph B, an M edge joins vertices in the same
    bipartition class. Triangle-freeness of B ∪ M excludes distance two.
    """
    b_graph = _normalised_graph(b_graph)
    if not nx.is_connected(b_graph):
        raise ValueError("B must be connected")
    if not nx.is_bipartite(b_graph):
        raise ValueError("B must be bipartite")

    colour = nx.bipartite.color(b_graph)
    distances: Mapping[int, Mapping[int, int]] = dict(nx.all_pairs_shortest_path_length(b_graph))
    result: list[WeightedBadEdge] = []
    for u, v in combinations(range(b_graph.number_of_nodes()), 2):
        distance = distances[u][v]
        if colour[u] == colour[v] and distance >= 4:
            result.append((u, v, distance))
    return result


def gamma_value(b_graph: nx.Graph, m_edges: Iterable[Edge]) -> int:
    b_graph = _normalised_graph(b_graph)
    distances = dict(nx.all_pairs_shortest_path_length(b_graph))
    total = 0
    for raw_edge in m_edges:
        u, v = _normalise_edge(raw_edge)
        total += (distances[u][v] + 1) ** 2
    return total


def verify_gamma_instance(b_graph: nx.Graph, m_edges: Iterable[Edge]) -> GammaInstanceReport:
    """Check every finite hypothesis behind the Γ transfer problem.

    Checks:
    - B is connected and bipartite;
    - M is simple, edge-disjoint from B, and same-side;
    - B ∪ M is triangle-free;
    - every cut obeys |δ_M(S)| <= |δ_B(S)|, equivalently the selected
      B-cut is maximum for G = B ∪ M.
    """
    b_graph = _normalised_graph(b_graph)
    order = b_graph.number_of_nodes()
    errors: list[str] = []

    if not nx.is_connected(b_graph):
        errors.append("B is disconnected")
    if not nx.is_bipartite(b_graph):
        errors.append("B is not bipartite")

    normalised_m: list[Edge] = []
    seen: set[Edge] = set()
    for raw_edge in m_edges:
        edge = _normalise_edge(raw_edge)
        if edge in seen:
            errors.append(f"duplicate M edge {edge}")
            continue
        seen.add(edge)
        normalised_m.append(edge)

    m_graph = nx.Graph()
    m_graph.add_nodes_from(range(order))
    m_graph.add_edges_from(normalised_m)

    if nx.is_bipartite(b_graph):
        colour = nx.bipartite.color(b_graph)
        for u, v in normalised_m:
            if colour[u] != colour[v]:
                errors.append(f"M edge {(u, v)} crosses the B bipartition")
            if b_graph.has_edge(u, v):
                errors.append(f"edge {(u, v)} occurs in both B and M")

    combined = nx.compose(b_graph, m_graph)
    if any(nx.triangles(combined).values()):
        errors.append("B ∪ M contains a triangle")

    if nx.is_connected(b_graph):
        for side in nontrivial_cuts(order):
            b_capacity = cut_size(b_graph, side)
            m_demand = cut_size(m_graph, side)
            if m_demand > b_capacity:
                errors.append(
                    f"cut violation at {sorted(side)}: M={m_demand}, B={b_capacity}"
                )
                break

    gamma = gamma_value(b_graph, normalised_m) if nx.is_connected(b_graph) else 0
    return GammaInstanceReport(
        order=order,
        b_edges=b_graph.number_of_edges(),
        m_edges=len(normalised_m),
        gamma=gamma,
        valid=not errors,
        errors=tuple(errors),
    )


def maximum_cut_decomposition(graph: nx.Graph, side: Iterable[int]) -> tuple[nx.Graph, nx.Graph]:
    """Split G into crossing graph B and monochromatic graph M for a cut."""
    graph = _normalised_graph(graph)
    chosen = frozenset(side)
    b_graph = nx.Graph()
    m_graph = nx.Graph()
    b_graph.add_nodes_from(graph.nodes())
    m_graph.add_nodes_from(graph.nodes())
    for u, v in graph.edges():
        target = b_graph if ((u in chosen) != (v in chosen)) else m_graph
        target.add_edge(u, v)
    return b_graph, m_graph


def _triangle_rows(
    order: int,
    candidates: Sequence[WeightedBadEdge],
    colour: Mapping[int, int],
) -> list[np.ndarray]:
    index = {(u, v): i for i, (u, v, _) in enumerate(candidates)}
    rows: list[np.ndarray] = []
    for a, b, c in combinations(range(order), 3):
        if not (colour[a] == colour[b] == colour[c]):
            continue
        edges = [(min(a, b), max(a, b)), (min(a, c), max(a, c)), (min(b, c), max(b, c))]
        if all(edge in index for edge in edges):
            row = np.zeros(len(candidates), dtype=float)
            for edge in edges:
                row[index[edge]] = 1.0
            rows.append(row)
    return rows


def maximize_gamma_for_fixed_b(
    b_graph: nx.Graph,
    *,
    time_limit_seconds: float = 60.0,
) -> tuple[int, list[WeightedBadEdge]]:
    """Maximise Γ over all simple triangle-free M satisfying every cut constraint.

    The formulation is exact up to the MILP solver's integral certificate/status.
    It is intended as an adversarial finite-instance oracle, not as a proof of the
    general conjecture.
    """
    b_graph = _normalised_graph(b_graph)
    if not nx.is_connected(b_graph) or not nx.is_bipartite(b_graph):
        raise ValueError("B must be connected and bipartite")

    candidates = candidate_bad_edges(b_graph)
    if not candidates:
        return 0, []

    objective = -np.asarray([(distance + 1) ** 2 for _, _, distance in candidates], dtype=float)
    rows: list[np.ndarray] = []
    upper: list[float] = []

    for side in nontrivial_cuts(b_graph.number_of_nodes()):
        row = np.asarray(
            [1.0 if ((u in side) != (v in side)) else 0.0 for u, v, _ in candidates],
            dtype=float,
        )
        if np.any(row):
            rows.append(row)
            upper.append(float(cut_size(b_graph, side)))

    colour = nx.bipartite.color(b_graph)
    for row in _triangle_rows(b_graph.number_of_nodes(), candidates, colour):
        rows.append(row)
        upper.append(2.0)

    matrix = np.vstack(rows) if rows else np.zeros((0, len(candidates)), dtype=float)
    constraints = LinearConstraint(
        matrix,
        np.full(len(rows), -np.inf, dtype=float),
        np.asarray(upper, dtype=float),
    )
    result = milp(
        objective,
        integrality=np.ones(len(candidates), dtype=int),
        bounds=Bounds(np.zeros(len(candidates)), np.ones(len(candidates))),
        constraints=constraints,
        options={"time_limit": time_limit_seconds, "mip_rel_gap": 0.0},
    )
    if not result.success or result.x is None or result.fun is None:
        raise RuntimeError(f"MILP did not close exactly: {result.message}")

    chosen = [candidate for candidate, value in zip(candidates, result.x) if value > 0.5]
    optimum = int(round(-float(result.fun)))
    return optimum, chosen


def path_closure_instance(order: int) -> tuple[nx.Graph, list[Edge]]:
    """Return the sharp path instance P_n plus one endpoint M edge (odd n >= 5)."""
    if order < 5 or order % 2 == 0:
        raise ValueError("order must be odd and at least five")
    return nx.path_graph(order), [(0, order - 1)]


def c5_blowup_cut_instance(class_size: int) -> tuple[nx.Graph, list[Edge]]:
    """A maximum-cut decomposition of the balanced C5 blow-up.

    B is the blow-up of a five-vertex path and M is the complete bipartite
    graph between the two endpoint classes. Γ = (5^2) * class_size^2 = N^2.
    """
    if class_size <= 0:
        raise ValueError("class_size must be positive")
    layers = [list(range(i * class_size, (i + 1) * class_size)) for i in range(5)]
    b_graph = nx.Graph()
    b_graph.add_nodes_from(range(5 * class_size))
    for left, right in zip(layers, layers[1:]):
        b_graph.add_edges_from((u, v) for u in left for v in right)
    m_edges = [(u, v) for u in layers[0] for v in layers[4]]
    return b_graph, m_edges
