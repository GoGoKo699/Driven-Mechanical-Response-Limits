# Capacitive implementation screen

Date: 30 September 2026. Baseline main: `abbf633`.

The user authorized continued research and repository merges. This increment assesses one concrete constitutive route: positive capacitive tuning of reciprocal piezoelectric elements. It introduces no manuscript and changes none of the original mechanical theorem's assumptions or benchmark values.

The ideal isolated zero-charge reduction has the desired tunable stiffness law. The complete model with constant leakage instead has a unique attracting static state, zero electrode voltage, and reciprocal response. Charge balance and a coercive full-state energy prove the result. The finite-tuning note separately derives the contrast interval compatible with a specified spring ratio and a positive support reserve; it does not repair the leakage obstruction.

Primary evidence supplies established constitutive and component models. Access levels and the limitation of a fixed leakage model are explicit in the [actuator note](../docs/CAPACITIVE_ACTUATION.md#primary-sources-and-access). Separate assistant derivations reviewed the mathematics and source interpretation; this is internal review, not external peer review or an experiment.

The new diagnostic uses one isolated-charge trajectory and two one-period leaky evolution maps, with no search over devices or long transient sweep. Its capacitances and material parameters are synthetic dimensionless examples. The measured mechanical asymmetry is about $`1.60\times10^{-4}`$ in the isolated case and numerically zero in both leaky cases, consistent with the analytic proof. No physical measurement precision is inferred from solver residuals.

Local validation: the eleven-group main suite and preserved reference benchmark passed, as did all four groups of `capacitive_shunt.py`, including the static-state check. The new script's assertions-disabled and reference-overwrite guards were tested. Documentation navigation, mathematical source syntax, preserved hashes/license, and whitespace checks passed. Hosted workflow results are separate from this local record.
