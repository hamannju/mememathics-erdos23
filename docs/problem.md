# Problem specification

For a finite simple graph `G`, let

\[
\beta(G)=\min\{|F|:G-F\text{ is bipartite}\}
        =|E(G)|-\operatorname{MaxCut}(G).
\]

Erdős Problem #23 asks whether every triangle-free graph on `N` vertices
satisfies

\[
\beta(G)\leq \frac{N^2}{25}.
\]

For `N=5n`, this is the historical form `beta(G) <= n²`. The constant is
sharp: the balanced blow-up `C5[n]` has `5n` vertices and bipartization number
`n²`.

The best published general bound currently cited by the Erdős Problems
database is `N²/23.5`, due to Balogh, Clemen and Lidický. They also prove the
sharp conjectured bound in the two graphon-density tails. Ferudun's June 2026
computer-assisted preprint proves the exact result for multiples of five
through `N=200` and isolates the connected maximum-cut transfer described in
[`gamma-reduction.md`](gamma-reduction.md).

## Falsification target

A finite counterexample consists of a triangle-free graph `G` satisfying

\[
25\bigl(|E(G)|-\operatorname{MaxCut}(G)\bigr)>|V(G)|^2.
\]

The difficult certificate is the upper bound on `MaxCut(G)`. A large candidate
must be accompanied by a proof-producing pseudo-Boolean or SAT run and a
separately checked proof log.
