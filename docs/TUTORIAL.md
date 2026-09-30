# From odd elasticity to a driven reciprocal element

[Home](../README.md) · [Model](MODEL.md) · [Results](RESULTS.md) · [Background and citations](MANUSCRIPT_BACKGROUND.md)

## A finite-dimensional dictionary

Start with two measured sliders and any number of hidden coordinates. A **port** pairs a displacement with the force that does work through it. Our variables translate the review's constitutive language into this finite mechanical setting:

| Symbol | Physical meaning |
|---|---|
| $`q`$ | All retained mechanical displacements, including hidden ones |
| $`x=P^Tq`$, $`F`$ | Two measured displacements and their conjugate applied forces; input power is $`F^T\dot x`$ |
| $`K(t)`$ | Instantaneous stiffness of the complete network; the energy Hessian |
| $`\chi`$ | Mean displacement per constant applied force while modulation continues |
| $`G`$ | Mean applied force per displacement held fixed while modulation continues |

The symmetric and skew parts of any real response matrix are

```math
\mathrm{Sym}\,Q=\frac{Q+Q^T}{2},\qquad
\mathrm{Skew}\,Q=\frac{Q-Q^T}{2}.
```

Exchange asymmetry means that exchanging the forcing and measurement directions changes the response. A sideways displacement by itself is insufficient: ordinary anisotropic springs can produce one.

Stress and strain play analogous conjugate roles in the review. Our two-port matrix is a finite constitutive element, however; identifying a bulk elastic tensor would require additional modeling. A skew response matrix is also different from an antisymmetric stress tensor.

