"""Reusable L1/cut-metric certificates for the Gamma transfer."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence

import networkx as nx

from .gamma import Edge, cut_size, verify_gamma_instance


@dataclass(frozen=True)
class WeightedCut:
    side: frozenset[int]
    weight: Fraction = Fraction(1)


@dataclass(frozen=True)
class CutMetricReport:
    valid_instance: bool
    dominates_m_distances: bool
    cut_cost: Fraction
    distance_sum: int
    gamma: int
    sufficient_scalar_bound: bool


def verify_cut_metric_certificate(
    b_graph: nx.Graph,
    m_edges: Iterable[Edge],
    cuts: Sequence[WeightedCut],
) -> CutMetricReport:
    """Verify a finite cut-metric domination certificate.

    If the supplied cut metric dominates `d_B` on every M edge, maximum-cut
    domination gives `sum_M d_B <= cut_cost`. Since every M distance is at
    least four,

        Gamma <= (diam(B) + 9/4) * cut_cost.

    The final Boolean records whether this scalar estimate is at most N^2.
    Stronger structural arguments, such as the exact cactus theorem, may still
    succeed when this generic criterion does not.
    """
    m_edges = tuple(m_edges)
    instance = verify_gamma_instance(b_graph, m_edges)
    if not instance.valid:
        return CutMetricReport(False, False, Fraction(0), 0, instance.gamma, False)

    distances = dict(nx.all_pairs_shortest_path_length(b_graph))
    dominates = True
    for u, v in m_edges:
        represented = sum(
            cut.weight
            for cut in cuts
            if ((u in cut.side) != (v in cut.side))
        )
        if represented < distances[u][v]:
            dominates = False
            break

    cost = sum(cut.weight * cut_size(b_graph, cut.side) for cut in cuts)
    distance_sum = sum(distances[u][v] for u, v in m_edges)
    diameter = nx.diameter(b_graph)
    sufficient = dominates and cost * (4 * diameter + 9) <= 4 * instance.order**2
    return CutMetricReport(
        valid_instance=True,
        dominates_m_distances=dominates,
        cut_cost=cost,
        distance_sum=distance_sum,
        gamma=instance.gamma,
        sufficient_scalar_bound=sufficient,
    )
