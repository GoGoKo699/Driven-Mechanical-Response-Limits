# Scientific background for the focused theory paper

[Home](../README.md) · [Tutorial bridge](TUTORIAL.md) · [Selected review](TUTORIAL_OPTIONS.md) · [Source register](SOURCES.md)

This is a research and citation guide, not manuscript text. It consolidates the background needed for the current ideal-theory claim, separates established ingredients from the local result, and links those explanations to the [local tutorial](TUTORIAL.md). The canonical statements remain [Model](MODEL.md), [Results](RESULTS.md), [Proof](PROOF.md), and the linked companion derivations. Access and comparisons were checked on 30 September 2026.

## 1. Begin with the measurement, not with a general claim of nonreciprocity

In a static reciprocal linear network, the energy is $`U=q^TKq/2`$ with $`K=K^T\succ0`$. With normalized conjugate ports $`P`$ and a constant applied force $`PF`$,

```math
\chi_{\rm static}=P^TK^{-1}P=\chi_{\rm static}^T.
```

In coordinates split into measured and hidden parts, write the static stiffness as blocks $`A,B,B^T,C`$. Eliminating the hidden coordinates gives

```math
G_{\rm static}=A-BC^{-1}B^T=\chi_{\rm static}^{-1}.
```

These elementary identities express static linear reciprocity and explain why ordinary hidden-coordinate elimination alone cannot generate an odd static response. Coulais, Sounas, and Alù's nonlinear static metamaterial work provides a useful contrast: its leading linear terms are reciprocal, while finite-force asymmetry relies on geometric nonlinearity ([R14](SOURCES.md#r14--static-nonreciprocity-through-geometric-nonlinearity)). Neither that result nor wave isolation is the observable optimized here.

Our constant probe acts while stiffness modulation continues. The periodic state can have internal motion even when measured coordinates are stationary. Its mean force compliance $`\chi`$ and the mean stiffness $`G`$ measured with coordinates held fixed are different experiments. In general $`G\ne\chi^{-1}`$; the attaining family has the extra stationary-output property that makes equality and static-load composition exact. This distinction must be taught locally, rather than inferred from a generic effective-medium analogy.

## 2. Odd elasticity supplies the physical context and work language

