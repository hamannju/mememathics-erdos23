import networkx as nx

from mememathics_erdos23.cactus_case import verify_cactus_proof_certificate
from mememathics_erdos23.gamma import (
    c5_blowup_cut_instance,
    maximize_gamma_for_fixed_b,
    path_closure_instance,
    verify_gamma_instance,
)
from mememathics_erdos23.rejected_tau import verify_tau_counterexample
from mememathics_erdos23.tree_case import verify_tree_proof_certificate


def test_path_closure_is_sharp_at_five() -> None:
    b_graph, m_edges = path_closure_instance(5)
    report = verify_gamma_instance(b_graph, m_edges)
    assert report.valid
    assert report.gamma == 25 == report.order**2
    assert verify_tree_proof_certificate(b_graph, m_edges)
    assert verify_cactus_proof_certificate(b_graph, m_edges)


def test_path_closure_is_sharp_at_seven() -> None:
    b_graph, m_edges = path_closure_instance(7)
    report = verify_gamma_instance(b_graph, m_edges)
    assert report.valid
    assert report.gamma == 49 == report.order**2
    assert verify_tree_proof_certificate(b_graph, m_edges)
    assert verify_cactus_proof_certificate(b_graph, m_edges)


def test_c5_blowup_decomposition_is_sharp() -> None:
    b_graph, m_edges = c5_blowup_cut_instance(3)
    report = verify_gamma_instance(b_graph, m_edges)
    assert report.valid, report.errors
    assert report.order == 15
    assert report.gamma == 225 == report.order**2


def test_invalid_cut_is_rejected() -> None:
    b_graph = nx.path_graph(5)
    report = verify_gamma_instance(b_graph, [(0, 4), (0, 2)])
    assert not report.valid


def test_fixed_b_milp_recovers_path_optimum() -> None:
    b_graph = nx.path_graph(7)
    optimum, chosen = maximize_gamma_for_fixed_b(b_graph)
    assert optimum == 49
    assert chosen == [(0, 6, 6)]


def test_fixed_b_milp_recovers_c5_blowup_gamma() -> None:
    b_graph, expected_m = c5_blowup_cut_instance(2)
    optimum, chosen = maximize_gamma_for_fixed_b(b_graph)
    assert optimum == 100
    assert {(u, v) for u, v, _ in chosen} == set(expected_m)


def test_rejected_tau_strengthening_has_exact_falsifier() -> None:
    report = verify_tau_counterexample()
    assert report.valid
    assert report.gamma == 100 < report.order**2


def test_unicyclic_cactus_instance() -> None:
    b_graph = nx.cycle_graph(8)
    m_edges = [(0, 4)]
    report = verify_gamma_instance(b_graph, m_edges)
    assert report.valid
    assert verify_cactus_proof_certificate(b_graph, m_edges)


def test_two_cycle_cactus_corner() -> None:
    b_graph = nx.Graph()
    b_graph.add_edges_from(
        [(0, 1), (1, 2), (2, 3), (3, 0),
         (0, 4), (4, 5), (5, 6), (6, 0)]
    )
    m_edges = [(2, 5)]
    report = verify_gamma_instance(b_graph, m_edges)
    assert report.valid
    assert verify_cactus_proof_certificate(b_graph, m_edges)
