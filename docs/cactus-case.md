# Proven subclass: the crossing graph B is a bipartite cactus

## Theorem

Let `B` be a connected bipartite cactus on `N` vertices and let `M` be the
monochromatic graph of a maximum cut. Assume `B union M` is triangle-free.
Then

\[
\Gamma(B,M)=\sum_{uv\in M}(d_B(u,v)+1)^2\leq N^2.
\]

Consequently Erdős #23 holds whenever a maximum cut has a cactus as its
crossing graph. This includes the previously recorded tree case.

## 1. Exact cut decomposition of the cactus metric

Let `q` be the number of cycle blocks of `B`. Every cycle block is even.

- Each bridge `e` gives a fundamental cut with `B`-capacity one.
- If a cycle block has length `2r`, its `r` pairs of antipodal edges give `r`
  cuts, each with `B`-capacity two.

For an even cycle, the distance between two vertices equals the number of these
antipodal-edge cuts that separate them. The block tree of a cactus therefore
gives, for every pair `x,y`,

\[
d_B(x,y)=
\sum_{e\text{ bridge}}1_{e\text{ separates }x,y}
+
\sum_{C}\sum_{j=1}^{|C|/2}1_{S_{C,j}\text{ separates }x,y}.
\]

The maximum-cut inequalities say

\[
|\delta_M(S)|\leq|\delta_B(S)|
\]

for every vertex set `S`. Summing them over the metric cuts above yields

\[
D:=\sum_{uv\in M}d_B(u,v)
\leq
\#\{\text{bridges}\}+\sum_C |C|
=|E(B)|=N-1+q. \tag{1}
\]

## 2. Diameter and topology bounds

A shortest path uses at most half of the edges of each even cycle. Since the
cycle edge sets of a cactus are disjoint,

\[
d_B(x,y)\leq |E(B)|-2q=N-1-q. \tag{2}
\]

Also every cycle has length at least four, so

\[
N\geq3q+1. \tag{3}
\]

Every `M` edge joins vertices in one bipartition class, hence has even
`B`-distance. Distance two would create a triangle with the `M` edge, so every
such distance `d_i` is an even integer at least four.

## 3. Scalar completion

Write `k=|M|`, `S=N-1+q`, and `L=N-1-q`. From (1)--(3),

\[
\sum_i d_i\leq S,\qquad 4\leq d_i\leq L.
\]

First,

\[
\Gamma=\sum_i d_i^2+2\sum_i d_i+k
\leq (L+2)S+k
=N^2-(q-1)^2+k. \tag{4}
\]

Thus (4) proves the result whenever `k <= (q-1)^2`.

Otherwise every `d_i` also satisfies

\[
d_i\leq S-4(k-1),
\]

because the other `k-1` distances are at least four. Hence

\[
\Gamma\leq(S-4k+6)S+k. \tag{5}
\]

For `q>=3`, the right-hand side of (5) decreases with `k`, so it is enough to
put `k=(q-1)^2+1`. It also decreases with `N`; using `N>=3q+1`, its excess over
`N^2` is at most

\[
-16q^3+40q^2-16q+1
=-8q^2(2q-5)-16q+1<0.
\]

For `q=1`, (1) gives `sum d_i<=N` and (2) gives `d_i<=N-2`. One edge is
strictly below `N^2`; for at least two edges, concentration at the largest
entry gives

\[
\Gamma\leq N^2+(6-4k)N+k<N^2.
\]

For `q=2`, (4) handles `k<=1`, and (5) handles `k>=3`. If `k=2`, parity and
convexity give

\[
\Gamma\leq
\begin{cases}
(N-3)^2+25,&N\text{ even},\\
(N-2)^2+25,&N\text{ odd}.
\end{cases}
\]

This is at most `N^2` except for the formal parameter corner `N=7`. In that
corner `B` is necessarily two 4-cycles sharing one vertex. It has only one
same-side vertex pair at distance at least four, so a simple `M` cannot have
`k=2`.

The tree case `q=0` is proved separately in [`tree-case.md`](tree-case.md).

## Computational audit

`verify_cactus_proof_certificate` recomputes the graph hypotheses, cactus block
structure, distance bounds and scalar inequality for concrete instances. A
falsifier-first sample of 300 random even cacti through 15 vertices, with the
fixed-`B` MILP choosing the worst valid `M`, found no violation. This sampling
is regression evidence; the proof above is the theorem.
