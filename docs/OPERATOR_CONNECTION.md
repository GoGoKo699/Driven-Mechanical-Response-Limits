# Operator connection and the slow–fast response budget

[Home](../README.md) · [Model](MODEL.md) · [Results](RESULTS.md) · [Proof](PROOF.md)

## What is established by this comparison

The response disk is a consequence of standard positive-plus-skew operator geometry. It should not be advertised as a new general resolvent inequality. Related weighted spectral representations, separation of the kernel, and symmetric-response monotonicity occur explicitly in the transport and nonreversible-diffusion literature [P1, P2]. Broader effective-operator constructions also include time-dependent media [P3, P4].

Specializing that framework here strengthens the bound for a **fixed mechanical schedule** and explains the attaining device in terms of one active spectral mode. The existing global stiffness ceiling is unchanged. The mechanical realizability, normalized resource optimization, conditional coordinate minimum, and positive-spring architecture remain separate questions; the cited formulas do not by themselves constitute a construction with reciprocal laboratory springs.

This is a theorem-level comparison of inspected sources, not an exhaustive priority determination. All new deductions below are proved locally rather than attributed to a source that states a different physical problem.

## A fixed schedule and its reciprocal endpoints

Fix a real symmetric periodic path $`\mathcal K(\theta)`$, with phase period one and $`mI\preceq\mathcal K\preceq MI`$. Preserve its phase weights and change only its speed:

```math
K_v(t)=\mathcal K(vt),\qquad v>0.
```

Thus the physical period is $`1/v`$. The probe remains constant, and damping $`\Gamma`$ remains constant positive symmetric. A bar below denotes a phase average, independent of $`v`$. Ports are the same normalized conjugate pairs as in the [model](MODEL.md).

Two reciprocal endpoint matrices are

```math
\chi_{\rm slow}=P^T\overline{\mathcal K^{-1}}P,
```

```math
\chi_{\rm fast}=P^T(\overline{\mathcal K})^{-1}P.
```

For a fixed piecewise-continuous uniformly positive schedule they are the limiting mean responses as $`v\to0`$ and $`v\to\infty`$, respectively. The first lets the full network relax at each phase before averaging. The second averages the full stiffness before inversion. Neither uses the inverse of a two-by-two measured block in place of the full inverse.

Define their mean direct compliances

```math
a_{\rm s}=\tfrac12\,\mathrm{tr}\,\chi_{\rm slow},\qquad
a_{\rm f}=\tfrac12\,\mathrm{tr}\,\chi_{\rm fast}.
```

The physical target at intermediate speed remains $`\alpha(v)=\mathrm{tr}\,\chi(v)/2`$ and $`\beta(v)=(\chi_{21}(v)-\chi_{12}(v))/2`$.

## Fixed-schedule disk

For every positive finite speed,

```math
\boxed{\beta(v)^2\leq[\alpha(v)-a_{\rm f}][a_{\rm s}-\alpha(v)].}
```

In particular,

```math
|\beta(v)|\leq\frac{a_{\rm s}-a_{\rm f}}2.
```

The right endpoint is $`a_{\rm s}=j`$ from the original proof. The left endpoint obeys $`a_{\rm f}\geq1/h`$, so the new disk is never weaker and can be strictly smaller for a specified path. The difference between the two endpoint compliances is a response budget, not a promise that a particular path uses it nonreciprocally.

For example, a static anisotropic stiffness has equal slow and fast responses and hence zero budget. Its old scalar-$`h`$ disk may have nonzero width: that larger disk was a bound over fewer specified details, not a false prediction of static nonreciprocity.

### Proof by projection onto all constant displacements

Let $`f=(p_1+ip_2)/\sqrt2`$ and let $`u(\theta)`$ solve

```math
v\Gamma u'+\mathcal Ku=f.
```

Use the phase-averaged inner product $`\langle a,b\rangle_{\mathcal K}=\overline{a^\dagger\mathcal Kb}`$. The original balances give $`\overline{\mathcal Ku}=f`$ and $`\|u\|_{\mathcal K}^2=\alpha`$. Put

