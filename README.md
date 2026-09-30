# Driven Mechanical Response Limits

### Reciprocal springs, driven odd response, and a sharp design limit

In a static linear spring network, exchanging the applied force and measured displacement gives the same cross-response. Periodic stiffness control can break that symmetry even though every instantaneous spring force remains reciprocal.

**How large can the resulting nonreciprocal response be if the stiffness of the entire network stays within a fixed range?**

This repository gives sharp limits for two measurements and a four-coordinate network that attains each limit at a different stiffness allocation. Its two measured coordinates remain stationary under constant forces while two hidden coordinates cycle. A twelve-spring construction realizes the worked example in the small-displacement limit.

The modulation supplies energy. The result is a design limit for a driven constitutive element, with explicit force, load, and work interpretations.

## Two measurements, two sharp limits

Fix physical coordinates and conjugate forces. The complete instantaneous stiffness $`K(t)`$ is symmetric, and every eigenvalue lies in $`[m,M]`$, with $`0<m<M`$. Damping is constant, symmetric, and positive definite. The origin stays fixed while the stiffness schedule repeats.

| Measurement | What is imposed and measured | Odd response |
|---|---|---|
| Constant-force response | Apply $`F`$ and average the measured displacement: $`\overline{P^Tq}=\chi F`$ | Cross-compliance $`\beta=(\chi_{21}-\chi_{12})/2`$ |
| Clamped response | Hold measured displacement $`x`$ fixed and average the holding force: $`\overline F=Gx`$ | Odd stiffness $`\kappa=(G_{12}-G_{21})/2`$ |

The [model](docs/MODEL.md) fixes the port normalization and counts every compliant coordinate. Over this class, the sharp ceilings are

```math
\boxed{
|\beta|\leq B_*
=\frac12\left(\frac1{\sqrt m}-\frac1{\sqrt M}\right)^2
}
```

and

```math
\boxed{
|\kappa|\leq K_{\mathrm{odd},*}
=\frac12\left(\sqrt M-\sqrt m\right)^2.
}
```

