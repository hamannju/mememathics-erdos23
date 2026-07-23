# A general cut-metric criterion

Let `B,M` satisfy the connected Gamma hypotheses. Suppose there are vertex cuts
`S_j` with nonnegative rational weights `lambda_j` such that every `M` edge
`uv` satisfies

\[
d_B(u,v)\leq\sum_j\lambda_j\,1_{S_j\text{ separates }u,v}. \tag{1}
\]

Set

\[
C=\sum_j\lambda_j|\delta_B(S_j)|.
\]

The maximum-cut inequalities and (1) give

\[
\sum_{uv\in M}d_B(u,v)
\leq\sum_j\lambda_j|\delta_M(S_j)|
\leq C. \tag{2}
\]

Let `Delta=diam(B)` and `k=|M|`. Since every `M` distance is at least four,
`k<=C/4`. Therefore

\[
\begin{aligned}
\Gamma
&=\sum_{uv\in M}(d_B(u,v)+1)^2\\
&\leq(\Delta+2)\sum_{uv\in M}d_B(u,v)+k\\
&\leq C\left(\Delta+\frac94\right).
\end{aligned}
\]

This proves the Gamma inequality whenever

\[
C(4\Delta+9)\leq4N^2. \tag{3}
\]

## Partial cubes

If `B` is a partial cube, its Djoković-Winkler/Theta classes give convex cuts
whose boundaries partition `E(B)`, and graph distance is exactly the number of
Theta cuts separating two vertices. Thus (1) holds with unit weights and

\[
C=|E(B)|.
\]

Consequently every partial-cube crossing graph satisfying

\[
|E(B)|(4\,\mathrm{diam}(B)+9)\leq4N^2
\]

obeys the Gamma inequality. This includes, for example, hypercubes `Q_d` for
`d>=3` and many Cartesian grids. The sharp long-path cases fall just outside
the generic diameter estimate and are covered by the stronger tree theorem.

`verify_cut_metric_certificate` checks rational finite certificates of this
form. The criterion is sufficient, not necessary.