```math
u_0=(\overline{\mathcal K})^{-1}f,
```

where $`u_0`$ is a constant displacement, and define $`r=u-u_0`$ and $`w=\mathcal K^{-1}f-u_0`$. Then

```math
\|r\|_{\mathcal K}^2=\alpha-a_{\rm f},\qquad
\|w\|_{\mathcal K}^2=a_{\rm s}-a_{\rm f},
```

```math
\langle w,r\rangle_{\mathcal K}=\alpha-i\beta-a_{\rm f}.
```

Cauchy–Schwarz gives the displayed disk. This uses all constant-coordinate test functions rather than projecting only along $`f`$; no new dynamical hypothesis is needed. Cauchy–Schwarz also gives $`(f^\dagger\overline{\mathcal K}f)(f^\dagger(\overline{\mathcal K})^{-1}f)\geq1`$, proving $`a_{\rm f}\geq1/h`$.

This proof is sufficient for the bound. The following operator reconstruction supplies the connection to prior methods, the endpoint limits, and the equality interpretation.

## Exact positive-plus-skew reduction

Work on the complexified phase space $`L^2_{\rm per}([0,1];\mathbb C^n)`$ with normalized phase measure. Let $`A`$ be multiplication by $`\mathcal K`$, and let $`D=\Gamma\partial_\theta`$ on periodic $`H^1`$ functions. Then $`A`$ is bounded coercive selfadjoint and $`D`$ is skew-adjoint. Define

```math
T=-iA^{-1/2}DA^{-1/2},\qquad q=A^{-1/2}f.
```

The domain of $`T`$ consists of vectors $`\psi`$ for which $`A^{-1/2}\psi`$ lies in periodic $`H^1`$. Bounded invertibility of $`A^{-1/2}`$ makes this a selfadjoint congruence of $`-iD`$; no differentiability of a piecewise stiffness square root is assumed. The forcing vector $`q`$ only needs to belong to $`L^2`$ for the resolvent below to act on it. This domain qualification is important: $`T`$ need not be a bounded matrix or bounded operator.

The measured complex scalar is exactly

```math
z(v)=\alpha(v)-i\beta(v)
=\langle q,(I+ivT)^{-1}q\rangle.
```

The kernel of $`T`$ consists of $`A^{1/2}`$ times constant vectors. The orthogonal projection of $`q`$ onto that kernel is $`q_0=A^{1/2}u_0`$, with

```math
\|q_0\|^2=a_{\rm f},\qquad
\|q-q_0\|^2=a_{\rm s}-a_{\rm f}=:\rho.
```

The spectral theorem therefore gives a positive finite measure $`\mu`$ on the nonzero real spectrum such that

```math
z(v)=a_{\rm f}+\int_{\lambda\ne0}\frac{d\mu(\lambda)}{1+iv\lambda},
```

```math
\mu(\mathbb R\setminus\{0\})=\rho.
```

The spectral measure depends on the complete stiffness path, constant damping, and chosen two-port complex force. It is not a probability distribution of thermodynamic states or a density of ordinary vibration frequencies. No stochastic dynamics is imported from the comparison papers.

Bounded convergence gives $`z(0^+)=a_{\rm s}`$ and $`z(+\infty)=a_{\rm f}`$. Polarization of the real and imaginary two-port forms gives the endpoint matrices above. This argument controls the limits within the overdamped model; taking infinite speed in a physical apparatus can invalidate neglected inertia or controller assumptions.

## The disk and equality are resolvent geometry

For every real $`y`$,

```math
\left|\frac1{1+iy}-\frac12\right|=\frac12.
```

Thus every nonzero spectral component lies on the same circle. A positive weighted average lies inside its disk. Translating by $`a_{\rm f}`$ and scaling by $`\rho`$ gives the fixed-schedule bound.

