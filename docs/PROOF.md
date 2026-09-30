# Proof of the response bounds and equality construction

[Model](MODEL.md) · [Statements](RESULTS.md) · [Checks](REPRODUCIBILITY.md#claim-map)

## Weighted projection

Use the normalized complex force $f=(p_1+ip_2)/\sqrt2$. This combines two real experiments; it is not an extra physical input. Let $u(t)$ be its periodic response and set

$$
z=\overline{f^\dagger u}=\alpha-i\beta.
$$

Averaging the equation gives $\overline{f^\dagger Ku}=1$. Multiplication by $u^\dagger$, taking real parts, and averaging gives $\overline{u^\dagger Ku}=\alpha$. Constancy and symmetry of $\Gamma$ make the derivative term a periodic boundary term in the latter identity.

Define $\langle v,w\rangle_K=\overline{v^\dagger Kw}$ and put

$$
r=u-f/h,\qquad v=K^{-1}f-f/h.
$$

Direct expansion yields

$$
\|r\|_K^2=\alpha-1/h,\qquad \|v\|_K^2=j-1/h,
$$

$$
\langle v,r\rangle_K=z-1/h.
$$

Cauchy–Schwarz implies

$$
|z-1/h|^2\leq(j-1/h)(\alpha-1/h),
$$

which rearranges to

$$
\beta^2\leq(\alpha-1/h)(j-\alpha).
$$

Both norm identities also handle the degenerate case $j=1/h$, when $\alpha=1/h$ and $\beta=0$. No slow-drive expansion, Fourier truncation, or restriction on dimension has been used.

## Removing the waveform

For $\lambda\in[m,M]$, convexity of the inverse gives

$$
\lambda^{-1}\leq\frac{m+M-\lambda}{mM}.
$$

Apply this eigenvalue by eigenvalue to the symmetric matrix $K(t)$, project with $f$, and average:

$$
j\leq\frac{m+M-h}{D},\qquad D=mM.
$$

The disk therefore yields

$$
|\beta|\leq\tfrac12\left(\frac{m+M-h}{D}-\frac1h\right).
$$

The derivative in $h$ vanishes at $h=\sqrt D$ and the second derivative is negative. Substitution gives $B_*$. Keeping $h=k=(m+M)/2$ instead gives the fixed-measured-budget result.

At fixed $\alpha$, maximize

$$
(\alpha-1/h)\left((m+M-h)/D-\alpha\right)
$$

over the admissible $h$. The maximizing value is $h=\sqrt{(m+M)/\alpha-D}$. Rearrangement gives the [spectral envelope](RESULTS.md#spectral-ceiling). Its real-axis range is $1/M\leq\alpha\leq1/m$.

These are applications of standard projection and scalar inverse bounds. The [explicit positive-map comparison](OPERATOR_CONNECTION.md#the-exact-inverse-gap-constants-are-established) identifies a published theorem giving the exact optimized inverse-gap constant. The proposed scientific statement is the mechanical response consequence and attaining architecture.

## Attainment

For the [four-coordinate family](RESULTS.md#attaining-four-coordinate-family), each frozen block has trace $h+g=m+M$ and determinant $hg-b^2=D$. Orthogonal rotation of the internal plane gives spectrum $(m,m,M,M)$.

Introduce the rotating internal variable $w=Ry$. The exact laboratory equations become

$$
\Gamma_x\dot x+hx+bw=F,
$$

$$
\gamma_y\dot w+(gI_2-\nu J)w+bx=0.
$$

This coordinate change is a calculation, not a physical rotation of the guides or a nonreciprocal primitive inserted into $K$. The unique attracting response has constant $x,w$. Elimination of $w$ gives

$$
G_{\rm dc}=hI_2-b^2(gI_2-\nu J)^{-1},\qquad \chi=G_{\rm dc}^{-1}.
$$

Identifying $J$ with multiplication by $i$ gives $C=(g-i\nu)/(D-ih\nu)$. In particular,

$$
\beta=\frac{b^2\nu}{D^2+h^2\nu^2}.
$$

Its largest magnitude is $b^2/(2hD)$ at $|\nu|=D/h$. Choosing $h=\sqrt D$ attains $B_*$. For fixed $h$, varying $\nu$ traces the disk boundary with endpoints $1/h$ and $g/D$. For a nonzero boundary point of the outer envelope, take the maximizing $h$ above and

$$
\nu=\frac{D\beta}{h(\alpha-1/h)}.
$$

This constructs the claimed envelope boundary without asserting a full-tensor classification.

## Coordinate minimum

Assume exact global attainment with stationary measured coordinates for all constant forces, and no measured/internal damping cross-block. Choose coordinates with the measured plane first, and $f=(1,i,0,\ldots)^T/\sqrt2$.

Attainment forces equality in the scalar optimization, inverse chord, and projection. Thus $h=\sqrt D$, $j=(m+M-h)/D$, and

$$
u=f/h+\lambda(K^{-1}f-f/h),\qquad \lambda=(1\mp i)/2.
$$

Here $u$ is the complex response, not a scalar frequency. Substituting into the differential equation, without differentiating $K$, gives

$$
\Gamma\dot u=(1-\lambda)(f-Kf/h).
$$

The measured derivative is zero. Block-diagonal damping implies $K_{xx}f_x=hf_x$. Reality and the independent real and imaginary parts of $f_x$ give $K_{xx}=hI_2$ almost everywhere.

The operator

$$
B_K=(m+M)I-K-DK^{-1}
$$

is positive semidefinite. Its averaged quadratic form on $f$ vanishes at equality, hence $B_Kf=0$ almost everywhere. Projecting this relation gives $P^TK^{-1}f=jf_x$. The measured response is therefore exactly $\chi=\alpha I_2+\beta J$.

Write the hidden response as $y=Y(t)F$. The stationary measured equation reads

$$
I_2=h\chi+K_{xy}Y(t).
$$

But

$$
\det(I_2-h\chi)=(1-h\alpha)^2+(h\beta)^2>0.
$$

Thus $K_{xy}Y$ has rank two and there must be at least two internal coordinates. The four-coordinate construction satisfies these conditions.

For comparison, three coordinates can have a smaller stationary nonreciprocal response. Let $v=r(\cos t,\sin t)^T$, take one internal coordinate with $y=v^Tx$, and define

$$
K_{xy}=-(gv+\dot v),\qquad K_{yy}=g,
$$

$$
K_{xx}=hI_2+gvv^T+(\dot v v^T+v\dot v^T)/2.
$$

With scalar internal drag one, the port relation is $F=(hI_2-r^2J/2)x$. At $h=2,g=1,r=1/4$ the matrix is positive and the response is below its own spectral ceiling. The check is a control against a stronger, false minimum claim.

## Coefficient errors

For identical damping and forcing, set $z=\widetilde q-q$. Then

$$
\Gamma\dot z+Kz=-E\widetilde q.
$$

The period-averaged energy balances, with normalized time norms, imply

$$
\|\widetilde q\|_{L^2}\leq\|F\|/\widetilde m,
$$

$$
\|z\|_{L^2}\leq\delta\|F\|/(m\widetilde m).
$$

Projection and averaging are contractions, proving the compliance-error bound. Relative errors bounded by $\varepsilon$ in positive rank-one spring coefficients yield

$$
(1-\varepsilon)K\preceq\widetilde K\preceq(1+\varepsilon)K.
$$

Use $\delta=\varepsilon M$ and $\widetilde m=(1-\varepsilon)m$. The antisymmetric part of a two-by-two error matrix has norm $|\widetilde\beta-\beta|$, bounded by the full operator norm.

## Parallel-guide obstruction

For scalar difference springs with nonnegative coefficients, grounded nonnegative springs, and diagonal positive drag, $-\Gamma^{-1}K(t)$ has nonnegative off-diagonal entries. Its transition operator is entrywise nonnegative: approximate by products of sufficiently small forward steps, or exponentials of piecewise constant matrices, and pass to the limit.

A constant nonnegative force applied from the distant past gives nonnegative displacement. Positive uniform stiffness ensures convergence. Hence the full individual-node compliance is entrywise nonnegative and cannot have exchanged cross-terms of opposite sign.

This permits unequal **positive** cross-responses. It does not cover collective signed ports, nonlocal damping, or the perpendicular-guide geometry used here.
