# Two reciprocal references and the operator connection

[Home](../README.md) · [Model](MODEL.md) · [Results](RESULTS.md) · [Proof](PROOF.md)

This note sharpens the waveform-resolved bound and makes its relation to established positive-plus-skew operator methods explicit. It changes neither the global stiffness ceiling nor the attaining mechanical architecture. The new statements are derived below; no new general spectral theorem or exhaustive priority claim is made.

## Two reciprocal references

Fix the entire stiffness waveform as a function of phase, $K(\theta)$, with period $2\pi$. Compare schedules $K_\omega(t)=K(\omega t)$ while keeping the ports, damping, and phase dwell fractions fixed. Only the traversal rate changes. The applied force remains constant.

Define the full-matrix static references

$$
\chi_{\mathrm s}=\overline{P^TK^{-1}P},
$$

$$
\chi_{\mathrm f}=P^T\overline K^{-1}P.
$$

Here $\overline K^{-1}$ means the inverse of $\overline K$, not the average of the inverse. Both reference matrices are symmetric. All internal coordinates are retained in each inverse.

The first reference equilibrates at each frozen configuration and averages the response. The second equilibrates under the averaged stiffness. They are respectively the slow-rate and fast-rate limits **of this overdamped model**. They can also be calculated from measured stiffness matrices without operating at extreme rates. Actually realizing the averaged matrix as a static device requires corresponding control capabilities.

Set $a_{\mathrm s}=\operatorname{tr}\chi_{\mathrm s}/2$ and $a_{\mathrm f}=\operatorname{tr}\chi_{\mathrm f}/2$. Every rate obeys

$$
\boxed{\beta^2\leq(\alpha-a_{\mathrm f})(a_{\mathrm s}-\alpha).}
$$

Consequently,

$$
|\beta|\leq\frac{a_{\mathrm s}-a_{\mathrm f}}2.
$$

A positive gap is necessary, not sufficient, for nonreciprocity. The circle is a bound for a fixed waveform, not a claim that changing the speed of every waveform reaches its boundary.

## Short proof by projection

Use $f=(p_1+ip_2)/\sqrt2$ and the periodic response $u$. Then $z=\overline{f^\dagger u}=\alpha-i\beta$. The existing proof gives $\overline{Ku}=f$ and $\overline{u^\dagger Ku}=\alpha$.

Improve the constant reference vector from $f/h$ to

$$
c_*=\overline K^{-1}f.
$$

In the positive inner product $\langle v,w\rangle_K=\overline{v^\dagger Kw}$, set $r=u-c_*$ and $v=K^{-1}f-c_*$. Direct expansion gives

$$
\|r\|_K^2=\alpha-a_{\mathrm f},
$$

$$
\|v\|_K^2=a_{\mathrm s}-a_{\mathrm f},
\qquad \langle v,r\rangle_K=z-a_{\mathrm f}.
$$

Cauchy–Schwarz proves the refined disk. This argument applies to the same bounded, piecewise continuous or measurable coefficients as the original [model](MODEL.md); it needs no differentiability of $K$.

It also identifies the gap exactly:

$$
a_{\mathrm s}-a_{\mathrm f}=\overline{v^\dagger Kv}.
$$

When the gap vanishes, $K^{-1}f=c_*$ almost everywhere. The real and imaginary parts show that both frozen force experiments have a phase-independent equilibrium displacement. The constant solution then works at every rate, so there is no nonreciprocal response.

Finally $a_{\mathrm s}=j$ and $a_{\mathrm f}\geq1/h$ by weighted Cauchy–Schwarz for $\overline K$. The new disk is at least as strong as the earlier disk. Combining it with the same inverse chord bound still gives the existing global ceiling $B_*$. Its attaining family has $a_{\mathrm f}=1/h$, so that ceiling and its equality construction are unchanged.

## Spectral representation and rate limits

