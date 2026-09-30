# Results and exact scope

[Home](../README.md) · [Model](MODEL.md) · [Proof](PROOF.md) · [Realization](REALIZATION.md)

## Resource-resolved disk

Under the [model](MODEL.md), any finite-dimensional periodic network satisfies

```math
\beta^2\leq(\alpha-1/h)(j-\alpha).
```

In particular $`1/h\leq\alpha\leq j`$. The disk is a statement about two scalar response quantities, not every entry of the full compliance matrix. Its proof is [one weighted projection argument](PROOF.md#weighted-projection).

## Fixed-schedule refinement

For a fixed phase-weighted stiffness schedule, write $`a_{\rm s}=\mathrm{tr}(P^T\overline{K^{-1}}P)/2`$ and $`a_{\rm f}=\mathrm{tr}(P^T(\overline K)^{-1}P)/2`$. The inverse in the second expression is taken after averaging the full stiffness. These are the slow- and fast-modulation direct-response limits with the probe force constant. Then

```math
\beta^2\leq(\alpha-a_{\rm f})(a_{\rm s}-\alpha).
```

Since $`a_{\rm s}=j`$ and $`a_{\rm f}\geq1/h`$, this can be stronger for a specified waveform. A positive endpoint gap is necessary, not sufficient, for nonreciprocity. The [proof and operator comparison](OPERATOR_CONNECTION.md#fixed-schedule-disk) derive the refinement and state its relation to established spectral-response methods. The global stiffness-only ceiling below is unchanged.

## Spectral ceiling

When only the complete stiffness interval $`[m,M]`$ is fixed,

```math
|\beta|\leq B_*,
```

```math
B_*=\frac12\left(\frac1{\sqrt m}-\frac1{\sqrt M}\right)^2.
```

The bound is independent of internal dimension, waveform, and period. It holds for every constant positive symmetric damping matrix. A four-coordinate family with suitable internal drag attains it. Sharpness for each separately fixed anisotropic damping tensor or sparse graph is not claimed.

Writing $`D=mM`$ and $`k=(m+M)/2`$, the spectral response envelope is

```math
(\alpha-k/D)^2+(|\beta|+1/\sqrt D)^2\leq k^2/D^2.
```

The four-coordinate family reaches each nonzero-$`\beta`$ boundary point. Endpoints with $`\beta=0`$ can also be realized statically. No full-tensor realizability statement is inferred from this two-scalar envelope.

## Fixed measured stiffness

If $`h=k`$ is fixed as an additional budget, put $`a=(M-m)/2`$. Then

```math
\beta^2\leq(\alpha-1/k)(k/D-\alpha),
```

```math
|\beta|\leq\frac{a^2}{2kD}.
```

This recovers the planar fixed-trace bound even with arbitrarily many internal coordinates. Uniform planar rotation is an attaining member for scalar damping. A fixed trace of the **whole** network is not a substitute for fixed $`h`$.

## Attaining four-coordinate family

Let $`x,y\in\mathbb R^2`$ be measured and internal coordinates. For $`m<h<M`$, choose

```math
g=m+M-h,\qquad b^2=(M-h)(h-m).
```

Use $`R(t)=\exp(\Omega tJ)`$ and

```math
K(t)=\begin{pmatrix}hI_2&bR(t)\\bR(t)^T&gI_2\end{pmatrix}.
```

Its exact spectrum is $`(m,m,M,M)`$. Take damping $`\mathrm{diag}(\Gamma_x,\gamma_yI_2)`$, with $`\Gamma_x`$ positive symmetric and $`\gamma_y>0`$. The response has the form $`\chi=\mathrm{Re}\,C\,I_2+\mathrm{Im}\,C\,J`$, where

```math
C=\frac{g-i\nu}{D-ih\nu},\qquad \nu=\gamma_y\Omega.
```

For fixed $`h`$, $`|\nu|=D/h`$ maximizes $`|\beta|`$. The global optimum uses

```math
h=\sqrt D,\qquad |\Omega_*|=\sqrt D/\gamma_y.
```

Its positive-orientation response is

```math
\chi_* =\frac{m+M}{2mM}I_2+B_*J.
```

The [realization](REALIZATION.md#stationary-outputs-and-static-loads) derives the exact static load law and modulation-power balance. The measured coordinates are stationary; the internal ones rotate.

## Conditional coordinate minimum

Suppose a network attains $`B_*>0`$, its two measured coordinates are stationary for **every** constant input force, and its constant damping has no measured/internal cross-block. It needs at least two internal coordinates, hence at least four total coordinates. The family above attains that conditional minimum.

This is not a minimum spring count or a prohibition on three-coordinate nonreciprocity. The [proof and suboptimal control](PROOF.md#coordinate-minimum) retain the extra assumptions explicitly.

## Clamped coordinate minimum

For the independently defined clamped response, let $`r`$ be the hidden-coordinate count and $`c_*=(\sqrt M-\sqrt m)^2`$. Then

```math
|\kappa|\leq c_*\min(r,2)/4.
```

Full clamped-ceiling attainment therefore requires at least four total coordinates, and the same architecture with its clamped-optimal allocation attains it. This statement allows constant damping cross-blocks and requires no force-controlled output stationarity. The [rank proof](PORT_WORK.md#four-coordinates-are-necessary-for-clamped-attainment) does not assert that the one-hidden-coordinate bound is sharp.

## Geometry and tolerance

For the worked interval $`[k_0,3k_0]`$, eight strictly positive modulated axial springs and four positive fixed support springs realize the attaining tangent stiffness on ideal perpendicular guides. The proposed layout has fixed rest lengths, no prestress at the reference origin, and no moving guides. Finite-amplitude motion obeys nonlinear spring geometry and is not subject to the original exact linear budget without further analysis.

For the same damping and ports, if $`\widetilde K=K+E`$, $`\|E\|\leq\delta`$, and $`\widetilde K\succeq\widetilde mI>0`$, then

```math
\|\widetilde\chi-\chi\|\leq\frac{\delta}{m\widetilde m}.
```

Relative errors at most $`\varepsilon<1`$ in all positive rank-one spring coefficients give

```math
|\widetilde\beta-\beta|\leq\frac{\varepsilon M}{m^2(1-\varepsilon)}.
```

This is a coefficient-error bound, not tolerance to arbitrary damping, prestress, geometric, or controller errors. The perturbed stiffness spectrum may exceed the original budget. See [the proof](PROOF.md#coefficient-errors).

## Research boundaries

No energy-efficiency optimum, universal inertial response bound, autonomous controller, experimentally measured performance, or universal bulk odd-elasticity theorem is established. A separate [small-mass consistency calculation](PHYSICAL_VALIDITY.md#a-controlled-small-mass-limit) proves stability and convergence for the same construction with scalar mass and drag; it does not extend the overdamped ceiling to finite mass. The [literature comparison](SOURCES.md) identifies inherited inequalities and the remaining realization questions. Evidence for universal statements is the proof, not the size of the numerical test suite.
