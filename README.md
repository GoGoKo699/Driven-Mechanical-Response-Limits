# Driven Mechanical Response Limits

**How much nonreciprocal response can a network produce when every instantaneous spring force is reciprocal?**

This repository derives a sharp limit for the response to a constant force in periodically modulated, overdamped mechanical networks. The limit does not depend on the number of internal coordinates. A four-coordinate construction attains it, with stationary measured outputs and cycling internal motion. A twelve-spring guided-slider construction realizes the worked example in the small-displacement limit.

The modulation is externally powered. Reciprocal instantaneous springs do not make the complete driven device passive.

## The central result

Let every instantaneous stiffness eigenvalue lie between $m$ and $M$, where $0<m<M$. Fix the physical coordinate and conjugate-force normalization. Apply two constant force components and measure their conjugate displacements after transients:

$$
\overline{P^Tq}=\chi F.
$$

The antisymmetric cross-compliance is $\beta=(\chi_{21}-\chi_{12})/2$. Every network in the [stated model](docs/MODEL.md) obeys

$$
|\beta|\leq B_*.
$$

$$
B_*=\frac12\left(\frac1{\sqrt m}-\frac1{\sqrt M}\right)^2.
$$

The damping matrix may be any constant symmetric positive-definite matrix. Attainment uses a suitable internal damping plane; optimality for every separately prescribed damping tensor is not asserted.

For $m=k_0$ and $M=3k_0$, the construction has

$$
k_0\chi_*=\begin{pmatrix}
2/3&-(2-\sqrt3)/3\\
(2-\sqrt3)/3&2/3
\end{pmatrix}.
$$

A force at one measured coordinate moves the other in the opposite sense to the exchanged experiment. This is not an amplitude isolator or a mechanical diode.

## Choose a reading route

| Goal | Start here |
|---|---|
| Understand the physical question | [A short explanation](docs/START_HERE.md) |
| Inspect the mathematical statement | [Model](docs/MODEL.md) → [Results](docs/RESULTS.md) → [Proof](docs/PROOF.md) |
| Examine the device and its loads | [Construction and spring geometry](docs/REALIZATION.md) |
| Compare with existing work | [Sources and assumption register](docs/SOURCES.md) |
| Reproduce the evidence | [Reproducibility and claim map](docs/REPRODUCIBILITY.md) |

## What the result includes

The proof first resolves a response disk using the stiffness allocated to the measured directions, then optimizes over that allocation. An [operator comparison](docs/OPERATOR_CONNECTION.md) identifies the established resolvent structure and a sharper fixed-schedule budget given by the difference between slow- and fast-driving compliance. This distinguishes a fixed measured-stiffness budget from a fixed spectrum of the complete network.

Four coordinates are the minimum for **exact ceiling attainment with both outputs stationary for every constant force**, when measured and internal coordinates have no direct damping cross-block. This is not a minimum for all nonreciprocal response or for the number of springs.

The attaining element composes with static loads at its measured coordinates. Its twelve-spring realization uses eight strictly positive modulated springs, four strictly positive fixed support springs, fixed guides, and fixed rest lengths. Exact-length integrations test the geometric linearization, not the universal theorem.

## Run the checks

Use Python 3.11 or later in a virtual environment:

```sh
python -m pip install -r requirements.txt
python checks/run.py --output results.local.json
python checks/check_docs.py
```

The suite covers the bound, equality construction, forced/loaded/clamped dynamics, positive-spring synthesis, finite-length mechanics, topology controls, and coefficient-error bounds. The [claim map](docs/REPRODUCIBILITY.md#claim-map) distinguishes proofs from finite diagnostics. The checked reference values are in [checks/reference.json](checks/reference.json).

## Scope

The main result concerns linear overdamped dynamics, constant damping, prescribed periodic stiffness, fixed equilibrium, and normalized force/displacement ports. It does not establish an inertial, feedback-controlled, broadband, or bulk-material response law. The proposed geometry is not a fabricated device, and controller losses are not optimized.

The [source comparison](docs/SOURCES.md) identifies established ingredients and the remaining operator-bound and implementation questions. This is a research repository, not a manuscript or a hardware report.

Copyright © 2026 Ruge Lin. [MIT license](LICENSE).
