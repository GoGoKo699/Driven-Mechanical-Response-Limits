# Physical validity of the attaining construction

[Home](../README.md) · [Model](MODEL.md) · [Realization](REALIZATION.md) · [Research status](RESEARCH_STATUS.md)

The four-coordinate design is an exact ideal tangent realization. This note makes two physical requirements quantitative: small inertia at the chosen pump rate, and the tuning range of the existing eight connecting springs. It does not specify a fabricated actuator.

## A controlled small-mass limit

For this check alone, give every retained coordinate the same mass $`\mu>0`$ and drag $`\gamma>0`$:

```math
\mu\ddot q+\gamma\dot q+K(t)q=PF.
```

The main response theorem remains overdamped. Here $`K(t)`$ has the same fixed origin, reciprocal symmetry, and bounds $`mI\preceq K(t)\preceq MI`$. Equal scalar mass and drag are additional assumptions of this check.

For a homogeneous difference of two trajectories, put

```math
z=q+(\mu/\gamma)\dot q,\qquad w=(\mu/\gamma)\dot q,
```

```math
V=\tfrac12(\|z\|^2+\|w\|^2).
```

Direct differentiation, using symmetry of $`K`$, cancels the cross terms:

```math
\dot V=-\frac1\gamma z^TKz
-w^T\left(\frac\gamma\mu I-\frac K\gamma\right)w.
```

Consequently, if

```math
\mu M<\gamma^2,
```

then $`\dot V\leq-2cV`$, with

```math
c=\min\{m/\gamma,\ \gamma/\mu-M/\gamma\}>0.
```

This is a sufficient condition, not a necessary stability threshold. It works for bounded measurable stiffness schedules and needs no bound on $`\dot K`$. For periodic coefficients it gives a unique attracting periodic forced response. The quadratic form is a stability certificate, not the physical stored energy; its norm equivalence to position and velocity is for each fixed positive mass.

## Exact response of the same rotating family

Keep the original force-optimal allocation and pump rate:

```math
D=mM,\quad h=\sqrt D,\quad g=m+M-h,
```

```math
b^2=(M-h)(h-m),\qquad \Omega=\sqrt D/\gamma.
```

There is an exact solution with constant measured $`x`$ and $`y(t)=R(\Omega t)^Tw_0`$. Since $`\dot y=-\Omega Jy`$ and $`\ddot y=-\Omega^2y`$, its equations are

```math
hx+bw_0=F,
```

```math
bx+[(g-\mu\Omega^2)I-\gamma\Omega J]w_0=0.
```

The stability condition makes this the attracting response. Identifying $`J`$ with $`i`$ gives $`\chi_\mu=\operatorname{Re}C_\mu I+\operatorname{Im}C_\mu J`$, where

```math
C_\mu=\frac{g-\mu\Omega^2-i\gamma\Omega}
{D-h\mu\Omega^2-ih\gamma\Omega}.
```

Define the ratio of momentum-relaxation time to the angular pump time $`1/\Omega`$,

```math
\varepsilon=\frac{\mu\Omega}{\gamma}
=\frac{\mu\sqrt D}{\gamma^2}.
```

The sufficient stability condition is $`\varepsilon<\sqrt{m/M}`$. At the same pump rate, exact subtraction from the overdamped response gives

```math
\frac{\beta_\mu}{B_*}=\frac{2}{(1-\varepsilon)^2+1},
```

```math
\|\chi_\mu-\chi_0\|_2
=\frac{\sqrt2 B_*\varepsilon}{\sqrt{(1-\varepsilon)^2+1}}
\leq\sqrt2 B_*\varepsilon.
```

Thus the constructed response converges regularly as inertia becomes small. It does not require a resonance or an unstable limit. In the stable interval, finite mass increases $`\beta`$ above the exact overdamped ceiling; the increase is small when $`\varepsilon`$ is small. This explicitly demonstrates why that ceiling must retain its overdamped hypothesis. No optimum over inertial networks is claimed.

For fixed mass and stiffness, larger scalar drag lowers both $`\varepsilon`$ and the chosen pump rate. Whether an apparatus permits that drag adjustment while preserving its other constitutive assumptions is a separate physical question. The mass calculation does not certify the actuator or hydrodynamic model.

## The existing spring schedule requires a large tuning range

Each connecting spring in the [specified quadratic decomposition](REALIZATION.md#twelve-strictly-positive-spring-coefficients) traverses

```math
\kappa_{\min}=b\eta,\qquad \kappa_{\max}=b(2+\eta).
```

Its required stiffness ratio is therefore

```math
r_\kappa=1+2/\eta.
```

Strictly positive fixed support springs require

```math
0<\eta<\tfrac12[\min(h,g)/b-3/2].
```

Within this particular decomposition, whenever its right side is positive,

```math
r_\kappa>1+\frac4{\min(h,g)/b-3/2}.
```

For the worked $`[k_0,3k_0]`$ force and clamped-work allocations, this strict lower limit is $`14.4322604`$. It is an infimum approached as a support coefficient tends to zero. The chosen $`\eta=0.1`$ requires a ratio of **21**. The balanced allocation has different support margins and is not assigned this same infimum. The connecting coefficients contain temporal harmonics through $`2\Omega`$.

These are requirements of the current construction, not universal lower bounds on actuators or alternative spring decompositions. They also distinguish the full-network spectral contrast of three from the individual spring tuning ratio of twenty-one.

The [finite-tuning analysis](TUNING_RANGE.md) gives the exact smaller-contrast interval attainable with any connecting-spring ratio $`r>1`$ in this same decomposition, including a finite support reserve. The resulting relative nonreciprocity shrinks quadratically with weak tuning.

## What the experimental precedents support

Martínez et al. [R6](SOURCES.md#r6) implement an overdamped optical confinement whose stiffness is controlled by laser power while its mean center stays fixed. The full published text reports a transient peak of $`37`$ times the initial stiffness. That supports large-range scalar confinement, not an eight-coupling spring network.

Trainiti et al. [R7](SOURCES.md#r7) implement switched piezoelectric shunts: the inspected experimental description reports about a 14% reduction of effective beam bending stiffness, with electrical stabilization. This supports physical stiffness modulation but does not supply the required continuous 21:1 connecting-spring law or prove constant damping.

The [full-text assumption map](SOURCES.md#full-text-primitive-check) supports harmonic control and local drag as established primitives. A complete device needs an elastic-element model covering the required tuning range and harmonics, residual force at zero extension, damping changes, and retained actuator states. Finite guide/support compliance must also be counted if appreciable. Component precedents cannot be combined into an unmeasured device performance claim.

One concrete candidate has now been resolved: a [positive capacitive piezoelectric shunt](CAPACITIVE_ACTUATION.md) gives the intended ideal law in an isolated zero-charge sector, but fixed nonzero leakage makes its attracting DC response reciprocal. This candidate does not certify the proposed mechanical device. Small-mass convergence and finite tuning do not remove that electrical obstruction.

## Verification

Run `python checks/finite_mass.py --output finite-mass.local.json`. The independent laboratory-frame integrations start from rest, apply the two constant force directions, and check the exact stationary port response, rotating hidden response, and small-mass convergence. A separate calculation checks the Lyapunov identity. The proof above, rather than those finite cases, establishes stability under the stated condition.
