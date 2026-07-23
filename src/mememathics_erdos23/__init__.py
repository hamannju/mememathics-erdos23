"""Exact and auditable helpers for Erdős Problem #23."""

from .gamma import (
    GammaInstanceReport,
    candidate_bad_edges,
    gamma_value,
    maximum_cut_decomposition,
    maximize_gamma_for_fixed_b,
    verify_gamma_instance,
)

__all__ = [
    "GammaInstanceReport",
    "candidate_bad_edges",
    "gamma_value",
    "maximum_cut_decomposition",
    "maximize_gamma_for_fixed_b",
    "verify_gamma_instance",
]