The selected single review is [Fruchart–Scheibner–Vitelli](TUTORIAL_OPTIONS.md#1-fruchart-scheibner-and-vitelli--selected-physics-anchor). The original Scheibner paper and Chen's active architecture establish odd constitutive response and deformation-cycle work ([W1–W2](PORT_WORK.md#6-comparison-with-actual-odd-elastic-architectures)). These precedents prevent claims to invent odd elasticity, its area law, or an operating odd element.

For the two conjugate displacement ports, our convention is $`G=\mathrm{Sym}\,G-\kappa J`$, with $`J_{12}=-1`$. The existing work note derives delivered quasistatic work $`W_{\rm qs}=2\kappa\mathcal A`$ for signed loop area $`\mathcal A`$. The scientific addition is the sharp constraint on $`\kappa`$ within the declared whole-network stiffness budget and its admissible attainment. A nonsymmetric compliance alone does not establish this work law for a differently constrained experiment.

Driven mean odd response also precedes this project. Huang and collaborators' granular model, Lin and collaborators' driven dissipative-coordinate model, and Rahimi–Park's passive-component driven architecture are compared at the equation level in [SOURCES](SOURCES.md#focused-paper-level-comparison), [PORT_WORK](PORT_WORK.md#6-comparison-with-actual-odd-elastic-architectures), and [SCALE_FREE_RESPONSE](SCALE_FREE_RESPONSE.md). Their existence rules out broad first-mechanism claims. Their differing constitutive assumptions do not by themselves prove our narrower priority; the comparison concerns the complete constrained optimum and equality family.

## 3. The mathematical ingredients have direct predecessors

| Ingredient | Primary source and precise role | Local step still required |
|---|---|---|
| Positive-plus-skew resolvent and spectral response | Pavliotis (2010), §3; Duncan–Lelièvre–Pavliotis (2016), Lemma 3, Eq. (29), Theorem 4; [P1–P2](OPERATOR_CONNECTION.md#direct-primary-source-comparison) | Identify the periodic mechanical operator and its domain, forcing, and measured scalar |
| Exact optimized inverse-gap constants | Moslehian–Nakamoto–Seo (2011), Theorem 2.1(i), p. 180; [explicit substitutions](OPERATOR_CONNECTION.md#the-exact-inverse-gap-constants-are-established) | Enforce the same complete mechanical budget and realize equality with reciprocal stiffness |
| Effective operators, projection, and attainable bounds | Milton's book, §§12.7–12.10 and Chapter 13; Kern–Miller–Milton (2020), Eqs. (1)–(9); [R2](SOURCES.md#r2) | A time-domain problem needs its own reduction; a spatial composite formula is not a mechanical proof |
| Normalized matrix asymmetry | Brandner–Seifert (2013), Eq. (15) and Appendix A; [N1](SCALE_FREE_RESPONSE.md) | Optimize the established index over this stiffness class and distinguish it from load cancellation |

The short proof uses a phase-weighted inner product, periodic quadratic identities, Cauchy–Schwarz, and an inverse chord inequality. The operator comparison explains the broader provenance; it need not become a prerequisite for reading the main theorem. Disk geometry, the dimensional constants, and the asymmetry index must receive attribution instead of being presented as independent new discoveries.

The local result combines those tools with a four-coordinate reciprocal equality family, the clamped coordinate minimum, and port/resource interpretation. The separate force-response minimum retains its stationary-output and damping-block assumptions. Neither minimum says that four coordinates are needed for every nonzero odd response.

## 4. Work extraction and efficiency need an explicit energy account

For differentiable prescribed stiffness, the model directly gives

```math
\dot U=(PF)^T\dot q-\dot q^T\Gamma\dot q+\tfrac12q^T\dot Kq.
```

The last term is stiffness-control power supplied to the mechanical system; it follows by differentiating the energy, not by assigning a passive label to the springs. Piecewise control requires the corresponding energy jumps. This mechanical account does not model controller losses.

Fodor and Souslov's [odd-engine paper, W3](PORT_WORK.md#6-comparison-with-actual-odd-elastic-architectures), Eqs. (2)–(5), defines an efficiency using output work and even-loss-modulus dissipation, while excluding the microscopic mechanism sustaining energy input. Our construction resolves hidden-coordinate dissipation, including loss during holding. Consequently its slow-cycle efficiency limit cannot be equated to theirs. Keep pump frequency separate from slow displacement-cycle frequency, and avoid turning a bound on work per area into a claim about optimal power or efficiency. The detailed comparison and finite-rate calculation belong in [PORT_WORK](PORT_WORK.md).

## 5. Constitutive support is not complete-device validation

The eight full-text harmonic-control precedents in [R4–R8 and R10–R12](SOURCES.md#full-text-primitive-check) support prescribed harmonic confinement, multicoordinate quadratic models, local constant drag approximations, and stiffness-drive work. They are collective evidence for model ingredients. They do not certify the complete guided-slider arrangement or every assumption of its actuators.

For a compact introduction, Plata (bounded stiffness), Baldassarri (coupled driven quadratic dynamics), and Dago (hydrodynamic approximations behind fixed mobility) are useful representative references. Martinez and Trainiti matter when discussing implemented control capability; Kwon matters for the inertial and work-account comparison. Use the detailed source register when making those specific implementation claims rather than listing every precedent in an introductory paragraph.

The [physical-validity note](PHYSICAL_VALIDITY.md) separates the tangent spring construction from finite-amplitude mechanics and states the controlled small-mass assumptions. The [capacitive screen](CAPACITIVE_ACTUATION.md#primary-sources-and-access) retains electrical charge before elimination and derives reciprocal long-time response with fixed positive leakage. Its cited piezoelectric, dielectric-loss, and time-varying-capacitor laws support that particular calculation. They do not establish a universal obstruction for all actuation technologies. Finite tuning at reduced contrast does not remove the leakage result.

## 6. Citation and teaching decisions before writing

| Purpose | Use |
|---|---|
| One external learning anchor | The selected [Fruchart–Scheibner–Vitelli review](TUTORIAL_OPTIONS.md), followed by the [local tutorial bridge](TUTORIAL.md) |
| Introduce reciprocity and odd elastic work | The review, Scheibner, and the exact constitutive comparisons above; Coulais if contrasting nonlinear static response |
| Attribute the proof ingredients | Moslehian–Nakamoto–Seo, Pavliotis, and Duncan–Lelièvre–Pavliotis at the relevant mathematical steps |
| Position the proposed contribution | Closest driven/hidden-variable mechanisms and the full resource-matched equality comparison |
| Discuss normalized asymmetry or efficiency | Brandner–Seifert or Fodor–Souslov, respectively; preserve definitions |
| Discuss implementation limits | The specific primitive sources and actuator laws actually used, with their approximation boundaries |

The [curated bibliography](../references.bib) provides reusable records for these central comparisons and tutorial candidates. It is not an instruction to cite every entry: the full linked source registers include additional supporting and contextual records. Strang's complete text was not inspected; peripheral abstract-only access limitations remain explicitly labeled in their original notes. The central Scheibner and Fodor–Souslov access gaps have been closed with full primary texts.
