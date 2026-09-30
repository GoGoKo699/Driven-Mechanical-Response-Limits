# Capacitive piezoelectric actuation and the steady-response obstruction

[Home](../README.md) · [Physical validity](PHYSICAL_VALIDITY.md) · [Tuning range](TUNING_RANGE.md) · [Research status](RESEARCH_STATUS.md)

**A positive capacitive shunt can reproduce the intended spring law in an isolated, charge-conserving idealization. With fixed leakage paths, the same model has exactly reciprocal long-time mean compliance, however small the leakage.** This closes one concrete implementation route for the strict steady-force measurement. It does not invalidate the prescribed-mechanical-stiffness theorem.

The result below is a local deduction from standard linear piezoelectric constitutive equations and charge balance. No priority claim is made for this circuit observation.

## The established element and its ideal stiffness

Write the small-signal constitutive equations of a piezoelectric elastic element as

$$
f=k_Ee-\theta V,\qquad Q_p=\theta e+C_pV.
$$

Here $e$ is elongation, $f$ the applied mechanical force, $V$ the electrode voltage, $k_E>0$ the short-circuit stiffness, $C_p>0$ the clamped capacitance, and $\theta$ a constant reciprocal coupling. The equations are standard shunted-piezoelectric ingredients [A1, A3]. They contain no voltage-independent bias force.

Connect a positive external capacitance $C_s(t)$ directly across the electrodes. Its modulation is prescribed and externally powered. With no leakage, the total electrode charge

$$
z=\theta e+[C_p+C_s(t)]V
$$

is conserved. In the prepared sector $z=0$,

$$
f=\kappa(t)e,\qquad
\kappa(t)=k_E+\frac{\theta^2}{C_p+C_s(t)}.
$$

Define $k_D=k_E+\theta^2/C_p$. Every target interval strictly inside $(k_E,k_D)$ maps to finite positive capacitances via

$$
C_s(t)=\frac{\theta^2}{\kappa(t)-k_E}-C_p.
$$

This uses neither zero nor infinite capacitance. The external capacitance waveform is generally not band limited, even when the desired stiffness contains only the first two pump harmonics. A nonzero conserved $z$ introduces an extra force, so the preparation condition is part of the idealization.

Positive capacitive stiffness tuning has an experimental precedent [A2]. That supports the component principle. It does not certify continuous multi-element modulation or the charge condition needed for our steady-force experiment.

## Keeping the leakage state

For a network let $q$ collect all retained mechanical coordinates, let the columns of $U$ define the connecting elongations $e=U^Tq$, and let $\Theta=\operatorname{diag}(\theta_j)$. Put

$$
H=U\Theta,\qquad
\mathcal C(t)=\operatorname{diag}(C_{p,j}+C_{s,j}(t)),
$$

$$
K_E=K_{\rm support}+U\operatorname{diag}(k_{E,j})U^T\succ0.
$$

Take positive continuously differentiable periodic capacitances, constant mechanical damping $\Gamma\succ0$, and a constant symmetric positive-definite conductance matrix $G_{\rm leak}$. Independent positive leakage conductances on each electrode pair are the simplest case. The complete equations are

$$
\Gamma\dot q+K_Eq-HV=PF,
$$

$$
z=H^Tq+\mathcal C(t)V,\qquad
\dot z=-G_{\rm leak}V.
$$

In voltage variables, the second equation contains the term $\dot{\mathcal C}V$:

$$
\mathcal C\dot V+\dot{\mathcal C}V+H^T\dot q
=-G_{\rm leak}V.
$$

Omitting that term or imposing $z=0$ in the leaky system changes the physical model. The capacitor product derivative and its control-work port are standard [A5]. A parallel leakage resistance is an established constitutive correction [A4]; its numerical value or frequency dependence is apparatus dependent. The theorem here assumes fixed nonzero DC conductance, not every possible model of dielectric loss.

## Three-line proof of reciprocal mean response

For a periodic attracting response, charge balance gives

$$
0=\overline{\dot z}=-G_{\rm leak}\overline V,
\qquad \overline V=0.
$$

Averaging the mechanical equation then gives

$$
K_E\overline q=PF.
$$

Therefore

$$
\boxed{\chi_{\rm leak}=P^TK_E^{-1}P
=\chi_{\rm leak}^T.}
$$

The conclusion holds for every positive leakage scale, pump speed, positive capacitance waveform, and number of these elements. In fact, this model has the exact static solution

$$
q_*=K_E^{-1}PF,\qquad z_*=H^Tq_*,\qquad V_*=0.
$$

The stability proof below makes it the unique attracting periodic solution. Thus pump-induced motion and electrical dissipation disappear after transients under a constant force: changing capacitance cannot act on a zero-voltage state. The averaging proof exposes the DC obstruction directly, without solving any transient.

Clamping two measured coordinates gives the same conclusion for mean reaction: after eliminating the mean hidden displacements, the reaction is the symmetric Schur complement of $K_E$. Its odd coefficient and slow-loop oriented-area coefficient vanish. This does not exclude other finite-frequency or transient effects.

### Why the periodic response exists

The full stored energy in the mechanical and charge variables is

$$
\mathcal E(q,z,t)=\tfrac12q^TK_Eq
+\tfrac12(z-H^Tq)^T\mathcal C(t)^{-1}(z-H^Tq).
$$

It is uniformly positive definite in any fixed normalization of these variables. The full equation is

$$
\begin{pmatrix}\Gamma&0\\0&G_{\rm leak}^{-1}\end{pmatrix}
\begin{pmatrix}\dot q\\\dot z\end{pmatrix}
+\nabla\mathcal E=\begin{pmatrix}PF\\0\end{pmatrix}.
$$

