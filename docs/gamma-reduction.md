# The maximum-cut Gamma reduction

Let `G` be triangle-free and fix a maximum cut `(X,Y)`.

- `B` is the bipartite graph formed by the crossing edges.
- `M` is the graph formed by the monochromatic edges inside `X` and inside `Y`.
- `|M| = beta(G)` for this maximum cut.

Flipping any vertex subset `S` cannot improve the cut. Hence every cut obeys

\[
|\delta_M(S)|\leq |\delta_B(S)|. \tag{1}
\]

Assume first that `B` is connected. Every `uv in M` lies in one bipartition
class of `B`, so `d_B(u,v)` is even. Triangle-freeness excludes `d_B(u,v)=2`.
Thus every such distance is at least four.

Define

\[
\Gamma(B,M)=\sum_{uv\in M}\bigl(d_B(u,v)+1\bigr)^2. \tag{2}
\]

The desired connected transfer is

\[
\Gamma(B,M)\leq N^2. \tag{3}
\]

Because every summand in (2) is at least `25`, (3) implies

\[
25|M|\leq N^2,
\]

which is Erdős #23.

The constraints implemented by `verify_gamma_instance` are exactly the finite
hypotheses above: connected bipartite `B`, simple `M`, triangle-free `B union M`,
and all inequalities (1).

## Sharp examples

1. Let `B=P_N` for odd `N>=5`, and let `M` contain the edge between the two
   endpoints. Then `d_B=N-1` and `Gamma=N²`.
2. In a maximum-cut decomposition of the balanced blow-up `C5[q]`, `B` is a
   five-layer path blow-up and `M` is complete bipartite between the endpoint
   layers. Every bad edge has distance four and
   `Gamma=25q²=(5q)²`.

Any proposed global inequality must therefore preserve both equality families.