This section gives the standard operator explanation of the same result. It also establishes a monotonicity property of the symmetric response. The mathematical strategy has direct predecessors in [R10](SOURCES.md#r10) and [R11](SOURCES.md#r11).

Use the Hilbert space of complex, periodic, square-integrable vector functions, with normalized phase average. Let $D=\Gamma\partial_\theta$ on the periodic Sobolev domain $H^1_{\mathrm{per}}$. It is skew-adjoint because $\Gamma$ is constant symmetric. Let $B=K^{-1/2}$ be the bounded invertible self-adjoint multiplication operator and define

$$
\mathcal H=iBDB.
$$

Its domain is $\{v:Bv\in H^1_{\mathrm{per}}\}$. Bounded invertible self-adjoint congruence preserves the adjoint relation on this domain, so $\mathcal H$ is self-adjoint. This is not the assertion that multiplication by a discontinuous $K^{-1/2}$ preserves $H^1$.

For real nonzero $\omega$, the closed differential operator $\mathcal L_\omega=K+\omega D$ has inverse

$$
\mathcal L_\omega^{-1}=B(I-i\omega\mathcal H)^{-1}B.
$$

At $\omega=0$ use $\mathcal L_0^{-1}=K^{-1}$ directly. The resolvent formula extends to that value as a bounded operator.

The spectral theorem gives a nonnegative scalar measure $\mu$ for the vector $Bf$:

$$
z(\omega)=\int_{\mathbb R}\frac{d\mu(\lambda)}{1-i\omega\lambda}.
$$

Its total mass is $a_{\mathrm s}$. To evaluate its zero-mode mass, observe that the kernel of $\mathcal H$ consists of $K^{1/2}$ times constant vectors. If $V$ embeds a constant vector $c$ as $K^{1/2}c$, then $V^\dagger V=\overline K$. The orthogonal kernel projector is $V\overline K^{-1}V^\dagger$. Therefore

$$
\mu(\{0\})=a_{\mathrm f}.
$$

Dominated convergence now yields the stated slow and fast limits. It does not require a finite Fourier truncation, a discrete spectral sum, or a dimension-dependent remainder. A physically fixed device may cease to be overdamped at large rates; the mathematical limit alone does not validate that extrapolation.

After removing the zero-mode mass, $z-a_{\mathrm f}$ is a positive weighted sum of points on the circle of diameter $[0,1]$, scaled by $a_{\mathrm s}-a_{\mathrm f}$. This recovers the disk and explains its equality conditions.

At a finite nonzero rate with a nonzero gap, equality requires all occupied nonzero spectral weight to be at a single **signed** $\lambda_0$. The absolute cross-response peaks when $|\omega\lambda_0|=1$. The four-coordinate construction meets this condition. This refers to the spectrum seen by the specified probe, not to the absence of all other modes from the full apparatus.

Two distinctions are essential. The spectral weights are nonnegative, but the support $\lambda$ can have either sign. Also, $\omega$ is the modulation rate, not an oscillating probe frequency. The imaginary part of $z$ encodes exchanged spatial cross-responses. The representation does not make it dielectric loss, imply a positive relaxation-time distribution, or establish a Kramers–Kronig claim in this rate variable.

## Symmetric response decreases with speed

Let $\mathcal P$ embed the two measured force directions as constant vector functions. Taking the symmetric part of the real measured compliance gives

$$
\operatorname{sym}\chi(\omega)
=\mathcal P^\dagger B(I+\omega^2\mathcal H^2)^{-1}B\mathcal P.
$$

Spectral functional calculus therefore gives, for $0\leq\omega_1\leq\omega_2$,

$$
\chi_{\mathrm f}\preceq\operatorname{sym}\chi(\omega_2)
\preceq\operatorname{sym}\chi(\omega_1)\preceq\chi_{\mathrm s}.
$$

This is the Loewner order of symmetric matrices. Equivalently, the displacement component along any fixed constant force direction cannot increase when the same waveform is traversed faster. It does not imply monotonicity of $\beta$, of every individual off-diagonal entry, or of dissipated power.

This conclusion requires that only the rate changes. Changing dwell fractions, stiffness amplitudes, damping, or the equilibrium center is not the same comparison. Reversing the rate gives $\chi(-\omega)=\chi(\omega)^T$; the symmetric response is even in rate.

## The worked mechanical example

For the attaining four-coordinate waveform with stiffness spectrum $(1,1,3,3)k_0$,

| Quantity | Value in units of $1/k_0$ |
|---|---:|
| $a_{\mathrm f}$ | 0.577350269190 |
| $a_{\mathrm s}$ | 0.755983064144 |
| Half their gap | 0.089316397477 |
| Direct response at the maximum cross-response | 0.666666666667 |

The two reciprocal references are isotropic. With scalar internal drag $\gamma_y$, the measured complex response can be written

$$
\alpha+i\beta=a_{\mathrm f}
+\frac{a_{\mathrm s}-a_{\mathrm f}}{1-i\omega\tau},
\qquad \tau=\frac{\gamma_y}{\sqrt3k_0}.
$$

For $k_0=\gamma_y=1$, the occupied nonzero spectral value for $z=\alpha-i\beta$ is $-1/\sqrt3$. The optimum is at $\omega=\sqrt3$. This reproduces the existing ceiling; it does not add a larger attainable response.

## Controls that prevent overinterpretation

A static anisotropic stiffness $\operatorname{diag}(1,3)$ has identical reciprocal references. The refined disk collapses to its actual response, while the older $1/h,j$ disk had a positive radius. Thus the refinement removes a spurious allowance without invalidating the original bound.

A scalar modulation through $I,3I,2I$ with equal phase fractions has a positive reference gap but zero antisymmetric response at every speed. Changing the stiffness magnitude alone does not provide a handed sequence. The gap bounds what a waveform can do; it does not guarantee that its dynamics use the available allowance.

Finally, the static operator $2I+J$ has inverse $(2I-J)/5$ and $\beta=-1/5$. Its symmetric part has spectrum $(2,2)$, which would give a zero stiffness-only ceiling. This is not a counterexample to our model: the antisymmetric term acts directly on a constant probe. In our mechanical operator, $D$ annihilates constant vectors. Positivity of a Hermitian part alone is not enough to import the mechanical ceiling into an arbitrary nonsymmetric matrix problem.

## What the literature comparison resolves

Duncan, Lelievre, and Pavliotis [R10](SOURCES.md#r10) obtain the symmetric inverse of a positive-plus-skew generator in their Eq. (29), then a positive spectral expansion with a nonvanishing kernel contribution in Eq. (34) and Theorem 4. This is a direct mathematical predecessor to the representation and monotone symmetric response above. Their observable is a sampling variance, not mechanical cross-compliance. Their operator assumptions differ from ours, so the mechanical domain and zero-mode projection are checked explicitly here rather than imported without translation.

Milton [R11](SOURCES.md#r11) connects projected resolvents to effective material parameters in Section 2 and treats coercive Hermitian plus anti-Hermitian operator parts in Section 5. This is closer than a comparison only with a particular static Hall-effect model. His spectral parameter, projections, and integral representation are not identified automatically with our drive-rate family. His text also points to an extensive preexisting literature; the general technique is not attributed solely to these two references.

The direct comparison now attributes the generic resolvent mechanism to established methods. It does not certify that no earlier theorem already contains the particular stiffness-budget bound and equality construction. The physical realization problem is an additional step: a bounded positive reciprocal multiplication operator, a derivative annihilating the force probes, stationary measured outputs, and positive springs must fit together. Our existing construction supplies that step for the stated class; its priority and significance remain separate questions.

## Evidence and source-access limits

[operator_bridge.py](../checks/operator_bridge.py) is a separately written diagnostic module. It uses exact affine propagation for 12 piecewise-constant waveforms in dimensions 2, 3, 4, and 6, at six rates each, including anisotropic constant damping and reversal tests. A separate finite Fourier implementation checks the spectral and direct inverses against the analytic four-coordinate solution on three odd grids and four rates. Odd grids avoid an artificial zero mode at the Nyquist frequency. The tests are not a general spectral-discretization convergence theorem.

Duncan et al.'s full publisher HTML, including the numbered equations above, was inspected. Milton's 16-page arXiv PDF supplied parsed text; attempts to render its pages through the browser screenshot service failed. No figure, plotted data, or visual verification of that PDF is claimed. The algebra in this note is derived directly, not copied from an ambiguous parsed equation.

This is an author-side derivation and source comparison. It adds no fabricated-device claim, independently reviewed result, or new large simulation campaign.
