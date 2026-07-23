"""Exact falsifier for a rejected component-potential strengthening.

The rejected statement assigned positive vertex weights x_v to each connected
component C of M with x_u x_v >= (d_B(u,v)+1)^2 on every M edge and conjectured
that the squared minimum total potential, summed over components, is at most
4N^2. The instance below satisfies every Gamma-transfer hypothesis but has one
P5 component with potential tau = 10 sqrt(6), hence tau^2 = 600 > 576.

This does not refute the Gamma inequality or Erdős Problem #23: its Gamma is
100 <= 144.
"""

from __future__ import annotations

import networkx as nx

from .gamma import Edge, GammaInstanceReport, verify_gamma_instance

TAU_COUNTEREXAMPLE_B_EDGES: tuple[Edge, ...] = (
    (0, 6), (0, 7), (0, 9), (0, 10),
    (1, 10), (1, 11),
    (2, 6), (2, 7), (2, 9), (2, 10),
    (3, 7), (3, 8),
    (4, 7), (4, 8), (4, 10),
    (5, 9), (5, 11),
)
TAU_COUNTEREXAMPLE_M_EDGES: tuple[Edge, ...] = (
    (6, 8), (6, 11), (7, 11), (8, 9),
)
TAU_COUNTEREXAMPLE_GRAPH6 = "K??DDoWhFOG_"


def tau_counterexample() -> tuple[nx.Graph, tuple[Edge, ...]]:
    b_graph = nx.Graph()
    b_graph.add_nodes_from(range(12))
    b_graph.add_edges_from(TAU_COUNTEREXAMPLE_B_EDGES)
    return b_graph, TAU_COUNTEREXAMPLE_M_EDGES


def verify_tau_counterexample() -> GammaInstanceReport:
    """Verify the graph hypotheses and exact scalar contradiction."""
    b_graph, m_edges = tau_counterexample()
    report = verify_gamma_instance(b_graph, m_edges)
    if not report.valid:
        raise AssertionError(report.errors)
    if nx.to_graph6_bytes(b_graph, header=False).decode().strip() != TAU_COUNTEREXAMPLE_GRAPH6:
        raise AssertionError("graph6 regression mismatch")
    distances = dict(nx.all_pairs_shortest_path_length(b_graph))
    if any(distances[u][v] != 4 for u, v in m_edges):
        raise AssertionError("all four M edges must have B-distance four")
    if report.gamma != 100 or report.order * report.order != 144:
        raise AssertionError("Gamma regression mismatch")
    tau_squared = 600
    four_n_squared = 4 * report.order * report.order
    if not tau_squared > four_n_squared:
        raise AssertionError("the rejected tau inequality was not falsified")
    return report