For the difference $u$ of two solutions, the derivative of its constant damping-weighted quadratic norm is $-2u^T\mathcal K(t)u$, where $\mathcal K$ is the energy Hessian. Uniform positivity proves contraction, a unique periodic response, and attraction from arbitrary initial conditions. No stability assumption is supplied by numerical sampling.

This full electromechanical Hessian is not the reduced four-coordinate stiffness with budget $[m,M]$. Electrical states and their conjugate variables are explicitly retained; their elimination cannot be used to claim the unchanged full-network mechanical resource interval.

## Energy accounting and order of limits

The exact power identity is

$$
\dot{\mathcal E}=F^TP^T\dot q
-\dot q^T\Gamma\dot q-V^TG_{\rm leak}V
-\tfrac12V^T\dot{\mathcal C}V.
$$

The last term is work delivered by capacitance modulation. The resistor loss is nonnegative. A positive capacitor under prescribed modulation does not make the complete driven system passive, and the power required by its controller is additional to this ledger.

Let $G_{\rm leak}=gG_0$ with $G_0\succ0$. Taking the attracting long-time response first gives the reciprocal matrix above for every $g>0$, and therefore also as $g\to0^+$. Taking $g\to0$ first on a fixed observation interval, with $z(0)=0$, gives the isolated-charge model. That model can attain the nonzero mechanical ceiling under the prescribed schedule. The two limits do not commute.

A separation between mechanical and leakage time scales can motivate a finite observation window, but it does not recover the stipulated infinite-time mean response. Slowing the pump to suppress other actuator errors is not a cure for this obstruction. No finite-window performance guarantee is claimed here.

The same average-current reasoning covers additional fixed series resistors when the constant nodal conductance matrix is nonsingular after grounding: all mean node voltages then vanish. It does not cover modulated conductances, injected electrical currents, voltage-biased or active circuits, variable electromechanical coupling, changing $k_E$, or electrically isolated charge modes. Those are different constitutive models, not automatic exceptions within the proof.

## Consequence for this project

The [finite-tuning construction](TUNING_RANGE.md) shows that 21:1 stiffness tuning is not necessary for some nonzero ideal attainment. It cannot overcome the leakage obstruction. Thus the continuously modulated positive-capacitance model with fixed leakage is **not a robust long-time DC realization** of our attaining element.

The mechanical theorem and positive-spring tangent construction remain conditional theoretical results. This particular implementation candidate is closed with a negative result. An implementation based on genuinely modulating mechanical stiffness, or a materially different electrical model, would need its own derivation; we do not launch another actuator search to conceal this conclusion.

## Primary sources and access

[A1] N. W. Hagood and A. von Flotow, *Damping of structural vibrations with piezoelectric materials and passive electrical networks*, Journal of Sound and Vibration **146**, 243–268 (1991), [primary record](https://doi.org/10.1016/0022-460X(91)90762-9). The inspected publisher abstract establishes frequency-dependent shunt stiffness and damping. Full equations are taken from A3 and independently derived above, not claimed read in A1.

[A2] C. L. Davis and G. A. Lesieutre, *An actively tuned solid-state vibration absorber using capacitive shunting of piezoelectric stiffness*, Journal of Sound and Vibration **232**, 601–617 (2000), [primary record](https://doi.org/10.1006/jsvi.1999.2755), [author-institution record](https://pure.psu.edu/en/publications/actively-tuned-solid-state-vibration-absorber-using-capacitive-sh/). The accessible primary abstract reports a relay-controlled ten-step positive capacitor ladder. Its adaptive finite-frequency tuning experiment does not establish the present continuous DC schedule.

[A3] X. Liu, Y. Fan, L. Li, and X. Yu, *Improving Aeroelastic Stability of Bladed Disks with Topologically Optimized Piezoelectric Materials and Intentionally Mistuned Shunt Capacitance*, Materials **15**, 1309 (2022), [publisher paper](https://doi.org/10.3390/ma15041309), [full primary PDF](https://www.mdpi.com/1996-1944/15/4/1309/pdf). The full PDF's coupled mechanical/charge equations and capacitive-shunt elimination, Eqs. (5)–(8), were inspected. They supply the ordinary reciprocal constitutive ingredients, not the leakage theorem or our mechanical architecture.

[A4] J. Liang, H. S.-H. Chung, and W.-H. Liao, *Dielectric loss against piezoelectric power harvesting*, Smart Materials and Structures **23**, 092001 (2014), [primary article](https://doi.org/10.1088/0964-1726/23/9/092001), [author-hosted full PDF](https://metal.shanghaitech.edu.cn/publication/J11.pdf). Section 2 adds a parallel leakage resistance; Section 3 tests the model experimentally. This supports retaining leakage in the constitutive model, not attributing our zero-frequency result to their harvesting calculation.

[A5] D. Jeltsema, *Time-Varying Capacitors as Lossless Two-Port Devices*, [arXiv:2210.14057v1](https://arxiv.org/abs/2210.14057v1) (2022), [full primary PDF](https://arxiv.org/pdf/2210.14057). Equation (3) retains the complete charge derivative; Eqs. (21)–(24) account for the capacitance-control work port. These are inherited circuit ingredients, not a construction of the present device.

Accessed 30 September 2026. A3–A5 were read in full primary text; A1 and A2 are explicitly abstract-level comparisons. No third-party PDFs are redistributed and no device observations were made in this project.

## Reproduce

Run `python checks/capacitive_shunt.py --output capacitive-shunt.local.json`. It checks the actual eight-spring synthesis, finite positive capacitances, the isolated-charge response, and two leaky periodic states obtained from their one-period evolution maps. These small diagnostics check signs and the retained-charge equations; the averaging proof establishes the dimension-independent obstruction.
