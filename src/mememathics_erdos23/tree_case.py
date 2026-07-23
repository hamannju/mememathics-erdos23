"""The proved Γ inequality when the maximum-cut graph B is a tree."""

from __future__ import annotations

from collections import Counter
from typing import Iterable

import networkx as nx

from .gamma import Edge, gamma_value, verify_gamma_instance


def tree_path_loads(b_tree: nx.Graph, m_edges: Iterable[Edge]) -> Counter[Edge]:
    """Count how many unique B-paths of M edges use each tree edge."""
    if not nx.is_tree(b_tree):
        raise ValueError("B must be a tree")
    loads: Counter[Edge] = Counter()
    for u, v in m_edges:
        path = nx.shortest_path(b_tree, u, v)
        for a, b in zip(path, path[1:]):
            edge = (a, b) if a < b else (b, a)
            loads[edge] += 1
    return loads


def verify_tree_proof_certificate(b_tree: nx.Graph, m_edges: Iterable[Edge]) -> bool:
    """Mechanically verify the finite inequalities used in the tree proof.

    For each tree edge f, its fundamental cut has B-capacity one. The maximum
    cut condition therefore forces at most one M path through f. Hence the M
    paths are edge-disjoint and Σ d_B(u,v) <= N-1. The scalar inequality

        (d+1)^2 / d <= N^2/(N-1),  1 <= d <= N-1,

    then yields Γ <= N^2.
    """
    m_edges = list(m_edges)
    report = verify_gamma_instance(b_tree, m_edges)
    if not report.valid or not nx.is_tree(b_tree):
        return False
    loads = tree_path_loads(b_tree, m_edges)
    if any(load > 1 for load in loads.values()):
        return False
    order = b_tree.number_of_nodes()
    distance_sum = sum(nx.shortest_path_length(b_tree, u, v) for u, v in m_edges)
    if distance_sum > order - 1:
        return False
    return gamma_value(b_tree, m_edges) <= order * order
