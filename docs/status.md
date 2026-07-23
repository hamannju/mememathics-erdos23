# Research status — 2026-07-23

Erdős Problem #23 remains open in the current public problem database. Ferudun's
June 2026 result proves the sharp value for `N=5,10,...,200`; it is a finite
computer-assisted theorem and not an all-order result.

## Completed in this repository

- Exact finite-instance validation of the connected maximum-cut Gamma setup.
- Fixed-`B` MILP with every cut constraint and explicit triangle constraints.
- Proof of `Gamma <= N²` when `B` is a tree.
- Proof of `Gamma <= N²` when `B` is any connected bipartite cactus.
- Exhaustive Graph Atlas audit for all 72 connected bipartite graphs through
  seven vertices. The largest ratios are the sharp path instances `P5` and
  `P7`, with `Gamma=N²`; no violation occurs.
- Sharp `C5`-blow-up and path regressions.
- Exact 12-vertex falsifier for the rejected component-potential square bound.
- Audit of the prior Ferudun/Fable/Lean campaign and its exact restart boundary.

## Exact remaining wall

The strongest prior campaign already built the downstream algebra and Lean
interfaces for a global length-surplus accounting certificate. It did not prove
that such a certificate exists for every graph. The shortest honest statement
of the remaining task is:

> Construct the real graph-derived full-bank provider, including globally
> consistent incidence, no double spending, component reserve identities, and
> global superadditivity; or prove the equivalent closed-shore plus restricted-
> Farkas route.

The prior handoff explicitly records that the full conjecture remains open and
that no unconditional top-level Lean theorem exists.

## Not completed

- The general connected-`B` Gamma transfer.
- The graph-derived full-bank provider or equivalent restricted-Farkas bridge.
- A proof-producing certificate pipeline for large MaxCut instances.
- A complete proof or finite counterexample to Erdős #23.

## Current research targets

1. Reconstruct the missing provider at the level of exact graph incidence,
   starting from the equality examples and the finite chart certificates.
2. Extend the cactus cut decomposition to controlled overlapping-cycle blocks
   and partial-cube blocks.
3. Continue falsifier-first testing of every proposed transfer lemma before any
   formalization effort.
