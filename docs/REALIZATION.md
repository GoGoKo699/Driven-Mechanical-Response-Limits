# The attaining device, static loads, and positive springs

[Home](../README.md) · [Model](MODEL.md) · [Results](RESULTS.md) · [Proof](PROOF.md)

## Stationary outputs and static loads

The device has measured coordinates $x\in\mathbb R^2$ and internal coordinates $y\in\mathbb R^2$. Its instantaneous reciprocal stiffness is

$$
K(t)=\begin{pmatrix}hI_2&bR(t)\\bR(t)^T&gI_2\end{pmatrix}.
$$

The [parameter choices](RESULTS.md#attaining-four-coordinate-family) give the spectrum $(m,m,M,M)$. In the variable $w=Ry$, the attracting constant-force solution has constant $x,w$ and rotating $y$. Therefore

$$
F=G_{\rm dc}x,
$$

$$
G_{\rm dc}=hI_2-b^2(gI_2-\gamma_y\Omega J)^{-1}.
$$

A constant symmetric positive-semidefinite spring load $L$ acting only on $x$ gives exactly

$$
\chi_L=(G_{\rm dc}+L)^{-1}.
$$

Clamping $x$ gives the same reaction matrix. Additional constant measured-coordinate damping affects transients but not this constant response. Hidden-coordinate loads, anisotropic internal drag, finite probe frequency, or arbitrary time-varying output loads require the full equations instead.

For the worked units $k_0=\gamma_y=1$, a unit isotropic spring load gives

$$
\chi_L\simeq\begin{pmatrix}
0.40171819&-0.03206183\\
0.03206183&0.40171819
\end{pmatrix}.
$$

These properties are verified by from-rest integration, not by initializing the analytic periodic state.

## Where the power comes from

At fixed $x$, the internal viscous loss equals the modulation power:

$$
\overline{P_{\rm drive}}=\gamma_y\Omega^2\|w\|^2.
$$

Equivalently it is

$$
\frac{\gamma_y\Omega^2b^2}{g^2+\gamma_y^2\Omega^2}\|x\|^2.
$$

The constant probe does no work once $x$ stops moving. The modulation drive powers the cycling internals. In the linear model the full instantaneous balance is

$$
\dot V=F^T\dot x-q^{\prime T}\Gamma q'+\tfrac12q^T\dot Kq,
$$

where $q'=\dot q$ and $V=q^TKq/2$. This accounts for work delivered by changing stiffness, not the inefficiency of a particular actuator or controller.

## Twelve strictly positive spring coefficients

Choose $\eta>0$ such that

$$
\min(h,g)>b(3/2+2\eta)=d_0.
$$

For each measured/internal pair $(i,j)$ and each sign $\sigma\in\{-1,+1\}$, use a spring with generalized elongation $(x_i+\sigma y_j)/\sqrt2$ and stiffness

$$
\kappa_{ij}^{\sigma}(t)=\tfrac b2(R_{ij}(t)+\sigma)^2+b\eta.
$$

Every coefficient exceeds or equals $b\eta>0$. The two springs for a pair contribute the off-diagonal coupling $bR_{ij}$ and diagonal amount $b(1+R_{ij}^2)/2+b\eta$. The sum over each row or column is $d_0$, independent of time, because $R$ is orthogonal.

Add two measured support springs of stiffness $h-d_0$ and two internal support springs of stiffness $g-d_0$. Their total tangent energy is exactly $q^TK(t)q/2$. Only the eight connecting springs are modulated. Their waveforms have a constant term and the first two temporal harmonics.

For $m=k_0$, $M=3k_0$, $h=\sqrt3k_0$ and $\eta=0.1$:

| Component | Stiffness divided by $k_0$ |
|---|---:|
| Each measured support spring | 0.094214632765 |
| Each internal support spring | 0.630113017627 |
| Minimum connecting coefficient | 0.096343304400 |
| Maximum connecting coefficient | 2.023209392405 |

This positive decomposition is guaranteed for the worked contrast and for parameters satisfying the displayed feasibility condition. It is not claimed for every spectral contrast with the same twelve-spring layout.

The chosen connecting waveforms require each spring to traverse a 21:1 stiffness range. The [physical-validity analysis](PHYSICAL_VALIDITY.md#the-existing-spring-schedule-requires-a-large-tuning-range) derives this requirement and its support-margin trade-off, and separately proves a controlled small-mass limit of the same four-coordinate model.

## Fixed geometry and exact spring lengths

Let measured sliders translate along horizontal fixed guides and internal sliders along vertical fixed guides. Multiple rigid attachment tabs allow two diagonal slopes for each pair. Crossings may be separated in fixed parallel layers. Guides and fixtures are ideal constraints, and this is not a fabrication drawing.

For each diagonal spring choose reference direction $n_\sigma=(1,-\sigma)/\sqrt2$, fixed rest length $L_0$, and endpoint separation

$$
d_{ij}^{\sigma}=L_0n_\sigma+(-x_i,y_j).
$$

Its exact central-force energy is

$$
V_{ij}^{\sigma}=\tfrac12\kappa_{ij}^{\sigma}(t)(|d_{ij}^{\sigma}|-L_0)^2.
$$

At the origin each spring is unextended. Changing its coefficient therefore introduces no reference force or equilibrium shift. Expansion gives

$$
V_{ij}^{\sigma}=\tfrac14\kappa_{ij}^{\sigma}(x_i+\sigma y_j)^2
+O(\kappa\|q\|^3/L_0).
$$

The tangent stiffness is exactly the one above. The two components of the internal plane can be separate guided sliders; they need not describe one physical point orbiting in a plane.

The checks integrate actual central forces from these lengths and verify the force Jacobian at the origin. Guide reactions do no work in the ideal permitted translations. Finite guide compliance, geometric misalignment, friction, and parasitic actuation forces are not covered by that idealization.

## Finite displacement is a different model

Central-difference response estimates from exact-length integration give:

| Force divided by $k_0L_0$ | Estimated $k_0\beta$ | Maximum axial strain |
|---|---:|---:|
| 0.02 | 0.089354291384 | 1.285% |
| 0.005 | 0.089318761018 | 0.3173% |

The tangent optimum is $0.089316397477\ldots$. These nonlinear values slightly above it are not counterexamples: finite stretching changes the local tangent stiffness and leaves the exact linear resource class. The error drops approximately quadratically with force. Small measured-coordinate ripple also remains at finite amplitude; exact stationarity belongs to the tangent model.

The energy calculation uses actual extensions, their time-dependent coefficients, probe power, and viscous loss. These integrations check a linearization; they do not prove nonlinear global stability or give laboratory performance figures.

## Calibration tolerance

With one-percent relative errors in every positive spring coefficient, the [general perturbation estimate](PROOF.md#coefficient-errors) guarantees

$$
\widetilde\beta\geq0.05901336717/k_0.
$$

The nominal value is $0.08931639748/k_0$. The actual stiffness interval may expand to $[0.99k_0,3.03k_0]$. This is a conservative robustness statement for periodic coefficient errors, not proof of exact optimality after perturbation or of tolerance to all implementation errors.

Prescribed mechanical stiffness modulation has direct experimental precedent [R7](SOURCES.md#r7). The full guide/rest-length/damping construction still requires platform-specific analysis. [Source and model limitations](SOURCES.md#assumption-register) remain separate from the exact elastic decomposition.

## Work cycles and the choice of objective

The inverse static response of the special four-coordinate architecture supports an externally imposed displacement cycle. The [clamped-response and work analysis](PORT_WORK.md) gives a sharp odd-stiffness ceiling under the same instantaneous spectral budget, identifies a different optimal stiffness allocation, and charges the modulation and internal viscous loss explicitly. A maximal cross-displacement is not the same objective as work per displacement-loop area, maximum power, or efficiency.
