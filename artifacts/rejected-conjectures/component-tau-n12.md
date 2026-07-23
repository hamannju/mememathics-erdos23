# Exact falsifier: component-potential square bound

This artifact refutes the proposed sufficient strengthening

\[
\sum_C \tau_C^2 \le 4N^2,
\]

not the Gamma inequality and not Erdős Problem #23.

## Instance

`N = 12`. The connected bipartite graph `B` has graph6 string

```text
K??DDoWhFOG_
```

and edges

```text
(0,6) (0,7) (0,9) (0,10)
(1,10) (1,11)
(2,6) (2,7) (2,9) (2,10)
(3,7) (3,8)
(4,7) (4,8) (4,10)
(5,9) (5,11)
```

The monochromatic graph `M` has edges

```text
(6,8) (6,11) (7,11) (8,9)
```

and is the path `9-8-6-11-7`.

The independent instance verifier confirms:

- `B` connected and bipartite;
- `B union M` triangle-free;
- every cut satisfies `|delta_M(S)| <= |delta_B(S)|`;
- all four `M` edges have `B`-distance four;
- `Gamma = 4*25 = 100 <= 12^2 = 144`.

For the sole `M` component, the product constraints are `x_u*x_v >= 25`
on the four edges of `P5`. By reflection symmetry the optimum has objective

\[
3\frac{25}{q}+2q,
\]

whose minimum occurs at `q^2=75/2`. Therefore

\[
\tau=10\sqrt6,\qquad \tau^2=600>4N^2=576.
\]

Replay:

```bash
PYTHONPATH=src python scripts/verify_tau_counterexample.py
```
