#!/usr/bin/env python3
"""Replay the exact falsifier for the rejected component-potential route."""

from __future__ import annotations

import json

from mememathics_erdos23.rejected_tau import (
    TAU_COUNTEREXAMPLE_B_EDGES,
    TAU_COUNTEREXAMPLE_GRAPH6,
    TAU_COUNTEREXAMPLE_M_EDGES,
    verify_tau_counterexample,
)


def main() -> None:
    report = verify_tau_counterexample()
    payload = {
        "statement_refuted": "sum_C tau_C^2 <= 4 N^2",
        "original_gamma_conjecture_refuted": False,
        "order": report.order,
        "b_graph6": TAU_COUNTEREXAMPLE_GRAPH6,
        "b_edges": TAU_COUNTEREXAMPLE_B_EDGES,
        "m_edges": TAU_COUNTEREXAMPLE_M_EDGES,
        "gamma": report.gamma,
        "n_squared": report.order**2,
        "tau_squared": 600,
        "four_n_squared": 4 * report.order**2,
        "valid_gamma_instance": report.valid,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
