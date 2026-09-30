# A scale-free comparison of the two mechanical responses

[Model](MODEL.md) · [Force-response theorem](RESULTS.md) · [Clamped response and work](PORT_WORK.md)

This note compares the existing force-controlled and displacement-controlled results on a common scale. It does not replace their different operational objectives. A large displacement response can result from softness; a large reaction coefficient can result from stiffness. The dimensionless measure used below is an established matrix asymmetry index [N1], not a newly invented nonreciprocity measure.

The additional mechanical result is a sharp stiffness-contrast bound on that index for **both** experiments. For devices whose measured outputs are stationary, it also gives a joint bound showing why the two separate dimensional maxima cannot be reached simultaneously. The argument is a consequence of the existing projection bounds, with arbitrary complex probe directions retained instead of only one particular combination.

## 1. The common quantity

For a real two-by-two response matrix $`Q`$, let

```math
S_Q=(Q+Q^T)/2,\qquad A_Q=(Q-Q^T)/2.
```

The symmetric part of either response considered here is positive definite. Define

```math
\mathfrak a(Q)=\left\|S_Q^{-1/2}A_QS_Q^{-1/2}\right\|_2.
```

Equivalently, it is the least $`s\geq0`$ such that $`sS_Q+iA_Q`$ is positive semidefinite. This is the convention of Brandner and Seifert [N1, Eq. (15)], specialized to a positive-definite symmetric part. In two dimensions,

```math
\mathfrak a(Q)=\frac{|Q_{21}-Q_{12}|}{2\sqrt{\det S_Q}}.
```

It is zero exactly when the response is reciprocal. It can exceed one in other resource regimes; it is not a probability, an efficiency, a transmission isolation ratio, or a universal measure of every nonreciprocal phenomenon.

For an isotropic symmetric response, $`Q=aI+bJ`$, it reduces to $`|b|/a`$. For an anisotropic response, replacing the denominator by half the trace would change the measure and generally underestimate it.

Real invertible congruence preserves the index:

```math
\mathfrak a(TQT^T)=\mathfrak a(Q).
```

This is the transformation relevant to paired force/displacement changes that preserve power. Changing units or adding an ideal reciprocal coordinate transformer therefore does not inflate this index. The stiffness eigenvalue budget must still be specified in the original physical coordinate normalization.

Inversion also preserves the index:

```math
\mathfrak a(Q^{-1})=\mathfrak a(Q).
```

One proof uses $`S_{Q^{-1}}=Q^{-T}S_QQ^{-1}`$ and $`A_{Q^{-1}}=-Q^{-T}A_QQ^{-1}`$, with the congruence definition. These algebraic properties are not new physics. In particular, they do **not** imply that two different physical experiments produce inverse matrices.

## 2. Sharp bound for either experiment

Keep the complete stiffness interval and all other assumptions of the [model](MODEL.md): $`0<mI\preceq K(t)\preceq MI`$, fixed conjugate ports, constant positive symmetric damping, prescribed periodic stiffness, and a fixed equilibrium. The two matrices are the force-controlled mean compliance $`\chi`$ and the independently defined clamped mean reaction $`G`$.

Put

```math
k=(m+M)/2,\qquad D=mM.
```

Then

```math
\boxed{\mathfrak a(\chi),\ \mathfrak a(G)\ \leq\mathfrak a_*},
```

```math
\mathfrak a_*=\frac{(M-m)^2}{4(M+m)\sqrt{mM}}.
```

The bound depends only on the contrast $`M/m`$, not on the common stiffness scale, waveform, internal dimension, or traversal rate. As before, a suitable four-coordinate family attains it; attainment for each separately fixed damping tensor or topology is not asserted.

This bound covers anisotropic measured response. It is stronger than simply maximizing $`|\beta|/\alpha`$ for the isotropic example. No assumption $`G=\chi^{-1}`$ is needed to bound the two experiments separately.

### Full numerical-range proof for force response

