# Proven subclass: the crossing graph B is a tree

## Theorem

Let `B` be a tree on `N` vertices and let `M` be a simple graph on the same
vertices. Suppose every cut satisfies

\[
|\delta_M(S)|\leq |\delta_B(S)|.
\]

Then

\[
\sum_{uv\in M}\bigl(d_B(u,v)+1\bigr)^2\leq N^2.
\]

Consequently the Gamma transfer, and hence Erdős #23, holds whenever a maximum
cut has a tree as its crossing graph.

## Proof

For an edge `f` of the tree, deleting `f` produces a fundamental cut `S_f` with

\[
|\delta_B(S_f)|=1.
\]

An `M` edge crosses this cut exactly when its unique `B`-path uses `f`.
Therefore the cut hypothesis implies that at most one `M`-path uses each tree
edge. The unique paths are edge-disjoint, and hence

\[
\sum_{uv\in M} d_B(u,v)\leq |E(B)|=N-1. \tag{1}
\]

For every integer `1 <= d <= N-1`,

\[
\frac{(d+1)^2}{d}=d+2+\frac1d
\leq N+1+\frac1{N-1}
=\frac{N^2}{N-1}. \tag{2}
\]

Combining (1) and (2),

\[
\begin{aligned}
\Gamma
&=\sum_{uv\in M}d_B(u,v)
  \frac{(d_B(u,v)+1)^2}{d_B(u,v)}\\
&\leq \frac{N^2}{N-1}
  \sum_{uv\in M}d_B(u,v)\\
&\leq N^2.
\end{aligned}
\]

Equality is attained when `B=P_N` for odd `N` and `M` consists of the endpoint
edge.

## Mechanical audit

`verify_tree_proof_certificate` checks the finite hypotheses, path loads,
distance sum and final inequality for concrete instances. The function is a
regression checker, not a replacement for the proof above.