The bounds hold independently of network size, waveform, and period. Attainment uses suitable hidden-coordinate damping; optimality for every separately prescribed damping tensor or spring graph is not asserted. See the [force theorem](docs/RESULTS.md#spectral-ceiling) and [clamped theorem](docs/PORT_WORK.md#2-a-sharp-clamped-response-ceiling).

**These are distinct experiments.** In general $`G\ne\chi^{-1}`$. The attaining family has stationary measured outputs, which makes $`G=\chi^{-1}`$ and static-load composition exact for that family. Maximizing the two odd coefficients still selects different stiffness allocations.

## Begin with one review

The teaching anchor is **Michel Fruchart, Colin Scheibner, and Vincenzo Vitelli, [*Odd Viscosity and Odd Elasticity*](https://doi.org/10.1146/annurev-conmatphys-040821-125506), Annual Review of Condensed Matter Physics 14, 471–510 (2023)**. An [arXiv version](https://arxiv.org/abs/2207.00071) is also available.

The selected portions explain reciprocity, odd constitutive response, and cyclic work. The local [tutorial bridge](docs/TUTORIAL.md) translates those ideas into our finite-dimensional driven model, distinguishes the measurements, and leads into the proof and construction. It assumes basic linear algebra, calculus, and mechanical work. A second external textbook is not required. The [reading guide](docs/TUTORIAL_OPTIONS.md) gives exact published section numbers and records the alternative entry points.

## Read the repository in three passes

| Pass | Route | Purpose |
|---|---|---|
| Orientation | This page → [physical explanation](docs/START_HERE.md) | Question, measurements, and design meaning |
| Learn the argument | Selected review passages → [tutorial bridge](docs/TUTORIAL.md) | Connect odd elasticity to the budget, proof, and attaining device |
| Inspect the result | [Model](docs/MODEL.md) → [Results](docs/RESULTS.md) → [Proof](docs/PROOF.md) → [Clamped work](docs/PORT_WORK.md) | Assumptions, exact statements, and derivations |

The [documentation map](docs/README.md) provides direct routes to construction, operator attribution, physical limits, sources, and reproducibility. Each formal statement has a canonical location; the tutorial supplies the connecting explanation.

## The construction at a glance

Two accessible coordinates $`x\in\mathbb R^2`$ couple to a hidden plane $`y\in\mathbb R^2`$. Their individual stiffnesses stay fixed while the coupling rotates:

```math
K(t)=
\begin{pmatrix}
hI_2 & bR(t)\\
bR(t)^T & gI_2
\end{pmatrix},
\qquad R(t)=e^{\Omega tJ}.
```

Here $`J_{12}=-1`$, $`J_{21}=1`$, $`g=m+M-h`$, and $`b^2=(M-h)(h-m)`$. The full spectrum is always $`(m,m,M,M)`$. The construction uses block-diagonal damping $`\Gamma=\operatorname{diag}(\Gamma_x,\gamma_yI_2)`$, with $`\Gamma_x\succ0`$ and $`\gamma_y>0`$. Both optima use $`|\Omega|=\sqrt{mM}/\gamma_y`$.

| Objective | Measured allocation $`h`$ | Hidden allocation $`g`$ |
|---|---|---|
| Largest cross-displacement per force | $`\sqrt{mM}`$ | $`m+M-\sqrt{mM}`$ |
| Largest clamped odd force per displacement | $`m+M-\sqrt{mM}`$ | $`\sqrt{mM}`$ |

Four coordinates are necessary and sufficient for the **full clamped ceiling**. The separate force-ceiling minimum assumes stationary measured outputs for every constant force and no measured/internal damping cross-block. These are minima for exact attainment, not for every nonzero odd response.

For $`m=k_0`$ and $`M=3k_0`$, the force-optimal response is

```math
k_0\chi_*=
\begin{pmatrix}
2/3 & -(2-\sqrt3)/3\\
(2-\sqrt3)/3 & 2/3
\end{pmatrix}.
```

The exchanged cross-displacements have opposite signs. The [spring realization](docs/REALIZATION.md) uses eight positive modulated springs and four positive fixed supports on ideal guides, with fixed rest lengths and no prestress at the reference origin.

## Work, attribution, and physical scope

For a slow displacement loop with signed area $`\mathcal A`$, the delivered work is $`W_{\mathrm{qs}}=2\kappa\mathcal A`$. This familiar odd-elastic area law is inherited from the literature. The [work account](docs/PORT_WORK.md#5-finite-circular-cycle-and-complete-power-accounting) also charges internal motion: the device dissipates during holding, and its slow-cycle work does not establish an efficiency or power optimum.

The [operator comparison](docs/OPERATOR_CONNECTION.md) attributes the response geometry and exact inverse-gap constants to established methods. The contribution is their constrained mechanical attainment, the clamped coordinate minimum, and the port/resource interpretation. A budget on the measured stiffness alone differs from a budget on the complete network.

The proposed geometry is an ideal tangent realization. Its worked example requires 21:1 connecting-spring tuning. [Smaller tuning ranges](docs/TUNING_RANGE.md) permit attainment at smaller stiffness contrast; the relative response vanishes quadratically as tuning approaches unity. The [capacitive actuator screen](docs/CAPACITIVE_ACTUATION.md) finds that fixed leakage restores reciprocal long-time response in that circuit. No complete apparatus is certified.

The theorem concerns linear overdamped dynamics and prescribed coefficients. The [physical-validity note](docs/PHYSICAL_VALIDITY.md) states the small-mass consistency result and the limits of the geometric and actuator assumptions. The [research status](docs/RESEARCH_STATUS.md) records the focused theory scope; manuscript writing has not begun.

## Reproduce the checks

Use Python 3.11 or later in a virtual environment:

```sh
python -m pip install -r requirements.txt
python checks/run.py --output results.local.json
python checks/port_work.py --output port-work.local.json
python checks/scale_free.py --output scale-free.local.json
python checks/finite_mass.py --output finite-mass.local.json
python checks/capacitive_shunt.py --output capacitive-shunt.local.json
python checks/check_docs.py
```

The [verification map](docs/REPRODUCIBILITY.md#claim-map) links each result to its proof and finite diagnostic. Numerical checks test formulas and implementation consistency; the proofs establish the universal statements. The original [reference values](checks/reference.json) remain fixed.

Copyright © 2026 Ruge Lin. [MIT license](LICENSE).
