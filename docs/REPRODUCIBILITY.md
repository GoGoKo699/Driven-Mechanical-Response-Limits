# Reproducibility and claim map

[Home](../README.md) · [Statements](RESULTS.md) · [Proof](PROOF.md)

## Commands

The tested environment is Python 3.13.5, NumPy 2.3.5, and SciPy 1.17.0. The pinned dependencies require Python 3.11 or later; other interpreter/library combinations have not been tested here.

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python checks/run.py --output results.local.json
python checks/check_docs.py
```

On Windows, activate the virtual environment with its platform-specific activation command. All calculations are local and CPU-only. No cloud simulation or network access is needed after dependency installation.

The runner calls eleven named diagnostic groups, then compares independently recomputed benchmark values with [reference.json](../checks/reference.json). It does not refresh that reference file. Assertions must be enabled: running with Python's `-O` flag is rejected. Numerical-library roundoff can change the last digits; comparisons use explicit tolerances rather than byte equality across environments.

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

The original scientific implementations are [network.py](../checks/network.py) and [springs.py](../checks/springs.py), preserved byte-for-byte from the supplied network and realization checkpoints. They are separate computational derivations: the nonlinear forces do not call the target stiffness matrix to manufacture the desired response. [run.py](../checks/run.py) provides the consolidated interface. The self-contained [operator-comparison module](../checks/operator_comparison.py) tests the additional fixed-schedule identities without importing either of those two modules. The module-level historical docstrings are not the canonical scope statement; use the documents above.

## What passing means

The checks test algebraic identities, signs, matrix spectra, finite numerical trajectories, and the consistency of the geometric linearization. They do not establish arbitrary-dimensional optimality by sampling, a minimum spring count, nonlinear global stability, experimental accuracy, an exhaustive literature search, or independent scientific validation. The written proofs support universal claims.

The finite-length outputs can slightly exceed the tangent ceiling because their actual tangent stiffness changes with displacement. Their convergence toward the linear example, not their finite-amplitude comparison with an unchanged spectral bound, is what is tested.

## Documentation validation

[check_docs.py](../checks/check_docs.py) verifies relative destinations, Markdown section anchors, math-fence balance, supported short display syntax, and preserved script/license hashes. It also checks that the benchmark quoted in the README and results remains tied to the stored reference.

This is a source and consistency check, not a guarantee of GitHub's live mathematical rendering. Displays are intentionally short; no equation tags or TeX document wrappers are used. Automated workflow results must be read separately from local execution records.

## Provenance

[INPUTS.json](../provenance/INPUTS.json) identifies the supplied checkpoints by SHA-256 and records which scripts are retained exactly. The original archives remain separate historical inputs rather than nested dependencies of the main reading path. They are not claimed to be fully republished in this repository.

The [build record](../provenance/BUILD.md) records what was actually rerun during consolidation. Its function is provenance, not certification of novelty or publication status.

The [operator-comparison record](../provenance/OPERATOR_COMPARISON.md) documents the subsequent fixed-schedule refinement and its source/test boundaries.
