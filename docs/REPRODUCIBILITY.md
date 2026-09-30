# Reproducibility and claim map

[Home](../README.md) · [Statements](RESULTS.md) · [Proof](PROOF.md)

## Commands

The original recorded environment is Python 3.13.5, NumPy 2.3.5, and SciPy 1.17.0. The physical-validity update also passed with Python 3.12.14 and the same numerical-library versions. The pinned dependencies require Python 3.11 or later.

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python checks/run.py --output results.local.json
python checks/port_work.py --output port-work.local.json
python checks/scale_free.py --output scale-free.local.json
python checks/finite_mass.py --output finite-mass.local.json
python checks/capacitive_shunt.py --output capacitive-shunt.local.json
python checks/check_docs.py
```

On Windows, activate the virtual environment with its platform-specific activation command. All calculations are local and CPU-only. No cloud simulation or network access is needed after dependency installation.

The runner calls eleven named diagnostic groups, then compares independently recomputed benchmark values with [reference.json](../checks/reference.json). It does not refresh that reference file. Assertions must be enabled: running with Python's `-O` flag is rejected. Numerical-library roundoff can change the last digits; comparisons use explicit tolerances rather than byte equality across environments.

The runner, standalone operator comparison, and four companion diagnostics reject an output path resolving to the stored reference file before running their checks. Their assertions-disabled guards also reject `-OO`.

The documentation release checks additionally use Node.js 22 or later:

```sh
python -m unittest discover -s checks -p 'test_check_docs.py'
npm ci --prefix checks --ignore-scripts
npm --prefix checks run check
```

These dependencies are only for documentation validation. The scientific calculations remain Python-only.

## Claim map

| Scientific claim | Analytic location | Executed diagnostic |
|---|---|---|
| General network disk | [Weighted projection](PROOF.md#weighted-projection) | `network_disk`: arbitrary 2-, 3-, 4-, 6-coordinate stepped networks; nonisotropic constant drag; periodic energy balances |
| Sharp ceiling and envelope | [Removing the waveform](PROOF.md#removing-the-waveform), [attainment](PROOF.md#attainment) | `attainment`: spectra, disk and envelope boundary formulas |
| Fair stiffness-budget comparison | [Fixed measured stiffness](RESULTS.md#fixed-measured-stiffness) | `resource_matched_comparison`: padded planar reference with matched spectrum |
| Stationary outputs and static loads | [Port law](REALIZATION.md#stationary-outputs-and-static-loads) | `loaded_clamped_dynamics`: from-rest trajectories, isotropic/anisotropic spring loads, port damping, and clamp reactions |
| Positive generalized spring decomposition | [Construction](REALIZATION.md#twelve-strictly-positive-spring-coefficients) | `generalized_springs` checks the earlier smooth decomposition; `fixed_support_axial_synthesis` checks the canonical fixed-support version |
| Exact axial geometry has the intended tangent | [Fixed geometry](REALIZATION.md#fixed-geometry-and-exact-spring-lengths) | `fixed_support_axial_synthesis`: finite-difference force Jacobian; `finite_length_geometry`: nonlinear central forces and power balance |
| Parallel difference-spring graph limitation | [Positivity argument](PROOF.md#parallel-guide-obstruction) | `parallel_graph_control`: unequal but nonnegative exchanged responses |
| Conditional four-coordinate minimum | [Rank proof](PROOF.md#coordinate-minimum) | `coordinate_minimum_controls`: equality identities and a suboptimal three-coordinate example; not an enumeration over all three-coordinate devices |
| Coefficient-error guarantee | [Energy estimate](PROOF.md#coefficient-errors) | `calibration_error`: specified unequal spring offsets versus the conservative bound |
| Fixed-schedule endpoint disk and operator relationship | [Operator connection](OPERATOR_CONNECTION.md) | `operator_connection`: four subgroups for resolvent reconstruction, phase-speed sweeps, equality, and excluded controls |
| Clamped ceiling and work account | [Clamped proof and cycles](PORT_WORK.md) | `port_work.py`: exact clamped maps, allocation, laboratory work ledger, finite-rate cycles, reversal controls |
| Four-coordinate clamped minimum | [Pointwise rank and trace proof](PORT_WORK.md#four-coordinates-are-necessary-for-clamped-attainment) | Existing one-hidden-coordinate stepped cases check the half-ceiling; the four-coordinate equality check supplies sufficiency. The necessity statement is analytic, not a numerical enumeration. |
| Full matrix asymmetry and inverse-pair product | [Numerical-range and sector proofs](SCALE_FREE_RESPONSE.md) | `scale_free.py`: five groups for general matrices, equality, loads, scope, and spring synthesis |
| Small-mass persistence of the same construction | [Stability and exact error](PHYSICAL_VALIDITY.md#a-controlled-small-mass-limit) | `finite_mass.py`: four laboratory integrations, two unit forces each, off-orbit Lyapunov identity, equal-spectrum control |
| Connecting-spring tuning requirement | [Exact extrema](PHYSICAL_VALIDITY.md#the-existing-spring-schedule-requires-a-large-tuning-range) | Algebraic extrema of the existing synthesis; no new simulation |
| Finite tuning at smaller contrast | [Exact feasible interval](TUNING_RANGE.md#exact-feasible-interval-for-the-existing-decomposition) | `capacitive_shunt.py`: support reserve, positive synthesis, finite capacitances at an illustrative 1.10 spring ratio |
| Capacitive implementation obstruction | [Charge balance and stability](CAPACITIVE_ACTUATION.md#three-line-proof-of-reciprocal-mean-response) | `capacitive_shunt.py`: isolated-charge ODE and two leaky one-period evolution maps; the universal conclusion is analytic |

The original scientific implementations are [network.py](../checks/network.py) and [springs.py](../checks/springs.py), preserved byte-for-byte from the supplied network and realization checkpoints. They are separate computational derivations: the nonlinear forces do not call the target stiffness matrix to manufacture the desired response. [run.py](../checks/run.py) provides the consolidated interface. The self-contained [operator-comparison module](../checks/operator_comparison.py) tests the additional fixed-schedule identities without importing either of those two modules. The module-level historical docstrings are not the canonical scope statement; use the documents above.

## What passing means

The checks test algebraic identities, signs, matrix spectra, finite numerical trajectories, and the consistency of the geometric linearization. They do not establish arbitrary-dimensional optimality by sampling, a minimum spring count, nonlinear global stability, experimental accuracy, an exhaustive literature search, or independent scientific validation. The written proofs support universal claims.

The finite-length outputs can slightly exceed the tangent ceiling because their actual tangent stiffness changes with displacement. Their convergence toward the linear example, not their finite-amplitude comparison with an unchanged spectral bound, is what is tested.

## Documentation validation

[check_docs.py](../checks/check_docs.py) verifies relative destinations, Markdown section anchors, and preserved script/license hashes. Its math-source checks cover GitHub `math` fences, dollar-delimited displays, protected and legacy inline formulas, balanced delimiters and braces, nonempty formulas, escaped table pipes, and short display lines. Ordinary fenced and inline code is excluded from math checks; unsupported TeX math delimiters, equation tags, and document wrappers are rejected. The script also checks the stored reference ceiling against its recorded value. Agreement of numerical values quoted in the prose is reviewed separately; this script does not parse and verify every such quotation.

The checker also rejects `\operatorname` and raw less-than signs in math, following the observed unsupported-command and truncated-formula failures. Use `\mathrm{...}` for operation names and `\lt` for strict inequalities. The [regression tests](../checks/test_check_docs.py) retain those failures and malformed delimiter, fence, brace, and table cases, alongside valid code exclusions.

[check_math.cjs](../checks/check_math.cjs) independently sends each complete Markdown document through a GFM parser and compares every formula's exact source and order with the source extractor. It then renders all mathematics with pinned MathJax base and AMS packages, with error suppression disabled. Unknown commands, malformed environments, empty renders, dropped or duplicated formulas, and inconsistent table widths fail the gate. Raw HTML requires an explicit format-policy decision rather than silently bypassing the Markdown path. Installed dependency documents are excluded.

Both checks run in CI. They validate the repository source and a complete local rendering path; they cannot guarantee every future browser or GitHub renderer version. Live GitHub inspection is recorded separately in the [build record](../provenance/BUILD.md). Displays are intentionally short, with no equation tags or TeX document wrappers.

## Provenance

[INPUTS.json](../provenance/INPUTS.json) identifies the supplied checkpoints by SHA-256 and records which scripts are retained exactly. The original archives remain separate historical inputs rather than nested dependencies of the main reading path. They are not claimed to be fully republished in this repository.

The [build record](../provenance/BUILD.md) records what was actually rerun during consolidation. Its function is provenance, not certification of novelty or publication status.

The [operator-comparison record](../provenance/OPERATOR_COMPARISON.md) documents the subsequent fixed-schedule refinement and its source/test boundaries.

The [physical-validity record](../provenance/PHYSICAL_VALIDITY.md) records the attribution correction, rank corollary, small-mass check, and concrete implementation boundary.

The [capacitive-screen record](../provenance/CAPACITIVE_SCREEN.md) records the resolved actuator candidate and the retained ideal-theory scope.

The [theory-scope record](../provenance/THEORY_SCOPE.md) records the bounded literature and significance assessment and the decision to proceed to manuscript preparation. Numerical checks do not establish that editorial judgment.
