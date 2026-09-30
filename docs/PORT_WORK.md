# Clamped response, work cycles, and the cost of internal motion

[Home](../README.md) · [Model](MODEL.md) · [Force-response theorem](RESULTS.md) · [Device](REALIZATION.md)

This note examines the operating meaning of the existing four-coordinate architecture. The force-controlled compliance ceiling is unchanged. A companion bound concerns a different, explicitly defined measurement: hold the two measured coordinates fixed, let the hidden coordinates cycle, and average the force required to hold them.

The resulting antisymmetric stiffness sets the work per oriented area in a slow displacement cycle. The design maximizing it differs from the design maximizing cross-displacement. Neither optimization maximizes power or efficiency. The familiar possibility of extracting work from an odd-elastic cycle is inherited from the literature; the additional result here is a stiffness-resource ceiling and a costed realization within this particular reciprocal-network class.

## 1. What the measured device can do

Split the normalized coordinates into measured displacements $`x\in\mathbb R^2`$ and hidden displacements $`y\in\mathbb R^r`$. Write

```math
K(t)=\begin{pmatrix}A(t)&B(t)\\B(t)^T&C(t)\end{pmatrix},
\qquad mI\preceq K(t)\preceq MI.
```

The stiffness is real symmetric and uniformly positive, the modulation is prescribed, the origin is fixed, and the full damping is constant symmetric positive definite, as in the [model](MODEL.md). Hold $`x`$ constant. The hidden equation is

```math
\Gamma_{yy}\dot y+C(t)y=-B(t)^Tx.
```

The mean applied reaction is $`\overline F=Gx`$. Its instantaneous expression also contains $`\Gamma_{xy}\dot y`$, whose period average vanishes. Define

```math
g_0=\tfrac12\,\mathrm{tr}\,G,\qquad
\kappa=\tfrac12(G_{12}-G_{21}).
```

Thus $`G=\mathrm{Sym}\,G-\kappa J`$, with $`J_{12}=-1`$ and $`J_{21}=1`$. This sign convention makes positive $`\kappa`$ deliver positive work during a counterclockwise slow displacement cycle.

In general $`G`$ is **not** the inverse of the force-controlled mean compliance. The original rotating planar trap is a counterexample: it has a nonzero mean cross-compliance but, with both coordinates clamped, $`G=\overline K`$ is symmetric. For the attaining four-coordinate family, stationary measured outputs do make $`G=\chi^{-1}`$ exactly at zero probe frequency.

## 2. A sharp clamped-response ceiling

Every finite network above obeys

```math
\boxed{|\kappa|\leq K_{\mathrm{odd},*}},
```

```math
K_{\mathrm{odd},*}=\tfrac12(\sqrt M-\sqrt m)^2.
```

This bound has units of stiffness. The existing compliance ceiling has units of inverse stiffness. They describe distinct measurements and must not be compared as if they were the same quantity.

A stronger waveform-specific disk uses two frozen-reference stiffnesses:

```math
G_{\mathrm s}=\overline{A-BC^{-1}B^T},
```

```math
G_{\mathrm f}=\overline A-\overline B(\overline C)^{-1}\overline B^T.
```

These are the average of the frozen clamped Schur complement and the Schur complement of the averaged full matrix. Put $`g_{\mathrm s,f}=\mathrm{tr}\,G_{\mathrm s,f}/2`$. Then

```math
\kappa^2\leq(g_0-g_{\mathrm s})(g_{\mathrm f}-g_0).
```

For a fixed smooth waveform traversed at changing speed, these are also the slow and fast clamped-response limits. A nonzero endpoint gap is not sufficient for a handed response. This is the same projection mechanism as the [force-response proof](PROOF.md), not a claim of a new general matrix inequality.

### Projection proof

Let $`f=(1,i)^T/\sqrt2`$, $`v(t)=B(t)^Tf`$, and solve

```math
\Gamma_{yy}\dot u+Cu=v.
```

The complex displacement solution is $`y=-u`$, and

```math
z=\overline{v^\dagger u},\qquad
f^\dagger Gf=\overline{f^\dagger Af}-z=g_0+i\kappa.
```

The period-averaged energy identity is $`\mathrm{Re}\,z=\overline{u^\dagger Cu}`$. Define

```math
u_0=(\overline C)^{-1}\overline v,\quad
t_0=\overline v^{\dagger}(\overline C)^{-1}\overline v,
```

```math
\rho=\overline{v^\dagger C^{-1}v}.
```

