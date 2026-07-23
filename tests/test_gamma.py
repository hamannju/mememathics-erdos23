import networkx as nx

from mememathics_erdos23.gamma import (
    c5_blowup_cut_instance,
    maximize_gamma_for_fixed_b,
    path_closure_instance,
    verify_gamma_instance,
)
from mememathics_erdos23.tree_case import verify_tree_proof_certificate


def test_path_closure_is_sharp_at_five() -> None:
    b_graph, m_edges = path_closure_instance(5)
    report = verify_gamma_instance(b_graph, m_edges)
    assert report.valid
    assert report.gamma == 25 == report.order**2
    assert verify_tree_proof_certificate(b_graph, m_edges)


def test_path_closure_is_sharp_at_seven() -> None:
    b_graph, m_edges = path_closure_instance(7)
    report = verify_gamma_instance(b_graph, m_edges)
    assert report.valid
    assert report.gamma == 49 == report.order**2
    assert verify_tree_proof_certificate(b_graph, m_edges)


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
