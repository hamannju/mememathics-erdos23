# Approach registry

## Active

### Connected-B Gamma transfer

Target:

\[
\sum_{uv\in M}(d_B(u,v)+1)^2\leq N^2
\]

under connected bipartite `B`, triangle-free `B union M`, and all maximum-cut
constraints `|delta_M(S)| <= |delta_B(S)|`.

Current proved base:

- tree `B`;
- bipartite cactus `B`, including arbitrary collections of edge-disjoint even
  cycle blocks;
- sharp path and `C5`-blow-up equality regressions.

Finite evidence:

- all connected bipartite Graph Atlas graphs through seven vertices: exact
  fixed-`B` MILP audit.

### Graph-derived full-bank provider

Ferudun's 2026 proof campaign reduced the remaining all-order problem to a
concrete global accounting object. Two equivalent implementation routes remain:

1. instantiate the closed-shore/allowed-cut interface and prove weighted Hall
   completeness, positive root-block extraction, the root-cut exchange, and a
   restricted rational Farkas bridge; or
2. construct a checked `FullBankGlobalPackage` directly, with graph-derived
   incidence, globally unique token sources, no double spend, component reserve
   identities, and global superadditivity.

Downstream package consumers already exist in that development. The missing
content is the provider itself; aggregate token counts or a local cover do not
suffice.

### Cut-metric dual route

The maximum-cut condition is a family of cut-capacity inequalities. A possible
proof would construct an `M`-dependent nonnegative combination of cuts whose
induced L1 metric dominates `(d_B+1)^2` on every `M` edge while its total cost on
`B` is at most `N²`. The cactus proof is an exact instance of this strategy:
bridges and antipodal cuts of even cycle blocks reproduce the graph metric.

### Structural subclasses

Extend the cactus theorem to crossing graphs with overlapping even cycles,
partial-cube blocks, or bounded treewidth. A valid block theorem should expose
the precise reserve term needed when the exact cactus cut decomposition fails.

## Blocked by exact counterexample or prior audit

### Component potential / Motzkin-Straus square bound

The proposed sufficient inequality

\[
\sum_C\tau_C^2\leq4N^2
\]

is false. An exact 12-vertex instance has valid `B,M`, `Gamma=100<=144`, but one
`P5` component has `tau=10*sqrt(6)` and `tau²=600>576`. See
[`../artifacts/rejected-conjectures/component-tau-n12.md`](../artifacts/rejected-conjectures/component-tau-n12.md).

### Other blocked routes

- Universal fractional demand LP without the simplicity bounds `x_e <= 1`.
- A general implication from the cut condition to congestion-one fractional
  multicommodity routing.
- Packing one distribution of shortest paths so that every ordered vertex pair
  has occupancy at most one.
- Bare shortest-geodesic Hall/SSE: an infinite family with unique maximum cuts
  violates it by an unbounded factor.
- The previously proposed R55/R57 branch-to-prefix extraction interface: a
  finite graph and an abstract positive-defect model invalidate it.
- Aggregate local capacity counts without an injective graph-incidence map.
- Treating a downstream checked-package consumer as an existence proof for the
  package.
- Several component-diameter and local degree-distance inequalities.

These failures are retained to prevent future agents from repeatedly pursuing
invalid strengthenings.
