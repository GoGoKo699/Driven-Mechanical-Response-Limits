#!/usr/bin/env python3
"""Run the consolidated mechanics diagnostics without changing reference data."""
from __future__ import annotations
import argparse
import json
import platform
from pathlib import Path
import numpy as np
import scipy
import network
import springs
import operator_bridge

ROOT = Path(__file__).resolve().parents[1]


def benchmark() -> dict:
    p = network.hidden_parameters(1.0, 3.0)
    chi, _ = network.exact_hidden(p, np.sqrt(3.0))
    loaded, _ = network.exact_hidden(p, np.sqrt(3.0), load=np.eye(2))
    values = [e[3] for t in np.linspace(0, springs.PERIOD, 65) for e in springs.elements(float(t))]
    return {
        "stiffness_interval": [1.0, 3.0],
        "ceiling": 0.5 * (1 - 1 / np.sqrt(3.0))**2,
        "planar_ceiling_same_interval": 1 / 12,
        "optimal_omega_internal_drag_one": np.sqrt(3.0),
        "compliance": chi.tolist(),
        "unit_spring_loaded_compliance": loaded.tolist(),
        "support_springs": springs.GROUNDS.tolist(),
        "modulated_spring_range": [min(values), max(values)],
        "one_percent_lower_beta": springs.BETA_STAR - 0.03 / 0.99,
    }


def compare_reference(actual: dict, path: Path) -> None:
    expected = json.loads(path.read_text())
    if actual.keys() != expected.keys():
        raise AssertionError("Reference fields do not match")
    for name in expected:
        np.testing.assert_allclose(actual[name], expected[name], rtol=2e-10, atol=2e-12, err_msg=name)


def main() -> None:
    if not __debug__:
        raise RuntimeError("Run without -O: scientific diagnostic assertions must be enabled")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "results.local.json")
    args = parser.parse_args()
    if args.output.resolve() == (ROOT / "checks/reference.json").resolve():
        parser.error("The reference file cannot be overwritten by this runner")
    groups = [
        ("network_disk", network.test_arbitrary_dimensions),
        ("attainment", network.test_sharpness),
        ("loaded_clamped_dynamics", network.test_time_domain),
        ("generalized_springs", network.test_spring_synthesis),
        ("resource_matched_comparison", network.test_fair_budget),
        ("fixed_support_axial_synthesis", springs.synthesis_checks),
        ("finite_length_geometry", springs.geometry_checks),
        ("parallel_graph_control", springs.positivity_control),
        ("coordinate_minimum_controls", springs.sharpness_and_three_coordinate_control),
        ("calibration_error", springs.tolerance_checks),
        ("operator_bridge", operator_bridge.run_checks),
    ]
    result = {}
    for name, check in groups:
        result[name] = check()
        print(f"PASS {name}", flush=True)
    values = benchmark()
    compare_reference(values, ROOT / "checks/reference.json")
    report = {
        "status": "PASS", "diagnostic_groups": len(groups),
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "benchmark": values, "checks": result,
        "scope": "Finite algebra and dynamics checks; the written proof supports universal statements.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print("PASS fixed benchmark reference")


if __name__ == "__main__":
    main()
