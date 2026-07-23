"""The Gamma inequality for cactus maximum-cut graphs.

A connected cactus is a graph whose every biconnected block is either one edge
or one cycle. In the bipartite case all cycle blocks are even and their graph
metric has an exact cut decomposition. Together with maximum-cut domination,
this controls the sum of all M-edge distances.
"""

from __future__ import annotations

from typing import Iterable

import networkx as nx

from .gamma import Edge, verify_gamma_instance


def cactus_cycle_count(graph: nx.Graph) -> int:
    """Return the number of cycle blocks, rejecting non-cactus graphs."""
    if not nx.is_connected(graph):
        raise ValueError("the graph must be connected")
    cycle_count = 0
    for block_edges_iter in nx.biconnected_component_edges(graph):
        block_edges = list(block_edges_iter)
        if len(block_edges) == 1:
            continue
        block = nx.Graph()
        block.add_edges_from(block_edges)
        if block.number_of_edges() != block.number_of_nodes():
            raise ValueError("a nontrivial block is not a cycle")
        if any(degree != 2 for _, degree in block.degree()):
            raise ValueError("a nontrivial block is not a simple cycle")
        cycle_count += 1
    return cycle_count


def cactus_scalar_bound(order: int, cycle_count: int, distances: Iterable[int]) -> bool:
    """Check the final exact arithmetic lemma used by the cactus proof.

    Required structural inputs are

        sum d_i <= N - 1 + q,
        max d_i <= N - 1 - q,
        d_i even and d_i >= 4,
        N >= 3q + 1.

    The sole loose parameter corner `(N,q,k)=(7,2,2)` cannot occur in a simple
    valid instance: the unique graph is two C4 blocks sharing one vertex and it
    has only one same-side pair at distance at least four.
    """
    values = tuple(distances)
    if order <= 0 or cycle_count < 0:
        return False
    if order < 3 * cycle_count + 1:
        return False
    if any(distance < 4 or distance % 2 for distance in values):
        return False
    if sum(values) > order - 1 + cycle_count:
        return False
    if values and max(values) > order - 1 - cycle_count:
        return False
    if (order, cycle_count, len(values)) == (7, 2, 2):
        return False
    return sum((distance + 1) ** 2 for distance in values) <= order * order


def verify_cactus_proof_certificate(b_graph: nx.Graph, m_edges: Iterable[Edge]) -> bool:
    """Mechanically audit a concrete instance of the cactus theorem."""
    m_edges = tuple(m_edges)
    report = verify_gamma_instance(b_graph, m_edges)
    if not report.valid or not nx.is_bipartite(b_graph):
        return False
    try:
        cycle_count = cactus_cycle_count(b_graph)
    except ValueError:
        return False
    distances_map = dict(nx.all_pairs_shortest_path_length(b_graph))
    distances = tuple(distances_map[u][v] for u, v in m_edges)
    return cactus_scalar_bound(report.order, cycle_count, distances)
