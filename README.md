# mememathics-erdos23

Reproducible computational and proof-oriented work on **Erdős Problem #23**:

> Can every triangle-free graph on `N` vertices be made bipartite by deleting at most `N²/25` edges?

For a graph `G`, write

```text
beta(G) = |E(G)| - MaxCut(G).
```

The conjecture is `25 * beta(G) <= |V(G)|²`. The balanced blow-up of `C5`
attains equality.

## Current result

No complete proof or counterexample is claimed.

The repository currently contains:

- an exact verifier for the maximum-cut `Gamma` reduction;
- a fixed-`B` MILP that adversarially maximises `Gamma` over all simple,
  triangle-free monochromatic edge sets satisfying every maximum-cut
  inequality;
- a complete proof and mechanical certificate checker for the case where the
  crossing graph `B` is a tree;
- sharp regression instances: odd paths closed by one monochromatic edge and
  maximum-cut decompositions of balanced `C5` blow-ups;
- a frozen exhaustive Graph Atlas run for connected bipartite `B` through
  seven vertices.

The mathematical status and trust boundary are recorded in
[`docs/status.md`](docs/status.md).

## Install and test

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]' --no-build-isolation
pytest
```

## Reproduce the finite `Gamma` audit

```bash
PYTHONPATH=src python scripts/enumerate_atlas_gamma.py \
  --maximum-order 7 \
  --output runs/2026-07-23-gamma/atlas-bipartite-n7.json
```

## Maximum-cut `Gamma` reduction

Fix a maximum cut of a triangle-free graph `G`. Let `B` contain the crossing
edges and `M` the monochromatic edges. For connected `B`, define

```text
Gamma(B, M) = sum_{uv in M} (dist_B(u, v) + 1)^2.
```

Every `M` edge has even `B`-distance at least four. Therefore
`Gamma <= N²` would imply `25 * |M| <= N²`, which is the conjectured bound.
The general connected-`B` transfer is open. See
[`docs/gamma-reduction.md`](docs/gamma-reduction.md).

## Verification policy

A numerical optimiser, heuristic cut, or solver status is not a proof. A
counterexample claim requires a canonical graph, independent triangle-free
checks, exact arithmetic, and a checked proof-producing MaxCut/PB/SAT
certificate. A proof claim must expose every external theorem and all
computer-assisted leaves. See [`docs/trust-model.md`](docs/trust-model.md).

## References

- Thomas Bloom, [Erdős Problem #23](https://www.erdosproblems.com/23).
- J. Balogh, F. C. Clemen, B. Lidický,
  [Max Cuts in Triangle-Free Graphs](https://arxiv.org/abs/2103.14179), 2021.
- A. Ferudun,
  [The Erdős n²/25 max-cut conjecture for small multiples of five](https://arxiv.org/abs/2606.28041), 2026.
- OEIS [A389646](https://oeis.org/A389646).