Here $`u_0`$ is a constant hidden reference displacement. In the $`C`$-weighted phase inner product, the vectors $`u-u_0`$ and $`C^{-1}v-u_0`$ have squared norms $`\mathrm{Re}\,z-t_0`$ and $`\rho-t_0`$. Their inner product is $`z-t_0`$. Cauchy–Schwarz gives

```math
(\mathrm{Im}\,z)^2
\leq(\mathrm{Re}\,z-t_0)(\rho-\mathrm{Re}\,z).
```

Since $`g_{\mathrm s}=\overline{f^\dagger Af}-\rho`$ and $`g_{\mathrm f}=\overline{f^\dagger Af}-t_0`$, this is the stated disk. In particular $`|\kappa|\leq(\rho-t_0)/2\leq\rho/2`$.

To impose the global spectral budget, use the eigenvalue inequality

```math
K^2\preceq(m+M)K-mMI.
```

Its hidden block implies

```math
B^TB+C^2\preceq(m+M)C-mMI.
```

A congruence by $`C^{-1/2}`$ therefore gives

```math
C^{-1/2}B^TBC^{-1/2}
\preceq(m+M)I-C-mMC^{-1}.
```

For every eigenvalue $`c>0`$, $`c+mM/c\geq2\sqrt{mM}`$. Hence

```math
\|BC^{-1/2}\|^2\leq(\sqrt M-\sqrt m)^2.
```

The normalized vector $`f`$ consequently satisfies $`\rho\leq(\sqrt M-\sqrt m)^2`$, proving the ceiling. Zero internal coordinates give $`G=\overline A`$ and $`\kappa=0`$ directly. No count of modes or discretization enters the proof.

### Four coordinates are necessary for clamped attainment

The same proof gives a coordinate-count consequence without requiring stationary outputs in the force-controlled experiment. Set $`c_*=(\sqrt M-\sqrt m)^2`$ and let $`r`$ be the number of hidden coordinates. Pointwise,

```math
H(t)=BC^{-1}B^T\preceq c_*I_2,\qquad
\mathrm{rank}\,H(t)\leq\min(r,2).
```

For $`f=(1,i)^T/\sqrt2`$, reality and symmetry of $`H`$ imply $`f^\dagger Hf=\mathrm{tr}\,H/2`$. Hence

```math
\rho=\tfrac12\overline{\mathrm{tr}\,H}
\leq\tfrac{c_*}{2}\min(r,2),
```

```math
|\kappa|\leq\frac{c_*}{4}\min(r,2).
```

With one hidden coordinate, the clamped coefficient is at most half the full ceiling. Thus full attainment at $`m\lt M`$ requires at least two hidden coordinates, or four total. The construction below attains that minimum. The one-hidden-coordinate bound is not asserted sharp.

