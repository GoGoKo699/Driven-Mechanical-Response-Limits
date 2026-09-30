# Finite spring tuning and the cost of weak contrast

[Home](../README.md) · [Spring construction](REALIZATION.md) · [Physical validity](PHYSICAL_VALIDITY.md) · [Capacitive candidate](CAPACITIVE_ACTUATION.md)

The 21:1 connecting-spring range belongs to the worked stiffness contrast of three. It is not necessary for nonzero ideal attainment. Every tuning ratio $`r>1`$ permits a sufficiently small contrast in the same twelve-spring construction, with strictly positive fixed supports. The response becomes quadratically small as the available tuning decreases.

## Exact feasible interval for the existing decomposition

Let $`\mathcal R=M/m>1`$, and use the force-optimal allocation. Then

```math
h=m\sqrt{\mathcal R},\qquad
g=m(1+\mathcal R-\sqrt{\mathcal R}),
```

```math
b=m\mathcal R^{1/4}(\sqrt{\mathcal R}-1),\qquad g\geq h.
```

To keep the connecting-spring ratio at most $`r`$, choose $`\eta=2/(r-1)`$. This is the smallest allowed offset and leaves the largest support margin. Both fixed supports are positive precisely when

```math
\frac hb>\frac32+\frac4{r-1}.
```

Since $`h/b=(\mathcal R^{1/4}-\mathcal R^{-1/4})^{-1}`$, this becomes

```math
1<\mathcal R<\exp\left[4\operatorname{arsinh}
\frac{r-1}{3r+5}\right].
```

The endpoint is excluded because a support vanishes there. This is a criterion for the specified decomposition and allocation, not every possible mechanical network. Exchanging measured and internal allocations gives the same criterion for the clamped-work optimizer.

To reserve a fixed support fraction $`0<\rho<1`$, choose

```math
\mathcal R=\exp\left[4\operatorname{arsinh}
\frac{(1-\rho)(r-1)}{3r+5}\right].
```

The smaller support coefficient is then $`\rho h>0`$, and the other is at least that large. A ratio strictly inside an actuator's attainable interval also leaves tuning margin.

For example, $`r=1.10`$ and $`\rho=1/4`$ give $`\mathcal R=1.036805225`$, connecting coefficients from $`0.368037228m`$ to $`0.404840951m`$, and

```math
mB_*=0.0001603791.
```

These are dimensionless design parameters, not measured actuator performance. A ratio check does not replace matching the absolute stiffness interval or the actuation dynamics.

## What the smaller tuning range costs

For $`\delta=\mathcal R-1\to0`$,

```math
B_*=\frac1{2m}\left(1-\frac1{\sqrt{1+\delta}}\right)^2
=\frac{\delta^2}{8m}+O(\delta^3/m).
```

The relative cross-response at this optimum is also quadratic:

```math
\frac{B_*}{\alpha_*}
=\frac{(\sqrt{\mathcal R}-1)^2}{1+\mathcal R}
=\frac{\delta^2}{8}+O(\delta^3).
```

With $`\epsilon=r-1\to0`$, the contrast supremum is $`1+\epsilon/2+O(\epsilon^2)`$, so the supremal $`mB_*`$ is $`\epsilon^2/32+O(\epsilon^3)`$. A support reserve multiplies the leading coefficient by $`(1-\rho)^2`$. The connecting coefficients themselves approach $`(1-\rho)m/2`$; this is weak modulation around finite positive springs, not a vanishing-support construction.

Uniform softening can increase displacement per force but does not improve the relative response. Finite tuning therefore removes one algebraic implementation obstacle while providing no automatic advantage in signal size, precision, efficiency, or robustness. In particular it does not repair the [charge-leakage obstruction](CAPACITIVE_ACTUATION.md#three-line-proof-of-reciprocal-mean-response).
