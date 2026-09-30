# Selected review and reading guide

[Home](../README.md) · [Tutorial bridge](TUTORIAL.md) · [Background and citation map](MANUSCRIPT_BACKGROUND.md)

**The selected teaching anchor is Fruchart, Scheibner, and Vitelli's review.** The route below supplies the physical introduction; the [local tutorial](TUTORIAL.md) carries its reader into the driven measurement, resource budget, proof, and construction. Basic linear algebra and calculus are the mathematical prerequisites.

Strang and Milton remain recorded as alternative entry points, not additional required reading. The review supplies established physical context; the repository gives its own precise model and derivations. The source does not establish the proposed apparatus.

## 1. Fruchart, Scheibner, and Vitelli — selected physics anchor

Michel Fruchart, Colin Scheibner, and Vincenzo Vitelli, *Odd Viscosity and Odd Elasticity*, Annual Review of Condensed Matter Physics **14**, 471–510 (2023). [Publisher and DOI](https://doi.org/10.1146/annurev-conmatphys-040821-125506) · [Open published PDF](https://par.nsf.gov/servlets/purl/10418598) · [arXiv version](https://arxiv.org/abs/2207.00071).

Read the odd-elasticity portions selectively. The following numbers refer to the **published review**, not the differently paginated arXiv preprint.

| Passage | Preparation |
|---|---|
| §1, p. 472; §2.1, p. 473; Table 1, p. 474 | Elastic and viscous response; symmetric and antisymmetric parts; deformation/stress basis |
| §§3.1–3.2.2, pp. 487–490 | Odd constitutive response, deformation cycles, and static deflection |
| §§3.3.1–3.3.3, pp. 491–494; especially §3.3.2 | Reciprocity, conjugate variables, and the work interpretation |
| §§3.4.4–3.4.5, pp. 497–498 | Mechanical examples with two coupled deformation modes |

**Why it is closest.** It supplies the language for the actual physical question: exchange asymmetry, odd stiffness, and work from a deformation loop. Most of its fluid, quantum, and topological-wave material is unnecessary for this project. Basic matrix algebra, calculus, and forces/work should suffice for the selected route; this prerequisite assessment is ours.

**The remaining bridge.** We must explain why a reciprocal instantaneous energy Hessian can produce an asymmetric *averaged* response under continuing drive; distinguish the force and clamped experiments; introduce the complete stiffness budget; and derive the sharp bounds, attaining rotation, and coordinate minimum. These are the project's essential local explanations, not missing chapters the reader must find elsewhere. Ordinary symmetric drag in our model is not odd viscosity.

**Access checked:** selected sections of the complete published PDF, with equations and relevant pages visually inspected. The arXiv record inspected is v1, submitted 30 June 2022. Its numbering must not be mixed with the published version.

## 2. Strang — matrix mechanics and proof preparation

Gilbert Strang, *Introduction to Applied Mathematics*, Wellesley-Cambridge Press (1986). [Author's book page](https://math.mit.edu/~gs/books/itam.html) · [Official detailed contents](https://math.mit.edu/~gs/books/itam_toc.html).

| Sections | Preparation |
|---|---|
| §§1.3–1.5 | Positive matrices, minimum principles, eigenvalues, and dynamics |
| §§2.1–2.2, 2.4 | Equilibrium, constraints, and structural mechanics |
| §2.5 | Least-squares geometry, useful for understanding projection |
| §§6.1–6.2 | Ordinary differential equations and stability |
| §4.1, optional | Periodic functions and orthogonal expansions |

**Why choose it.** The main proof needs weighted inner products, Cauchy–Schwarz, a scalar inverse bound, and elementary linear dynamics. This book connects those mathematical foundations with mechanical equilibrium in one volume. It is the more useful choice if the obstacle is understanding the derivation rather than recognizing its physical significance.

**The remaining bridge.** The listed material does not supply the modern odd-elasticity context, the periodically driven measurement protocol, or our attaining network. The optional infinite-dimensional operator comparison also needs its own domain explanation. A reader already comfortable with matrix analysis may gain less from this route than from option 1.

**Access checked:** the author's description and official section contents, not the complete book. The section-to-project mapping is an informed assessment of those verified topics; full free-text access has not been established.

## 3. Milton — advanced effective-response background

Graeme W. Milton, *The Theory of Composites*, Cambridge University Press (2002). [Author's book page](https://www.math.utah.edu/books/tcbook/) · [Author-hosted complete text](https://www.math.utah.edu/~milton/TheoryCompositesNOPRINT.pdf).

The focused route is §§12.1 and 12.7–12.10, then §§13.1 and 13.4: projections, effective operators, elimination, and variational bounds. Section 12.7 explicitly includes finite-dimensional spaces and a Schur complement. Optional continuations are §18.3 for spectral representations, §§20.1–20.4 for networks, and §§25.3, 25.5–25.6 for equality conditions and attainable bounds. Use section numbers across editions; pagination of the author-hosted reissue need not match every original printing.

**Why choose it.** It gives the strongest conceptual preparation for asking which effective responses are possible and whether equality can be realized. It assumes more mathematical maturity and introduces considerably more material than our projection proof requires.

**The remaining bridge.** The inspected sections do not provide our periodic damped dynamics, separate port experiments, modulation-work account, or mechanical equality family. Replacing spatial position with time is not a justified identification of its constitutive operators with our unbounded time-derivative operator. This makes it a useful advanced alternative, but the least direct teaching anchor of the three.

**Access checked:** the complete author-hosted text was available; selected operator and variational passages in Chapters 12–13 and §18.3 were inspected. The optional network and attainment continuations were located primarily through the detailed contents, with the opening of §25.3 checked. Primary contents and preface records were also consulted. This is a selective assessment, not a claim to have studied the whole book.

## Continue through the local bridge

The [tutorial](TUTORIAL.md) connects the selected review to this sequence:

1. Interpret $`q`$, its conjugate force, the positive energy Hessian $`K(t)`$, and the continuing external modulation.
2. Distinguish constant-force mean compliance from clamped mean stiffness and from wave transmission.
3. Understand why normalization and the spectrum of the **whole network** define the resource being optimized.
4. Follow the weighted-projection proof, then see how the rotating hidden plane attains equality.
5. Interpret the two optima, coordinate minima, load relation, work cost, and ideal-implementation boundary.

The [model](MODEL.md), [proof](PROOF.md), [port-work](PORT_WORK.md), and [realization](REALIZATION.md) notes remain the technical homes of these ingredients. The [background map](MANUSCRIPT_BACKGROUND.md) identifies their external context and attribution. The [documentation map](README.md) connects the complete reading route without requiring a second external textbook.