Take any complex unit vector $`e\in\mathbb C^2`$ and use $`f=Pe`$. The [weighted projection proof](PROOF.md#weighted-projection) uses only $`\|f\|=1`$, not the special choice $`f=(p_1+ip_2)/\sqrt2`$. Write $`z=e^\dagger\chi e=x+iy`$ and

```math
h=\overline{f^\dagger Kf},\qquad j=\overline{f^\dagger K^{-1}f}.
```

It gives $`y^2\leq(x-1/h)(j-x)`$, while $`j\leq(m+M-h)/D`$. Maximizing over $`h`$ gives

```math
D|z|^2-(m+M)x+2\sqrt D\,|y|+1\leq0.
```

Thus the complete numerical range, not just its center and vertical endpoint, lies in the same spectral lens already derived for one force combination. The symmetric part is positive because $`x\geq1/h>0`$ for every $`e`$.

### Corresponding clamped proof

Partition $`K`$ into measured block $`A`$, coupling $`B`$, and hidden block $`C`$ as in [the clamped note](PORT_WORK.md). Fix an arbitrary complex unit measured displacement $`e`$ and write $`z=e^\dagger Ge=x+iy`$. The existing projection argument gives

```math
y^2\leq(x-s)(h-x),\qquad h=\overline{e^\dagger Ae},
```

where $`s=\overline{e^\dagger(A-BC^{-1}B^T)e}`$. We have used the weaker fast endpoint $`h`$; the actual fast endpoint can be smaller.

Let $`S=A-BC^{-1}B^T`$. The inverse chord bound on the full $`K`$ implies

```math
S^{-1}\preceq\frac{(m+M)I-A}{D}.
```

Inverse order, scalar Cauchy–Schwarz, and convexity under time averaging yield

```math
s\geq\frac{D}{m+M-h}.
```

Maximizing $`(x-D/(m+M-h))(h-x)`$ over $`h`$ gives

```math
|z|^2-(m+M)x+2\sqrt D\,|y|+D\leq0.
```

No internal coordinates gives $`G=\overline A`$ and zero asymmetry directly. Damping cross-blocks do not spoil the clamped mean because their derivative contribution averages to zero. The positive symmetric part follows also from the full averaged elastic energy with a nonzero imposed displacement.

### One sector for both lenses

Normalize the force scalar by $`w=\sqrt D\,z`$ and the clamped scalar by $`w=z/\sqrt D`$. Both inequalities become

```math
|w|^2-2\xi\operatorname{Re}w+2|\operatorname{Im}w|+1\leq0,
\qquad \xi=\frac{k}{\sqrt D}.
```

For $`t=|\operatorname{Im}w|/\operatorname{Re}w`$, existence of a positive real part requires

```math
(\xi-t)^2\geq1+t^2.
```

Therefore $`t\leq(\xi^2-1)/(2\xi)=\mathfrak a_*`$. Holding for every complex $`e`$, this is precisely the matrix inequality $`\mathfrak a_*S_Q\pm iA_Q\succeq0`$, proving the claimed index bound.

These are ordinary numerical-range and sector arguments. The result should be treated as a sharpened interpretation of the existing mechanical theorem, not as a new general theory of matrix asymmetry.

## 3. A balanced allocation attains both index bounds

In the existing rotating-coupling family choose

```math
h=g=k,\qquad b=(M-m)/2,\qquad \gamma_y\Omega=\sqrt D.
```

All instantaneous stiffness eigenvalues remain $`(m,m,M,M)`$. The measured coordinates remain stationary under every constant force. Direct elimination gives

```math
\chi=\alpha I+\beta J,
```

```math
\alpha=\frac{2k}{k^2+D},\qquad
\beta=\frac{k^2-D}{\sqrt D(k^2+D)}.
```

Thus $`\beta/\alpha=\mathfrak a_*`$, $`\det\chi=1/D`$, and $`G=\chi^{-1}`$ attains the same index. The original two dimensional objectives are not changed.

For the worked spectrum $`(1,1,3,3)k_0`$ and the same modulation rate, compare:

| Allocation | $`k_0\beta`$ | $`\kappa/k_0`$ | Common index when $`G=\chi^{-1}`$ |
|---|---:|---:|---:|
| Cross-displacement optimum | 0.089316397 | 0.197418394 | 0.133974596 |
| Balanced | 0.082478610 | 0.247435830 | **0.144337567** |
| Work-per-loop-area optimum | 0.065806131 | 0.267949192 | 0.133974596 |

There is no claim that the balanced device is better for every application. It maximizes relative asymmetry rather than either absolute cross coefficient. It is not an efficiency optimization.

At this contrast the existing twelve-spring geometry remains strictly positive. With the existing smoothing choice $`\eta=0.1`$, all four fixed support coefficients equal $`0.3k_0`$ and the eight connecting coefficients range from $`0.1k_0`$ to $`2.1k_0`$. The guide, actuator, and damping idealizations are unchanged. The same layout is not claimed feasible for arbitrary contrast.

The force-only index bound can also be attained by the planar rotating example. This note does not prove a new minimum coordinate count for the index. The four-coordinate construction is useful because **one and the same device** attains both indices while its measured coordinates are stationary.

## 4. The absolute optima cannot both be reached by an inverse pair

For a two-port device whose stationary measured outputs ensure $`G=\chi^{-1}`$, write $`\chi=S+\beta J`$. Since $`\det\chi=\det S+\beta^2`$,

```math
\beta\kappa=\frac{\mathfrak a(\chi)^2}{1+\mathfrak a(\chi)^2}.
```

Consequently,

```math
\boxed{\beta\kappa\leq
\left(\frac{k^2-D}{k^2+D}\right)^2.}
```

The balanced allocation attains the product bound. At $`m=k_0,M=3k_0`$ it is $`1/49\simeq0.0204082`$. Multiplying the two separate absolute ceilings would instead give approximately $`0.0239323`$, which cannot be simultaneously attained by an inverse response pair.

This product statement must not be applied to arbitrary mean force and clamped measurements that are not inverses. The earlier rotating planar device remains a counterexample to identifying the experiments: it has a nonzero force-controlled antisymmetric response but a symmetric clamped reaction.

## 5. A reciprocal load can look perfectly directional

For any positive-definite symmetric part and a static symmetric positive-semidefinite addition $`L`$,

```math
\mathfrak a(Q+L)\leq\mathfrak a(Q).
```

Indeed, the skew part is unchanged and its quadratic form is normalized by a larger positive form. When a stationary-output device is loaded at the measured coordinates, $`G_L=G+L`$ and $`\chi_L=G_L^{-1}`$, so the normalized index cannot grow. This is a matrix property plus the exact static load law, not a general assertion for devices with port micromotion or altered internal loading.

Nevertheless, a directional **ratio** can become arbitrarily large. For the balanced $`[k_0,3k_0]`$ example,

```math
G=k_0\begin{pmatrix}12/7&\sqrt3/7\\-\sqrt3/7&12/7\end{pmatrix}.
```

Attach one reciprocal difference-spring load

```math
L=\frac{\sqrt3k_0}{7}\begin{pmatrix}1&-1\\-1&1\end{pmatrix}.
```

It is positive semidefinite. The loaded result is

```math
k_0\chi_L\simeq
\begin{pmatrix}0.509756343&0\\0.128593157&0.509756343\end{pmatrix}.
```

One exchanged cross-response vanishes, while the other remains nonzero. Yet the index falls from $`0.144337567`$ to $`0.127147451`$. This is cancellation between reciprocal and antisymmetric couplings, not an increase in normalized asymmetry. It is a zero-frequency directional response, not broadband isolation. Small load error destroys exact cancellation; no robustness of an infinite directional ratio is claimed.

The load also changes the complete instantaneous stiffness interval to approximately $`[1,3.277593337]k_0`$. It is not an admissible way to claim an improvement at the unchanged $`[1,3]k_0`$ budget. Direct integration of the laboratory-frame forced equations verifies the loaded matrix from rest.

## 6. A real predecessor exposes the physical boundary

Lin et al. [N2] derive an overdamped particle above a driven rotating disk. Their small-displacement equation (12), with an added constant test force, has effective reaction

```math
G_{\rm disk}=kI-\frac{f\xi}{\zeta_s}J.
```

Here $`f`$ is the applied driving torque, and $`\xi,\zeta_s`$ are their friction coefficients. Its asymmetry index is $`|f\xi|/(k\zeta_s)`$ even though the ordinary confining springs are isotropic. Thus a ceiling inferred from the springs alone with $`m=M=k`$ would fail for that published device.

This is **not** a counterexample to our theorem. The rotating disk creates a drive-dependent viscous positional force. Before elimination, its dissipation matrix depends on the mechanical coordinates and its extra driven coordinate is not uniformly confined by a positive quadratic stiffness. It is not a prescribed, uniformly positive stiffness modulation with constant damping and fixed equilibrium on all accounted coordinates.

This comparison closes an earlier abstract-only gap for that source: the explicit finite-dimensional model and Eq. (12) were read in the primary PDF. It also narrows the physical claim. We limit what **stiffness programming alone within this class** can produce, not everything assembled from reciprocal springs and an arbitrary drive.

Shi et al. [N3] likewise show that nonreciprocal dynamics can be embedded in a larger constrained Hamiltonian system. Their primary text notes that the Hamiltonian can vanish identically on the constraint and acts as a dynamics generator rather than the energy of the original system. Such an embedding is not automatically a stable bounded-stiffness realization with a fixed power-conjugate force probe. Absence of a microscopic potential in the reduced coordinates, or doubling the variables, is not a novelty claim available here.

## 7. Relation to established asymmetry bounds

Brandner and Seifert [N1, Eq. (15) and Appendix A] use this asymmetry index to constrain Onsager matrices and their Schur complements. Their bound follows from current conservation and substochastic scattering matrices; its resource is not a mechanical stiffness contrast. The related three-terminal PRL [N4] already demonstrates why a response asymmetry limit must use microscopic constraints beyond a positive symmetric part.

We inherit the index and its basic geometry. We have not established that the mechanical constant derived here is absent from every operator-bound theorem. This is a useful common interpretation and an exact consequence of the previous mechanical proofs, not a new independent centerpiece based on a familiar matrix functional. A shared mathematical language does not equate scattering, heat-engine efficiency, and externally driven elastic compliance.

The finite spring realization remains an ideal construction rather than a fabricated apparatus. No new experiment, inertial model, controller, or large search over devices is introduced. The original force and clamped dimensional ceilings and their benchmark values are preserved.

## Sources and access

[N1] K. Brandner and U. Seifert, *Multi-terminal thermoelectric transport in a magnetic field: bounds on Onsager coefficients and efficiency*, New Journal of Physics **15**, 105003 (2013), [arXiv:1308.2179v1](https://arxiv.org/abs/1308.2179). Primary PDF: Eq. (15), Section 3, and Appendix A inspected. The paper credits a related earlier measure to Crouzeix and Gutan; the latter's publisher record and abstract, but not its full proof, were checked: [Optimization 52, 251–262 (2003)](https://doi.org/10.1080/0233193031000120048).

[N2] L.-S. Lin, K. Yasuda, K. Ishimoto, Y. Hosaka, and S. Komura, *Onsager's variational principle for nonreciprocal systems with odd elasticity*, Journal of the Physical Society of Japan **92**, 033001 (2023), [arXiv:2209.15363](https://arxiv.org/abs/2209.15363). The primary PDF's Eqs. (1)–(12) were inspected, including the full frictional model before elimination. No figure data or graphical measurements were used.

[N3] Y.-B. Shi, R. Moessner, R. Alert, and M. Bukov, *Hamiltonian description of non-reciprocal interactions*, Nature Physics (12 June 2026), [publisher full text](https://www.nature.com/articles/s41567-026-03317-0). The constrained embedding and its energy interpretation were inspected. The existence of a Hamiltonian embedding is credited, not treated as an invention of this project.

[N4] K. Brandner, K. Saito, and U. Seifert, *Strong Bounds on Onsager Coefficients and Efficiency for Three-Terminal Thermoelectric Transport in a Magnetic Field*, Physical Review Letters **110**, 070603 (2013), [primary record](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.110.070603). The publication record and abstract were checked; no complete equation-by-equation subsumption assessment is claimed from that abstract.

Accessed 30 September 2026. Primary PDF text was available for N1 and N2; screenshot attempts failed. The exact matrix relations used here were independently derived, and no visual inspection or copied figure is claimed. Bibliographic dates follow the original arXiv headers and journal records rather than regenerated body dates. These limitations do not constitute an exhaustive priority determination.

## Reproduce

Run `python checks/scale_free.py --output scale-free.local.json`. Five diagnostic groups independently implement exact stepped force/clamped maps, full matrix sector tests, equality and inverse/product checks, a from-rest loaded trajectory, and the existing positive-spring synthesis at balanced allocation. None imports the prior scientific modules. Random examples supplement the analytic proof; they do not establish the arbitrary-dimension bound.
