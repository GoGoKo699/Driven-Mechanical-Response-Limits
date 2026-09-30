#!/usr/bin/env python3
"""Diagnostics for the reciprocal-endpoint bound and its operator interpretation.

The written argument is in docs/OPERATOR_BRIDGE.md. Finite Fourier matrices are
used only as consistency checks. They are not a proof of arbitrary waveforms.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import block_diag, expm


def assert_close(a, b, name: str, tol: float = 3e-10) -> float:
    err = float(np.max(np.abs(np.asarray(a) - np.asarray(b))))
    if not np.isfinite(err) or err > tol:
        raise AssertionError(f"{name}: {err} > {tol}")
    return err


def sym(a):
    return (a + a.T) / 2


def endpoints(Ks, weights, ports):
    weights = np.asarray(weights, float)
    if np.min(weights) <= 0 or not np.isclose(weights.sum(), 1):
        raise ValueError("Positive normalized phase weights required")
    mean = sum(w*K for w, K in zip(weights, Ks))
    slow = sum(w*(ports.T @ np.linalg.solve(K, ports)) for w, K in zip(weights, Ks))
    fast = ports.T @ np.linalg.solve(mean, ports)
    h = np.trace(ports.T @ mean @ ports)/2
    return fast, slow, float(h)


def stepped_response(Ks, weights, Gamma, ports, speed):
    """Exact affine maps and integrals, not the Fourier resolver below."""
    if speed == 0:
        return endpoints(Ks, weights, ports)[1]
    if speed < 0:
        return stepped_response(list(reversed(Ks)), list(reversed(weights)), Gamma, ports, -speed)
    n = len(Gamma)
    identity = np.eye(n)
    affine = np.zeros_like(ports)
    phi = identity.copy()
    segments = []
    for K, w in zip(Ks, weights):
        dt = 2*np.pi*w/speed
        rate = np.linalg.solve(Gamma, K)
        evolution = expm(-dt*rate)
        equilibrium = np.linalg.solve(K, ports)
        affine = evolution @ affine + (identity-evolution) @ equilibrium
        phi = evolution @ phi
        segments.append((dt, rate, evolution, equilibrium))
    first = np.linalg.solve(identity-phi, affine)
    cur = first.copy()
    integral = np.zeros_like(ports)
    for dt, rate, evolution, equilibrium in segments:
        integral += dt*equilibrium + np.linalg.solve(rate, (identity-evolution) @ (cur-equilibrium))
        cur = evolution @ cur + (identity-evolution) @ equilibrium
    assert_close(cur, first, "Periodic closure")
    return ports.T @ integral / (2*np.pi/speed)


def four_coordinate(phase):
    h = np.sqrt(3.)
    g = 4-h
    b = np.sqrt((3-h)*(h-1))
    R = np.array([[np.cos(phase), -np.sin(phase)], [np.sin(phase), np.cos(phase)]])
    return np.block([[h*np.eye(2), b*R], [b*R.T, g*np.eye(2)]])


def four_response(speed):
    h = np.sqrt(3.)
    c = (4-h-1j*speed)/(3-1j*h*speed)
    return np.array([[c.real, -c.imag], [c.imag, c.real]])


def collocation(Ks, Gamma, ports):
    """Real skew Fourier derivative on an odd grid; preserve its constant kernel."""
    nphase = len(Ks)
    n = len(Gamma)
    if nphase % 2 != 1:
        raise ValueError("An odd grid avoids an artificial Nyquist zero mode")
    k = np.fft.fftfreq(nphase, 1/nphase)
    derivative = np.fft.ifft(1j*k[:, None]*np.fft.fft(np.eye(nphase), axis=0), axis=0).real
    assert_close(derivative.T, -derivative, "Skew Fourier derivative")
    matrix = block_diag(*Ks)
    drift = np.kron(derivative, Gamma)
    embeds = np.tile(ports, (nphase, 1))/np.sqrt(nphase)
    Bpieces = []
    for K in Ks:
        vals, vecs = np.linalg.eigh(K)
        if vals.min() <= 0:
            raise ValueError("Stiffness must be positive")
        Bpieces.append((vecs/np.sqrt(vals)) @ vecs.T)
    B = block_diag(*Bpieces)
    hermitian = 1j * B @ drift @ B
    assert_close(hermitian, hermitian.conj().T, "Whitened derivative")
    values, vectors = np.linalg.eigh(hermitian)
    f = (embeds[:, 0]+1j*embeds[:, 1])/np.sqrt(2)
    weights = abs(vectors.conj().T @ B @ f)**2
    return matrix, drift, embeds, B, values, weights


def test_endpoints():
    rng = np.random.default_rng(20260930)
    speeds = [.02, .1, .5, 2., 10., 80.]
    rows = []
    for n in [2, 3, 4, 6]:
        for _ in range(3):
            ports, _ = np.linalg.qr(rng.normal(size=(n, 2)))
            z = rng.normal(size=(n, n))
            Gamma = .5*np.eye(n)+z.T@z/n
            Ks = []
            for _ in range(3):
                Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
                values = rng.uniform(1., 3., n)
                values[0], values[-1] = 1., 3.
                Ks.append((Q*values)@Q.T)
            weights = rng.uniform(.1, 1, 3)
            weights /= weights.sum()
            fast, slow, h = endpoints(Ks, weights, ports)
            a_fast, a_slow = np.trace(fast)/2, np.trace(slow)/2
            assert a_fast >= 1/h-1e-12
            previous = slow
            smallest_disk = smallest_matrix = 1.
            for speed in speeds:
                chi = stepped_response(Ks, weights, Gamma, ports, speed)
                alpha, beta = np.trace(chi)/2, (chi[1, 0]-chi[0, 1])/2
                margin = (alpha-a_fast)*(a_slow-alpha)-beta**2
                ordering = min(np.linalg.eigvalsh(previous-sym(chi)).min(), np.linalg.eigvalsh(sym(chi)-fast).min())
                assert margin > -3e-10 and ordering > -3e-10
                rev = stepped_response(Ks, weights, Gamma, ports, -speed)
                assert_close(rev, chi.T, "Schedule reversal")
                smallest_disk = min(smallest_disk, float(margin))
                smallest_matrix = min(smallest_matrix, float(ordering))
                previous = sym(chi)
            rows.append(dict(dimension=n, fast=float(a_fast), slow=float(a_slow),
                             old_left_endpoint=float(1/h), smallest_disk_margin=smallest_disk,
                             smallest_matrix_order_margin=smallest_matrix))
    return dict(waveforms=len(rows), rates_per_waveform=len(speeds), rows=rows,
                scope="Exact stepped propagators; finite examples do not prove the universal inequalities.")


def test_spectral_bridge():
    residual = 0.
    mass_error = 0.
    observed_modes = []
    for nphase in [7, 11, 17]:
        Ks = [four_coordinate(2*np.pi*i/nphase) for i in range(nphase)]
        ports = np.eye(4)[:, :2]
        K, D, P, B, values, weights = collocation(Ks, np.eye(4), ports)
        zero = abs(values) < 1e-9
        fast, slow, _ = endpoints(Ks, np.ones(nphase)/nphase, ports)
        mass_error = max(mass_error, assert_close(weights.sum(), np.trace(slow)/2, "Total spectral mass"),
                         assert_close(weights[zero].sum(), np.trace(fast)/2, "Zero-mode mass"))
        active = (weights > 1e-11) & ~zero
        active_mean = float(np.dot(values[active], weights[active])/weights[active].sum())
        spread = float(np.max(abs(values[active]-active_mean)))
        assert spread < 1e-10
        observed_modes.append(dict(phases=nphase, signed_nonzero_mode=active_mean, spread=spread))
        for speed in [.07, .4, np.sqrt(3.), 7.]:
            chi = P.T @ np.linalg.solve(K+speed*D, P)
            zsum = np.sum(weights/(1-1j*speed*values))
            z = (np.trace(chi)+1j*(chi[0, 1]-chi[1, 0]))/2
            residual = max(residual, assert_close(zsum, z, "Spectral resolvent sum"),
                           assert_close(chi, four_response(speed), "Four-mode analytic dynamics"))
    return dict(grid_checks=len(observed_modes), rates_per_grid=4,
                maximum_resolvent_residual=residual, maximum_endpoint_mass_error=mass_error,
                occupied_nonzero_modes=observed_modes,
                scope="Finite spectral matrices verify a formula with an analytic periodic solution; no general collocation convergence is claimed.")


def test_controls():
    P = np.eye(2)
    # A static anisotropic matrix: the stronger disk collapses exactly.
    K = np.diag([1., 3.])
    fast, slow, h = endpoints([K], [1.], P)
    static_radius = (np.trace(slow)-np.trace(fast))/4
    old_radius = (np.trace(slow)/2-1/h)/2
    assert_close(static_radius, 0., "Static collapse")
    assert old_radius > .08
    # Changing scalar stiffness gives a positive static gap but no cross-response.
    Ks = [np.eye(2), 3*np.eye(2), 2*np.eye(2)]
    weights = [1/3]*3
    fast, slow, _ = endpoints(Ks, weights, P)
    radius = (np.trace(slow)-np.trace(fast))/4
    assert radius > 0
    for speed in [.1, 1., 8.]:
        chi = stepped_response(Ks, weights, np.eye(2), P, speed)
        assert_close(chi, np.trace(chi)/2*np.eye(2), "Scalar no-handedness control")
    # A positive Hermitian part alone is insufficient for the stiffness ceiling.
    J = np.array([[0., -1.], [1., 0.]])
    chi_direct_skew = np.linalg.inv(2*np.eye(2)+J)
    beta_direct = (chi_direct_skew[1, 0]-chi_direct_skew[0, 1])/2
    assert_close(beta_direct, -.2, "Skew acting directly on ports")
    # This last matrix is NOT an admissible reciprocal-stiffness static device.
    return dict(static_refined_radius=float(static_radius), static_old_radius=float(old_radius),
                scalar_modulation_radius=float(radius), direct_skew_beta=float(beta_direct),
                direct_skew_is_admissible=False)


def test_sharp_numbers():
    root = np.sqrt(3.)
    fast = 1/root
    slow = (4-root)/3
    beta = (slow-fast)/2
    chi = four_response(root)
    assert_close(beta, (chi[1, 0]-chi[0, 1])/2, "Half static gap")
    assert_close(np.trace(chi)/2, (slow+fast)/2, "Midpoint direct compliance")
    # A symmetric-part prediction at all speeds, not a monotonicity claim for beta.
    rates = [.1, .5, 1., root, 4., 20.]
    rows = []
    for speed in rates:
        c = four_response(speed)
        rows.append(dict(speed=float(speed), direct=float(np.trace(c)/2), beta=float(c[1, 0])))
    assert all(rows[i]['direct'] > rows[i+1]['direct'] for i in range(len(rows)-1))
    assert rows[3]['beta'] > rows[0]['beta'] and rows[3]['beta'] > rows[-1]['beta']
    return dict(fast=fast, slow=slow, endpoint_gap=slow-fast,
                half_gap=beta, optimal_speed=root, response=chi.tolist(), speed_scan=rows)


def run_checks():
    result = {}
    for name, fn in [("stepped_endpoint_bounds", test_endpoints), ("spectral_resolvent", test_spectral_bridge),
                     ("negative_controls", test_controls), ("attaining_example", test_sharp_numbers)]:
        result[name] = fn()
    return result


def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("operator_bridge.local.json"))
    args = parser.parse_args()
    result = run_checks()
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print("PASS four operator-bridge groups")


if __name__ == "__main__":
    main()
