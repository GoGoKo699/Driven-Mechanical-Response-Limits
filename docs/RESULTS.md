# Results and exact scope

[Home](../README.md) · [Model](MODEL.md) · [Proof](PROOF.md) · [Realization](REALIZATION.md)

## Resource-resolved disk

Under the [model](MODEL.md), any finite-dimensional periodic network satisfies

$$
\beta^2\leq(\alpha-1/h)(j-\alpha).
$$

In particular $1/h\leq\alpha\leq j$. The disk is a statement about two scalar response quantities, not every entry of the full compliance matrix. Its proof is [one weighted projection argument](PROOF.md#weighted-projection).

## Two reciprocal endpoints

For a fixed phase waveform, let $\chi_{\mathrm s}=\overline{P^TK^{-1}P}$ and $\chi_{\mathrm f}=P^T\overline K^{-1}P$. These are symmetric static reference compliances, with $a_{\mathrm s,f}=\operatorname{tr}\chi_{\mathrm s,f}/2$. Then

$$
\beta^2\leq(\alpha-a_{\mathrm f})(a_{\mathrm s}-\alpha).
$$

Here $a_{\mathrm s}=j$ and $a_{\mathrm f}\geq1/h$, so this is a stronger per-waveform disk. When only the traversal rate increases, the symmetric response decreases in the Loewner order from $\chi_{\mathrm s}$ toward $\chi_{\mathrm f}$. This is a limit within the overdamped model, not a promise of valid arbitrarily fast operation in a fixed apparatus. The [derivation, equality conditions, and source comparison](OPERATOR_BRIDGE.md) keep this distinction explicit.

## Spectral ceiling

When only the complete stiffness interval $[m,M]$ is fixed,

$$
|\beta|\leq B_*,
$$

$$
B_*=\frac12\left(\frac1{\sqrt m}-\frac1{\sqrt M}\right)^2.
$$

The bound is independent of internal dimension, waveform, and period. It holds for every constant positive symmetric damping matrix. A four-coordinate family with suitable internal drag attains it. Sharpness for each separately fixed anisotropic damping tensor or sparse graph is not claimed.

Writing $D=mM$ and $k=(m+M)/2$, the spectral response envelope is

$$
(\alpha-k/D)^2+(|\beta|+1/\sqrt D)^2\leq k^2/D^2.
$$

The four-coordinate family reaches each nonzero-$\beta$ boundary point. Endpoints with $\beta=0$ can also be realized statically. No full-tensor realizability statement is inferred from this two-scalar envelope.

## Fixed measured stiffness

If $h=k$ is fixed as an additional budget, put $a=(M-m)/2$. Then

$$
\beta^2\leq(\alpha-1/k)(k/D-\alpha),
$$

$$
|\beta|\leq\frac{a^2}{2kD}.
$$

This recovers the planar fixed-trace bound even with arbitrarily many internal coordinates. Uniform planar rotation is an attaining member for scalar damping. A fixed trace of the **whole** network is not a substitute for fixed $h$.

## Attaining four-coordinate family

Let $x,y\in\mathbb R^2$ be measured and internal coordinates. For $m<h<M$, choose

$$
g=m+M-h,\qquad b^2=(M-h)(h-m).
$$

Use $R(t)=\exp(\Omega tJ)$ and

$$
K(t)=\begin{pmatrix}hI_2&bR(t)\\bR(t)^T&gI_2\end{pmatrix}.
$$

Its exact spectrum is $(m,m,M,M)$. Take damping $\operatorname{diag}(\Gamma_x,\gamma_yI_2)$, with $\Gamma_x$ positive symmetric and $\gamma_y>0$. The response has the form $\chi=\operatorname{Re}C\,I_2+\operatorname{Im}C\,J$, where

$$
C=\frac{g-i\nu}{D-ih\nu},\qquad \nu=\gamma_y\Omega.
$$

For fixed $h$, $|\nu|=D/h$ maximizes $|\beta|$. The global optimum uses

$$
h=\sqrt D,\qquad |\Omega_*|=\sqrt D/\gamma_y.
$$

Its positive-orientation response is

$$
\chi_*=\frac{m+M}{2mM}I_2+B_*J.
$$

The [realization](REALIZATION.md#stationary-outputs-and-static-loads) derives the exact static load law and modulation-power balance. The measured coordinates are stationary; the internal ones rotate.

## Conditional coordinate minimum

Suppose a network attains $B_*>0$, its two measured coordinates are stationary for **every** constant input force, and its constant damping has no measured/internal cross-block. It needs at least two internal coordinates, hence at least four total coordinates. The family above attains that conditional minimum.

This is not a minimum spring count or a prohibition on three-coordinate nonreciprocity. The [proof and suboptimal control](PROOF.md#coordinate-minimum) retain the extra assumptions explicitly.

## Geometry and tolerance

For the worked interval $[k_0,3k_0]$, eight strictly positive modulated axial springs and four positive fixed support springs realize the attaining tangent stiffness on ideal perpendicular guides. The proposed layout has fixed rest lengths, no prestress at the reference origin, and no moving guides. Finite-amplitude motion obeys nonlinear spring geometry and is not subject to the original exact linear budget without further analysis.

For the same damping and ports, if $\widetilde K=K+E$, $\|E\|\leq\delta$, and $\widetilde K\succeq\widetilde mI>0$, then

$$
\|\widetilde\chi-\chi\|\leq\frac{\delta}{m\widetilde m}.
$$

Relative errors at most $\varepsilon<1$ in all positive rank-one spring coefficients give

$$
|\widetilde\beta-\beta|\leq\frac{\varepsilon M}{m^2(1-\varepsilon)}.
$$

This is a coefficient-error bound, not tolerance to arbitrary damping, prestress, geometric, or controller errors. The perturbed stiffness spectrum may exceed the original budget. See [the proof](PROOF.md#coefficient-errors).

## Research boundaries

No energy-efficiency optimum, inertial extension, autonomous controller, experimentally measured performance, or universal bulk odd-elasticity theorem is established. The [literature comparison](SOURCES.md) keeps the relation to broader operator/effective-response results open. Evidence for universal statements is the proof, not the size of the numerical test suite.
