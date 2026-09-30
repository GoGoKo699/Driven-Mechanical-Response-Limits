# Model and measurement

[Home](../README.md) · [Results](RESULTS.md) · [Proof](PROOF.md)

## Coordinates and resources

For $`q\in\mathbb R^n`$, consider

```math
\Gamma\dot q(t)+K(t)q(t)=PF.
```

The force $`F\in\mathbb R^2`$ is constant. The real $`n\times2`$ matrix $`P=(p_1\ p_2)`$ has orthonormal columns. Measured displacements are $`P^Tq`$, so probe power is $`F^TP^T\dot q`$. Coordinates are fixed generalized translations with conjugate forces. Coordinate rescaling is not free.

The damping matrix $`\Gamma`$ is constant, symmetric, and positive definite. The real symmetric stiffness is bounded, periodic, and may be piecewise continuous:

```math
mI\preceq K(t)\preceq MI,\qquad 0\lt m\lt M.
```

A bounded measurable periodic schedule also suffices for the averaged proof with absolutely continuous solutions. The construction uses smooth coefficients. All retained compliant coordinates are included in these matrices. Ideal guides and fixed supports are constraints, not omitted soft modes; finite support compliance would need a separate model.

The equilibrium origin is fixed. There is no inertia, displacement-dependent feedback, time-varying damping, or forcing induced by a moving trap center. The prescribed modulation is externally powered. No bandwidth, period, or actuation-power budget is imposed by the theorem.

The model uses deterministic mean motion. Adding independent additive zero-mean noise to the linear equation leaves the mean equation unchanged, but this observation is not a noise-performance or fluctuation-transport theorem.

## Attracting periodic response

A homogeneous difference $`u`$ between two trajectories satisfies

```math
\frac{d}{dt}(u^T\Gamma u)=-2u^TKu.
```

Consequently it decays at least exponentially at the rate supplied by $`m/\lambda_{\max}(\Gamma)`$. The periodic affine evolution is a contraction, so the driven periodic solution is unique and attracts every initial condition. No Floquet instability is used.

A bar denotes a normalized average over one period after transients. Define

```math
\overline{P^Tq}=\chi F,
```

```math
\alpha=\tfrac12\,\mathrm{tr}\,\chi,\qquad
\beta=\tfrac12(\chi_{21}-\chi_{12}).
```

The target is $`|\beta|`$: absolute antisymmetric steady-force compliance. It is not $`|\beta|/\alpha`$, a directional transmission ratio, a power efficiency, or a broadband isolation measure.

## Two different stiffness budgets

Define scalars

```math
h=\tfrac12\overline{\mathrm{tr}(P^TKP)},
```

```math
j=\tfrac12\overline{\mathrm{tr}(P^TK^{-1}P)}.
```

The inverse in $`j`$ is the inverse of the **full** stiffness. It allows hidden displacement in the frozen static problem. It is neither the inverse of the measured stiffness block nor the inverse of the final mean response.

Holding the spectral interval fixed does not hold $`h`$ fixed. Holding the global trace fixed does not do so either. The [results](RESULTS.md) state both resource questions explicitly.

## Static loading

For a generic modulated device, mean compliance is not a substitute for its full time-dependent input–output relation. A load acts on the actual trajectory, including its within-cycle motion.

The special attaining construction has stationary measured outputs under constant forces. A static spring attached only to those coordinates then composes exactly with its zero-frequency inverse compliance. This does not justify the same substitution for arbitrary protocols, hidden-coordinate loads, or finite probe frequencies.

## Notation

| Symbol | Meaning |
|---|---|
| $`m,M`$ | Complete instantaneous stiffness eigenvalue bounds |
| $`P`$ | Two normalized conjugate force/displacement directions |
| $`\Gamma`$ | Constant positive symmetric damping |
| $`h,j`$ | Mean measured stiffness and full-inverse stiffness scalars |
| $`\alpha,\beta`$ | Mean direct and antisymmetric compliance |
| $`D=mM`$ | Product of stiffness endpoints, not a damping symbol |
| $`k=(m+M)/2`$, $`a=(M-m)/2`$ | Midpoint and half-width of the spectral interval |
| $`b`$ | Coupling amplitude of the four-coordinate construction; generally not $`a`$ |
| $`\Omega`$ | Rotation rate of the coupling block in that construction |
| $`J`$ | Planar matrix with $`J_{12}=-1`$, $`J_{21}=1`$ |

Every inference is conditional on the equations and normalization above. The [assumption register](SOURCES.md#assumption-register) distinguishes established primitives from this particular design and from incomplete implementation evidence.