More precisely, set $`d\nu=d\mu/\rho`$ when $`\rho>0`$, $`g_v(\lambda)=(1+iv\lambda)^{-1}`$, and $`\bar g=\int g_v\,d\nu`$. Then

```math
(\alpha-a_{\rm f})(a_{\rm s}-\alpha)-\beta^2
=\rho^2\int|g_v-\bar g|^2d\nu.
```

At a positive finite speed, equality at a nontrivial boundary point requires the force-coupled spectral measure to be supported at one nonzero value of $`\lambda`$. Degenerate eigenvectors at that same value are permitted. This is not a claim that the whole device has only one normal mode.

Opposite signed spectral values give opposite handed cross-responses and can cancel. Multiple distinct response factors move the weighted average inside the circle. Neither extra internal coordinates nor more Fourier harmonics automatically improve the response.

The four-coordinate construction already in the repository has a single active nonzero spectral value for the complex force used above. In its constant rotating-frame equations,

```math
A_0=\begin{pmatrix}hI&bI\\bI&gI\end{pmatrix},\qquad
D_0=\mathrm{diag}(0,-\gamma_yJ).
```

In this finite reduction the operator is $`A_0+\Omega D_0`$, where $`\Omega`$ is the coupling angular frequency. The force lies in $`\ker D_0`$. The active value is $`\lambda_* =\gamma_y h/(mM)`$, the slow endpoint is $`g/(mM)`$, and the fast endpoint is $`1/h`$. Thus its response traces the circle exactly. In the period-one phase convention used above, $`\Omega=2\pi v`$ and the active spectral value is multiplied by $`2\pi`$; the product of rate and spectral value is unchanged. This is a modal explanation of the existing equality construction, not an additional device or an optimality claim based on fitting a one-pole curve.

## Speed dependence of the reciprocal part

Taking the Hermitian part gives

```math
\mathrm{Herm}(I+ivT)^{-1}=(I+v^2T^2)^{-1}.
```

It decreases in the positive-operator order as $`v`$ increases. Projecting back to the physical force/displacement ports gives, for $`0<v_1<v_2`$,

```math
\mathrm{Sym}\,\chi(v_1)\succeq\,\mathrm{Sym}\,\chi(v_2),
```

and in particular $`\alpha(v)`$ is nonincreasing. This is the same positive/skew mechanism behind the symmetric-resolvent comparison in [P2, Lemma 3 and Theorem 4], specialized to changing the speed of a fixed stiffness schedule. It is not claimed as a new general monotonicity theorem.

The antisymmetric response is different: it vanishes at both limiting speeds, and it can peak or change sign between them. A positive endpoint gap is necessary but not sufficient for a nonzero response. A two-contiguous-stage schedule has the same reversal as a phase shift and remains reciprocal, despite a possible nonzero gap.

These statements require changing **only** the phase speed. They do not hold by this argument when the waveform, phase weights, damping, or load is also altered with speed. They concern modulation speed under a steady probe, not a harmonic probe-frequency sweep. Monotone direct response does not prohibit dissipation resonances, inertial resonance, or gain in another physical model.

## A finite check using the existing design

For the worked interval $`[1,3]`$ and its optimal allocation,

| Quantity | Value in units with $`k_0=1`$ |
|---|---:|
| $`a_{\rm s}`$ | 0.755983064144 |
| $`a_{\rm f}`$ | 0.577350269190 |
| $`(a_{\rm s}-a_{\rm f})/2`$ | 0.089316397477 |
| Optimum $`\alpha`$ | 0.666666666667 |
| Optimum $`\beta`$ | 0.089316397477 |

Half the difference of the reciprocal endpoints is exactly the attained global spectral ceiling. This may be useful as a design diagnostic because the endpoints have direct limiting-response interpretations. Finite-speed endpoint measurements need convergence and error bounds; two arbitrary rate measurements cannot be substituted for the limits and called a certified ceiling.