The selected anchor is Fruchart, Scheibner, and Vitelli, [*Odd Viscosity and Odd Elasticity*](https://doi.org/10.1146/annurev-conmatphys-040821-125506), Annual Review of Condensed Matter Physics **14**, 471–510 (2023). In its **published** pagination, read §1, p. 472; §2.1, p. 473; and Table 1, p. 474 for the vocabulary. Then read §§3.1–3.2.2, pp. 487–490, and §§3.3.1–3.3.3, pp. 491–494 for odd response, reciprocity, and work. The hinge and beam examples in §§3.4.4–3.4.5, pp. 497–498 connect these ideas to coupled mechanical coordinates. The [source guide](TUTORIAL_OPTIONS.md) records version and access details.

## Two experiments while the pump keeps running

A static positive symmetric stiffness gives reciprocal compliance because its inverse is symmetric. The present device instead obeys

```math
\Gamma\dot q+K(t)q=PF.
```

The damping $`\Gamma`$ is constant, symmetric, and positive definite. The prescribed stiffness schedule repeats around a fixed equilibrium; the force $`F`$ stays constant. Drag lets the trajectory retain information about earlier configurations. Averaging the dynamics therefore does not generally amount to inverting an averaged stiffness. Uniform positivity gives a unique attracting periodic response, so measurements are taken after transients.

In the **force experiment**, impose each constant force and average the measured displacement. In the **clamped experiment**, hold each measured displacement fixed and average the force needed to hold it:

```math
\overline x=\chi F,\qquad \overline F=Gx.
```

The bar denotes a pump-period average. These constraints produce different hidden trajectories, so generally $`G\ne\chi^{-1}`$. For example, a rotating two-coordinate trap can have asymmetric mean force compliance. Clamp both coordinates, and its mean reaction is simply the symmetric matrix $`\overline K`$.

The **pump** is the continuing stiffness modulation. A later, slow **probe cycle** moves the measured coordinates through a displacement loop. Its frequency is separate from the pump frequency. “DC response” here means a constant probe, not a stopped pump. Ordinary symmetric drag is not the review's odd viscosity.

## Count the whole mechanical resource

The comparison holds every instantaneous stiffness eigenvalue within one interval:

```math
0<mI\preceq K(t)\preceq MI,\qquad m<M.
```

This includes hidden coordinates. Adding a very soft internal mode or changing a lever normalization changes the resource. The port directions are fixed and normalized, $`P^TP=I_2`$, with conjugate forces; rescaling displacement alone is not a free improvement.

The theorem permits arbitrary finite dimension, period, and waveform within the [declared model](MODEL.md). It does not impose a control-power or bandwidth limit. Fixing the full spectrum also leaves freedom to allocate stiffness between measured and hidden directions. Fix that measured allocation separately, and the [more restrictive bound](RESULTS.md#fixed-measured-stiffness) applies.

## Why a short projection argument gives a universal bound

Separate the direct and exchanged force responses using

```math
\alpha=\tfrac12\,\mathrm{tr}\,\chi,\qquad
\beta=\tfrac12(\chi_{21}-\chi_{12}).
```

The proof combines the two real force experiments into one complex vector. This is bookkeeping for spatial directions, not an oscillating force or a temporal phase lag.

Two averaged identities do the work: force balance and a quadratic identity obtained by multiplying the equation by the displacement. Constant symmetric damping makes its contribution to the latter a periodic boundary term. The physical power balance instead uses velocity and retains viscous loss, as shown below. Measure trajectory lengths using the stiffness-weighted inner product, then compare the actual response with a constant reference and a frozen static response. Cauchy–Schwarz gives

```math
\beta^2\leq(\alpha-1/h)(j-\alpha).
```

Here $`h=\overline{\mathrm{tr}(P^TKP)}/2`$ measures allocated stiffness, while $`j=\overline{\mathrm{tr}(P^TK^{-1}P)}/2`$ uses the inverse of the **complete** stiffness. A scalar inverse bound on $`[m,M]`$ removes waveform details; optimizing over $`h`$ gives the global ceiling below.

The [short proof](PROOF.md#weighted-projection) supplies every algebraic step. Its [operator comparison](OPERATOR_CONNECTION.md#the-exact-inverse-gap-constants-are-established) credits the established resolvent geometry and exact inverse-gap constants. The mechanical question is whether admissible springs can attain the bound.

## A rotating hidden plane attains equality

Use two measured coordinates $`x`$ and two hidden coordinates $`y`$. Their coupling rotates, while the guides remain fixed:

```math
K(t)=\begin{pmatrix}
hI_2&bR(t)\\
bR(t)^T&gI_2
\end{pmatrix},\qquad R(t)=e^{\Omega tJ},
```

where $`J_{12}=-1`$, $`J_{21}=1`$, and its diagonal entries vanish. Choose

```math
g=m+M-h,\qquad b^2=(M-h)(h-m).
```

For $`m<h<M`$, the spectrum is exactly $`(m,m,M,M)`$ throughout the cycle. Reciprocal coupling appears in transposed blocks; no instantaneous odd spring is inserted.

Take block-diagonal damping with scalar hidden drag $`\gamma_yI_2`$. In the calculated variable $`w=Ry`$, the equations have constant coefficients. Their attracting constant-force solution has constant $`x,w`$, although $`y`$ continues to rotate. Thus the internal motion produces an odd measured response while the measured outputs remain stationary.

This property makes clamping and force control agree for this family: $`G=\chi^{-1}`$. A static positive-semidefinite symmetric spring load $`L`$ attached only at these ports gives exactly $`\chi_L=(G+L)^{-1}`$. Generic devices with port motion require their full trajectories. The [construction](REALIZATION.md#stationary-outputs-and-static-loads) derives the relation and states its loading limits.

## Two optima and two minimum statements

For clamping, define $`\kappa=(G_{12}-G_{21})/2`$, so $`G=\mathrm{Sym}\,G-\kappa J`$. The sharp ceilings are

```math
\lvert\beta\rvert\leq\frac12
\left(\frac1{\sqrt m}-\frac1{\sqrt M}\right)^2,
```

```math
\lvert\kappa\rvert\leq\frac12(\sqrt M-\sqrt m)^2.
```

Compliance has inverse-stiffness units; clamped reaction has stiffness units. Their optima select different allocations in the same family:

| Objective | Optimal allocation |
|---|---|
| Cross-displacement per force | $`h=\sqrt{mM}`$, $`g=m+M-\sqrt{mM}`$ |
| Clamped odd force per displacement | $`g=\sqrt{mM}`$, $`h=m+M-\sqrt{mM}`$ |

Both use $`\lvert\Omega\rvert=\sqrt{mM}/\gamma_y`$. Bounds hold for every admitted constant damping matrix; these equality choices do not prove attainment for each separately fixed anisotropic drag or sparse graph.

Full **clamped-ceiling** attainment needs four coordinates: one hidden coordinate permits at most half the ceiling. This minimum allows damping cross-blocks and needs no force-output stationarity assumption. The **force-ceiling** minimum is conditional: four are necessary when both measured outputs are stationary for every constant force and damping has no measured/hidden cross-block. Neither statement prohibits smaller nonzero responses with three coordinates. See the [precise statements](RESULTS.md#conditional-coordinate-minimum).

## Work and the boundary of the ideal device

For signed displacement-loop area $`\mathcal A`$, delivered quasistatic work is $`W_{\rm qs}=2\kappa\mathcal A`$. This inherited odd-elastic area law becomes a resource-limited work coefficient through the clamped bound. It is not an efficiency or power optimum.

For smooth stiffness, with $`U=q^TKq/2`$, the mechanical ledger is

```math
\dot U=F^T\dot x-\dot q^T\Gamma\dot q
+\tfrac12q^T\dot Kq.
```

The last term is supplied stiffness-control power. In this construction, hidden motion still dissipates energy at a held nonzero output. The pump supplies it even though the stationary probe does no work. Controller losses require additional modeling; [PORT_WORK](PORT_WORK.md) keeps these distinctions explicit.

The [twelve-spring synthesis](REALIZATION.md#twelve-strictly-positive-spring-coefficients) realizes the tangent matrix using positive coefficients and ideal guides in its stated range. It is not a fabricated apparatus or a finite-amplitude theorem. Reduced tuning ranges permit weaker ideal effects, while the screened capacitive actuator loses the DC target when fixed leakage is retained. These [physical limits](PHYSICAL_VALIDITY.md) accompany the exact mechanical theorem and its attaining construction.