This trace estimate is pointwise before averaging: rotating a rank-one coupling does not evade it. Measured/internal damping cross-blocks are allowed because their mean derivative reaction vanishes. This clamped minimum is distinct from the [conditional force-response minimum](PROOF.md#coordinate-minimum).

### Attainment with the same architecture

Use the existing rotating-coupling family, but exchange its measured and internal stiffness allocations:

```math
g=\sqrt{mM},\qquad h=m+M-\sqrt{mM},
```

```math
b^2=(M-h)(h-m),\qquad \Omega=\sqrt{mM}/\gamma_y.
```

Its complete instantaneous spectrum is still $`(m,m,M,M)`$ and its constant internal drag is $`\gamma_yI_2`$. The clamped response is

```math
G=\frac{m+M}{2}I_2-K_{\mathrm{odd},*}J.
```

Thus the bound is sharp. It is not an optimum for every separately specified damping tensor or spring graph. The twelve-spring realization for $`[k_0,3k_0]`$ remains strictly positive: its eight connecting waveforms and modulation speed stay the same, while the measured and internal support stiffnesses exchange values.

## 3. Cross-displacement and work choose different designs

For $`m=k_0`$, $`M=3k_0`$, and equal unit-normalized drag, compare the two allocations:

| Quantity | Compliance-optimal allocation | Clamped-work-optimal allocation |
|---|---:|---:|
| $`h/k_0`$ | 1.732050808 | 2.267949192 |
| $`g/k_0`$ | 2.267949192 | 1.732050808 |
| $`k_0\beta`$ | 0.089316397 | 0.065806131 |
| $`\kappa/k_0`$ | 0.197418394 | 0.267949192 |
| $`W_{\mathrm{qs}}/(k_0\mathcal A)`$ for positive oriented area | 0.394836787 | 0.535898385 |

Both use the same spectrum, total trace, coupling amplitude, and modulation speed. The second delivers about 35.7% more work per fixed slow displacement-loop area, but less cross-displacement per applied force. The first remains the optimizer for the original objective.

This comparison uses **different stiffness allocations**, not an uncounted change in spectral budget. It is not an efficiency or power comparison, and it does not redefine the original theorem to make the existing example appear suboptimal.

## 4. What a closed displacement loop measures

Odd-elastic work cycles are established, including the area law [W1, W2]. With a fixed effective reaction matrix $`G`$ and a signed displacement-loop area

```math
\mathcal A=\tfrac12\oint(x_1\,dx_2-x_2\,dx_1),
```

the work delivered by the device to the external agent is

```math
W_{\mathrm{qs}}=-\oint(Gx)^Tdx=2\kappa\mathcal A.
```

The new clamped bound therefore gives

```math
|W_{\mathrm{qs}}|\leq(\sqrt M-\sqrt m)^2|\mathcal A|.
```

Area is in the fixed, normalized conjugate displacement coordinates. This is a bound on the slow-loop coefficient, not a finite-rate power bound or a bound on arbitrary probe protocols.

For a fixed smooth modulated network, uniform exponential stability makes the slowly moving-port limit precise. Let $`Y(t)`$ solve the periodic hidden problem for unit constant clamped displacements. For $`x(t)=X(t/T)`$, the residual in $`y=Y(t)x(t)`$ is proportional to $`\dot x=O(T^{-1})`$; the stable hidden dynamics give an $`O(T^{-1})`$ tracking error after transients. The oscillatory part of the clamped reaction has a bounded periodic primitive, so integration by parts in the work integral replaces it by its period average with vanishing error. Constant damping terms also contribute a vanishing correction. This establishes the area limit as $`T\to\infty`$ for a fixed smooth closed path and fixed pump waveform. The constants are not uniform over all networks and periods.

For the rotating architecture, the stronger finite-rate result below avoids a general averaging approximation entirely.

### Exact dynamics for arbitrary port motion

For the rotating architecture with $`\Gamma=\mathrm{diag}(\gamma_xI_2,\gamma_yI_2)`$, transform only the hidden variables, $`w=R(\Omega t)y`$. Then

```math
\gamma_y\dot w+(gI_2-\gamma_y\Omega J)w=-bx,
```

```math
F=\gamma_x\dot x+hx+bw.
```

These equations are exact. The transformation is not a physical rotation of the guides and does not introduce a free force source.

For a smooth closed port trajectory in its attracting periodic transformed response, write $`w_0=-b(gI_2-\gamma_y\Omega J)^{-1}x`$. The difference $`e=w-w_0`$ obeys a stable linear equation forced by $`\dot x`$. Its energy estimate gives

```math
\left|W_{\mathrm{out}}-2\kappa\mathcal A\right|
\leq c_{\mathrm{rate}}\int|\dot x|^2dt,
```

```math
c_{\mathrm{rate}}=\gamma_x+
\frac{\gamma_y b^2}{g\sqrt{g^2+(\gamma_y\Omega)^2}}.
```

The proof uses $`\|e\|_{L^2}\leq\gamma_yb\|\dot x\|_{L^2}/[g\sqrt{g^2+(\gamma_y\Omega)^2}]`$ and Cauchy–Schwarz in the extra port work. For a fixed path traversed over a time $`T`$, the right-hand side is proportional to $`1/T`$. This gives an explicit finite-rate approach to the same quasistatic area law. It does not optimize that rate bound.

## 5. Finite circular cycle and complete power accounting

Prescribe

```math
x(t)=r_0R(\omega t)e_1,
```

where $`\omega`$ is the signed **probe-cycle** rate and $`\Omega`$ remains the modulation rate. These are different controls. Put $`\delta=\Omega-\omega`$ and

```math
\kappa_\delta=\frac{b^2\gamma_y\delta}{g^2+(\gamma_y\delta)^2}.
```

After transients, exact solution of the two hidden equations gives

```math
P_{\mathrm{out}}=r_0^2\omega(\kappa_\delta-\gamma_x\omega),
```

```math
P_{\mathrm{drive}}=r_0^2\Omega\kappa_\delta,
```

```math
P_{\mathrm{loss},x}=r_0^2\gamma_x\omega^2,
\qquad P_{\mathrm{loss},y}=r_0^2\delta\kappa_\delta.
```

The stored spring energy is constant along this circular solution. Hence

```math
P_{\mathrm{drive}}=P_{\mathrm{out}}
+P_{\mathrm{loss},x}+P_{\mathrm{loss},y}.
```

The work per port cycle is each power multiplied by $`2\pi/|\omega|`$. The formula remains valid for opposite rotation and for rates exceeding the pump, with signed drive and output powers retained. An efficiency is quoted only when both drive input and delivered output are positive.

For $`0\lt \omega\lt \Omega`$ in the work-producing range,

```math
\eta_{\mathrm{mech}}=\frac{\omega}{\Omega}
\left(1-\frac{\gamma_x\omega}{\kappa_\delta}\right)
\lt \frac{\omega}{\Omega}.
```

This is net work delivered to the imposed probe divided by work delivered by the stiffness modulation. It is not wall-plug efficiency. The drive and probe controls are prescribed; autonomous load following or actuator efficiency is not supplied by this calculation.

### A closed, finite example

Use the work-optimal $`[k_0,3k_0]`$ design, $`\gamma_x=\gamma_y=\gamma`$, and $`\omega=\Omega/20`$. The pump executes twenty complete periods per port cycle, so the whole prescribed schedule and state close. Energies below are divided by $`k_0r_0^2`$:

| Per-cycle quantity | Value |
|---|---:|
| Work delivered by the stiffness modulation | 33.627242208 |
| Work delivered to the external load | 1.137222301 |
| Viscous loss at measured coordinates | 0.544139809 |
| Viscous loss at internal coordinates | 31.945880097 |
| Mechanical conversion efficiency | 3.38185% |

The two losses plus output equal input. Reversing only the probe cycle reverses the useful odd-work tendency while retaining viscous costs. Reversing both pump and probe preserves the energy magnitudes. Stopping the pump leaves a reciprocal system and no work-producing cycle.

### Slower is not more efficient for this continuously driven family

At fixed nonzero $`\Omega`$ and loop radius, $`\omega\to0^+`$ yields a finite work per cycle, approaching $`2\pi r_0^2\kappa`$, but the total drive work grows as $`1/\omega`$. The internals dissipate even while a nonzero measured displacement is held fixed. Therefore $`\eta_{\mathrm{mech}}\to0`$ along this slow-loop limit.

This is not a universal bound on all odd engines. Other models optimize other controls, energy accounts, and cycles [W3]. Here no subtraction of the ongoing holding loss is used to advertise a larger efficiency. The response ceiling and the area-work ceiling must not be sold as high-efficiency energy-conversion results.

## 6. Comparison with actual odd-elastic architectures

### W1 — Work-producing odd elasticity is established

C. Scheibner et al., *Odd elasticity*, Nature Physics **16**, 475–480 (2020), [primary record](https://www.nature.com/articles/s41567-020-0795-y), [arXiv:1902.07760](https://arxiv.org/abs/1902.07760).

The [full accepted manuscript](https://purehost.bath.ac.uk/ws/portalfiles/portal/205056987/OddElasticity_MainText.pdf) was inspected. Using manuscript pagination, Eq. (1), pp. 1–2, introduces active transverse bonds; Eq. (2), p. 2, gives the odd constitutive matrix; p. 3 states the closed-cycle work formula and explains its area interpretation. Equations (5)–(7), pp. 6–7, connect an elastic potential to major symmetry and static reciprocity. We inherit these concepts. These passages do not supply our positive reciprocal periodic stiffness budget or stationary-port equality construction. The Bath-hosted copy contains a cover followed by the accepted manuscript; its separate supplemental information was not checked, and its numbering should not be mixed with arXiv v1.

### W2 — A realized active elastic element with a static odd response

Y. Chen, X. Li, C. Scheibner, V. Vitelli, and G. Huang, *Realization of active metamaterials with odd micropolar elasticity*, Nature Communications **12**, 5935 (2021), [full publisher article](https://www.nature.com/articles/s41467-021-26034-z).

The inspected design, constitutive equations, and work-cycle discussion are direct precedents for an operating odd element. Its piezoelectric patches sense bending and use an electronic feed-forward circuit to actuate shear. The article demonstrates waves experimentally and tests quasistatic work cycles in coupled finite-element simulations; those two forms of evidence should not be conflated.

Our actuation is a displacement-independent stiffness schedule, and our full instantaneous elastic matrix is symmetric. That difference matters to the resource model, but it is not a first demonstration of static nonreciprocal response, a work-generating cycle, or active elastic computation. The proposed guided device also relies on external supports and damping; it is not a freestanding momentum-conserving micropolar continuum like their construction.

### W3 — Energy conversion has its own objective

Étienne Fodor and Anton Souslov, *Optimal power and efficiency of odd engines*, Physical Review E **104**, L062602 (2021), [primary article record](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.104.L062602), [full primary preprint, v2](https://arxiv.org/pdf/2109.10603v2). The publisher records publication on 27 December 2021.

The full preprint's Eqs. (2)–(5), p. 2, define extracted cycle work, dissipation from the even loss modulus, and the efficiency $`E=W/(W+D)`$. The text following Eq. (5) explicitly excludes the microscopic mechanisms sustaining the energy input. Page 3 distinguishes some odd solids that do not dissipate at rest from continually active constituents; Eq. (10) gives the quasistatic area work and the Kelvin–Voigt slow-cycle efficiency result. These passages were also visually checked in the rendered PDF.

Our energy ledger explicitly resolves the modeled hidden-coordinate losses, including loss at a held nonzero displacement. Its denominator is therefore not automatically the same as their response-level $`W+D`$. Our slow-cycle efficiency tending to zero does not contradict their near-unit regimes. Neither result includes every apparatus's controller or fuel-conversion cost, and no equivalence by parameter substitution is claimed.

### W4 — Eliminating a driven coordinate is also established

L.-S. Lin et al., *Onsager's Variational Principle for Nonreciprocal Systems with Odd Elasticity*, Journal of the Physical Society of Japan **92**, 033001 (2023), [arXiv:2209.15363v2](https://arxiv.org/abs/2209.15363).

The later [full-text comparison](SCALE_FREE_RESPONSE.md#6-a-real-predecessor-exposes-the-physical-boundary) inspected the primary PDF's Eqs. (1)–(12). Eliminating a driven frictional coordinate produces an odd positional force, so this mechanism is established. Its coordinate-dependent dissipation and unconfined drive coordinate are outside the present full-network model. This is a specific constitutive distinction, not a novelty claim for eliminating hidden coordinates.

### W5 — Driven mechanics without electronic feedback

M. Rahimi and H. S. Park, *Driven Odd Elasticity in Passive Mechanical Metamaterials*, [arXiv:2607.13997v1](https://arxiv.org/html/2607.13997v1), 15 July 2026 preprint.

Sections 1–3 were inspected in full HTML. Their chiral gears have frictional contacts, clearances, and changes of contact point during strain increments. Periodically driven gears act on a lattice; the resulting averaged nonsymmetric constitutive law supports work cycles. Thus absence of electronic feedback and use of individually passive mechanical elements are not new broad claims available here.

Our continuously positive homogeneous linear stiffness, fixed equilibrium, and prescribed coefficient modulation exclude those contact transitions. This gives a specific comparison of mechanisms, not an assertion that one is universally more physical or technologically useful.

## 7. What is and is not claimed

The combination now provides two distinct resource-matched limits: cross-displacement per force, and clamped odd force per displacement. The latter gives a maximal slow-cycle work per oriented area. Both have small constructions in the same reciprocal driven network class. Their operators and energy accounts are explicit.

The proof uses established projection, Schur-complement, and scalar inverse geometry. The [exact positive-map substitution](OPERATOR_CONNECTION.md#the-exact-inverse-gap-constants-are-established) identifies the published inverse-gap constant used in this ceiling. The inspected architecture papers do not supply the complete resource-matched mechanical attainment and clamped coordinate minimum. No new general theory of odd elasticity, efficiency theorem, exhaustive priority certificate, platform feasibility, or technological energy saving is established here.

The comparison removes two possible overclaims: our original compliance optimizer is not an optimizer for every useful mechanical task, and finite odd work does not imply efficient conversion when internal cycling losses are charged. The original force-response theorem, fixed references, and positive-spring implementation remain unchanged.

## Reproduce

Run `python checks/port_work.py --output port-work.local.json` from the repository root. The new module imports no preceding research functions. It checks exact stepped clamped dynamics, sharpness under several stiffness intervals, the different stiffness allocations, full laboratory-frame energy integration from transients, noncircular finite-rate error, and drive/reversal controls.

The small finite tests support the equations but do not prove the universal bounds. The clamped measurement and the slowly imposed work cycle are distinguished throughout from the original force-controlled mean response. There are no hardware observations in this note.