The code also checks a two-stage schedule with endpoint gap 0.055329562310 but zero antisymmetric response, and a static anisotropic system for which the stronger endpoint disk collapses to a point. Finally it checks an excluded static skew-force model: positivity of the restoring part alone does not give our disk when the dynamics acts directly on the forced constant subspace. The condition $`Df=0`$ is essential in the generic operator formulation.

## The exact inverse-gap constants are established

Moslehian, Nakamoto, and Seo [P5, Theorem 2.1(i)] prove an operator Klamkin–McLenaghan inequality for positive maps. Its specialization gives both dimensional resource constants used here. They are not new general inequalities.

Let $`\mathcal A`$ be multiplication by $`\mathcal K`$ and let $`\Phi`$ be compression onto all constant trajectories, so $`\Phi(\mathcal A)=\overline{\mathcal K}`$. In their notation take $`A=\mathcal A`$, $`B=\mathcal A^{-1}`$, and lower/upper constants $`1/M,1/m`$. Their hypothesis holds, $`A\mathbin{\#}B=I`$, and the conclusion is

```math
\overline{\mathcal K^{-1}}-(\overline{\mathcal K})^{-1}
\preceq(1/\sqrt m-1/\sqrt M)^2I.
```

Projection to the measured plane and the fixed-schedule disk give $`|\beta|\leq B_*`$. No derivative-operator assumption enters this published gap inequality.

There is a dual substitution for the clamped experiment. At each phase take their $`A=K^{-1}`$, $`B=K`$, constants $`m,M`$, and $`\Phi`$ as compression to measured coordinates. Write the mechanical blocks as $`K_{xx},B,C`$ and $`S=K_{xx}-BC^{-1}B^T`$. Since $`\Phi(K^{-1})=S^{-1}`$, the same theorem gives

```math
BC^{-1}B^T=K_{xx}-S
\preceq(\sqrt M-\sqrt m)^2I_2.
```

The clamped projection proof then gives the existing odd-stiffness ceiling. These are explicit applications of [P5]; the local proofs remain useful for self-contained reading.

The full spectral lens follows from the inverse chord, the disk, and scalar optimization. The normalized-asymmetry ceiling follows by enclosing that lens in a sector. We have not located an inspected source printing this exact mechanical formulation, but neither consequence should be advertised as a new foundational operator method. The scientific question is admissible mechanical attainment with the stated ports and resources.

## Direct primary-source comparison

### P1 — spectral transport framework

G. A. Pavliotis, *Asymptotic analysis of the Green–Kubo formula*, IMA Journal of Applied Mathematics **75**, 951–967 (2010), [arXiv:1002.4103](https://arxiv.org/abs/1002.4103), [publisher record](https://doi.org/10.1093/imamat/hxq039).

The inspected Section 3 separates a generator into symmetric and antisymmetric parts, uses a weighted inner product, separates the kernel, and derives spectral formulas for both symmetric and antisymmetric response; see Eqs. (3.2), (3.6), (3.8), and Proposition 3.4. This is a direct methodological predecessor, not merely a shared keyword. Its stated spectral construction assumes a bounded transformed operator at the relevant step; our periodic derivative can be unbounded, and the domain argument above must be supplied rather than silently applying that hypothesis. Diffusion coefficients are not automatically our force–displacement observables.

### P2 — symmetric resolvents and speed monotonicity

A. B. Duncan, T. Lelièvre, and G. A. Pavliotis, *Variance Reduction Using Nonreversible Langevin Samplers*, Journal of Statistical Physics **163**, 457–491 (2016), [full publisher text](https://doi.org/10.1007/s10955-016-1491-2).

Lemma 3, Eq. (29), rewrites the symmetric part of the inverse of a symmetric-plus-antisymmetric generator. Section 3.3 and Theorem 4 give a positive spectral expansion and identify the kernel contribution. These reproduce the generic algebra used in our direct-response monotonicity after matching signs and the inner product. The source optimizes sampling variance in a specified diffusion class, not reciprocal elastic realization or the stiffness-budget ceiling.

### P3 — general effective-operator embedding

G. W. Milton, *A unifying perspective on linear continuum equations prevalent in science. Part V: resolvents; bounds on their spectrum; and their Stieltjes integral representations when the operator is not selfadjoint*, [arXiv:2006.03162](https://arxiv.org/abs/2006.03162) (2020).

Sections 4–5, including Eqs. (4.3)–(4.7) and Theorem 1, describe Hermitian embeddings and spectral integral representations of non-Hermitian effective operators. Our positive-plus-skew normalization is consistent with that established framework. The fact that a circular region has been derived is not sufficient novelty evidence. No claim is made that the complete theorem is excluded from every consequence of this framework.

### P4 — time-dependent material laws

G. W. Milton, *A unifying perspective on linear continuum equations prevalent in physics. Part III: Canonical forms for dynamic equations with moduli that may, or may not, vary with time*, [arXiv:2006.02432](https://arxiv.org/abs/2006.02432) (2020).

Its introductory formulation explicitly covers time-dependent moduli, and Section 7 explains why physically changing material parameters can generate extra coupling terms. Thus describing our coefficients as time dependent does not by itself place the problem outside effective-operator theory. Our guided-spring derivation and its no-moving-equilibrium assumption must still be evaluated on their own physical merits. The paper's examples are not an automatic fabrication of our network.

### P5 — the exact inverse-gap budget

M. S. Moslehian, R. Nakamoto, and Y. Seo, *A Diaz–Metcalf type inequality for positive linear maps and its applications*, Electronic Journal of Linear Algebra **22**, 179–190 (2011), [journal article](https://doi.org/10.13001/1081-3810.1433), [primary full PDF](https://journals.uwyo.edu/index.php/ela/article/download/867/867/867).

Theorem 2.1(i), journal p. 180, and its proof Eq. (2.8) were inspected in the full primary text. The two substitutions above identify the precise inherited constants; the paper is not cited as a spring-device construction.

### Source-access limits

The publisher's full HTML for P2 and the parsed primary PDF texts for P1, P3, and P4 were available on 30 September 2026. For that P1–P4 comparison, PDF screenshot calls and attempts at local rendering failed. The later P5 comparison used its accessible full journal PDF. No visual figure, table, or unrendered symbol is used as evidence for a new claim; the operator identities are independently stated and derived above. P1's displayed body date differs from its arXiv submission and journal dates; bibliographic dating follows the latter. No full citation-network search or expert priority determination was completed.

## Consequence for the research claim

The abstract disk, its positive-measure interpretation, the monotonicity mechanism, and the two inverse-gap constants are established operator consequences. The project should not count each as an independent foundational discovery. This comparison does not invalidate the mechanical theorem or show that the complete sharp physical construction is already published.

The contribution retained by the [scope decision](RESEARCH_STATUS.md) is the resource-matched mechanical result: an optimum over arbitrary reciprocal positive periodic networks, a small attaining architecture with stationary measured outputs, and an explicit positive-spring realization in its stated range. A prior source supplying that combination or a rigorous reduction to it would affect originality; a similar circle alone does not settle the comparison. Conversely, a distinct mechanical vocabulary does not make a standard inequality new.

The additional fixed-schedule result is useful for explaining and checking the same device. It is not an invitation to begin a separate stochastic-transport project, add quantum assumptions, or replace the current stiffness budget. The [existing source guide](SOURCES.md) retains the implementation and assumption-provenance limitations.

## Reproduction

Run `python checks/operator_comparison.py --output operator-results.local.json`, or the main [runner](REPRODUCIBILITY.md). The four subgroups contain 156 finite diagnostic cases: exact positive/skew resolvents, piecewise-constant periodic force responses at changing speeds, necessity controls, and the single-mode attaining example. The tests use small matrices and exact stage exponentials; they do not enumerate arbitrary networks or prove priority. Existing benchmark references and the two preserved scientific modules are unchanged.
