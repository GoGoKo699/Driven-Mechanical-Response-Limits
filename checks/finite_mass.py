#!/usr/bin/env python3
"""Small independent diagnostics of finite-mass persistence.

The laboratory equation is mu*q'' + gamma*q' + K(t)*q = P*F.
No project scientific module is imported. Four integrations check the existing
rotating construction, not an arbitrary-waveform finite-mass ceiling. The
written Lyapunov proof, rather than these examples, establishes stability.

Run: python checks/finite_mass.py --output finite-mass.local.json
"""
from __future__ import annotations

import argparse
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import solve_ivp


ROOT = Path(__file__).resolve().parents[1]
I2 = np.eye(2)
J = np.array([[0., -1.], [1., 0.]])
P = np.eye(4)[:, :2]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def near(actual, expected, label, tolerance=2e-10):
    error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
    require(np.isfinite(error) and error <= tolerance,
            f'{label}: {error} > {tolerance}')
    return error


def rotation(phase):
    c, s = np.cos(phase), np.sin(phase)
    return np.array([[c, -s], [s, c]])


def parameters(m, M, mu, gamma=1.):
    require(0 < m <= M and mu > 0 and gamma > 0, 'Positive parameters')
    require(mu*M < gamma**2, 'Sufficient uniform stability condition')
    h = np.sqrt(m*M)
    return dict(m=m, M=M, mu=mu, gamma=gamma, h=h, g=m+M-h,
                b=np.sqrt(max(0., (M-h)*(h-m))), Omega=h/gamma)


def stiffness(t, p):
    B = p['b']*rotation(p['Omega']*t)
    return np.block([[p['h']*I2, B], [B.T, p['g']*I2]])


def complex_response(p, mu):
    # This formula is tested against the full laboratory ODE below.
    a = p['g']-mu*p['Omega']**2-1j*p['gamma']*p['Omega']
    denominator = (p['m']*p['M']-p['h']*mu*p['Omega']**2
                   -1j*p['h']*p['gamma']*p['Omega'])
    return a/denominator


def response_matrix(z):
    return z.real*I2+z.imag*J


def lyapunov_check(p):
    """Evaluate Wdot directly from the homogeneous lab equation, off orbit."""
    mu, gamma = p['mu'], p['gamma']
    tau = mu/gamma
    decay_rate = min(p['m']/gamma, gamma/mu-p['M']/gamma)
    states = [
        (np.array([1., -.3, .7, .2]), np.array([-.5, .8, .4, -.9])),
        (np.zeros(4), np.array([1., -2., .5, .7])),
        (np.array([-.2, .6, 1.1, -.8]), np.zeros(4)),
    ]
    identity_error = 0.
    minimum_decay_slack = np.inf
    spectrum_error = 0.
    for phase in [0., .37, 2.1]:
        K = stiffness(phase/p['Omega'], p)
        spectrum_error = max(spectrum_error, near(
            np.linalg.eigvalsh(K), [p['m'], p['m'], p['M'], p['M']],
            'Full instantaneous stiffness spectrum'))
        for q, v in states:
            acceleration = (-gamma*v-K@q)/mu
            z, w = q+tau*v, tau*v
            zdot, wdot = v+tau*acceleration, tau*acceleration
            direct = float(z@zdot+w@wdot)
            formula = float(-z@K@z/gamma
                            -w@(gamma/mu*np.eye(4)-K/gamma)@w)
            scale = max(1., abs(direct), abs(formula))
            error = near(direct/scale, formula/scale, 'Lyapunov identity')
            identity_error = max(identity_error, error)
            W = .5*float(z@z+w@w)
            require(W > 0 and direct < 0, 'Strict homogeneous decay')
            slack = -direct-2*decay_rate*W
            require(slack >= -2e-12, 'Uniform Lyapunov decay inequality')
            minimum_decay_slack = min(minimum_decay_slack, slack)
    return dict(states=9, relative_identity_error=identity_error,
                maximum_spectrum_error=spectrum_error,
                minimum_decay_slack=float(minimum_decay_slack),
                W_decay_rate=2*decay_rate,
                stability_margin_gamma_squared_minus_mu_M=gamma**2-mu*p['M'])


def laboratory_case(p):
    """Integrate both independent unit forces from q=v=0 in lab coordinates."""
    mu, gamma, omega = p['mu'], p['gamma'], p['Omega']
    period = 2*np.pi/omega
    rate = min(p['m']/gamma, gamma/mu-p['M']/gamma)
    burn = 30/rate

    def rhs(t, state):
        q, v = state[:8].reshape(4, 2), state[8:].reshape(4, 2)
        # Construct forces directly in the laboratory frame; no rotating-frame
        # state, response formula, or steady-state initial condition enters.
        B = p['b']*rotation(omega*t)
        restoring = np.vstack((p['h']*q[:2]+B@q[2:],
                               B.T@q[:2]+p['g']*q[2:]))
        acceleration = (P-gamma*v-restoring)/mu
        return np.r_[v.ravel(), acceleration.ravel()]

    sol = solve_ivp(rhs, (0., burn+period), np.zeros(16), method='DOP853',
                    rtol=1e-10, atol=1e-12, max_step=period/32,
                    dense_output=True)
    require(sol.success, sol.message)
    times = np.linspace(burn, burn+period, 129)
    values = sol.sol(times).T
    q, v = values[:, :8].reshape(-1, 4, 2), values[:, 8:].reshape(-1, 4, 2)
    C = complex_response(p, mu)
    X = response_matrix(C)
    internal = -p['b']*np.linalg.solve(
        (p['g']-mu*omega**2)*I2-gamma*omega*J, X)
    expected_q = np.array([np.vstack((X, rotation(omega*t).T@internal))
                           for t in times])
    expected_v = np.zeros_like(expected_q)
    expected_v[:, 2:] = np.array([-omega*J@y[2:] for y in expected_q])
    state_error = near(q, expected_q, 'Laboratory positions', 2e-8)
    velocity_error = near(v, expected_v, 'Laboratory velocities', 2e-8)
    measured = np.trapezoid(q[:, :2], times, axis=0)/period
    response_error = near(measured, X, 'Two-force measured compliance', 2e-8)
    port_ripple = float(np.ptp(q[:, :2], axis=0).max())
    require(port_ripple < 2e-8, 'Stationary measured coordinates')
    # Test the physical rotation independently of the laboratory pointwise fit.
    corotated = np.array([rotation(omega*t)@y[2:] for t, y in zip(times, q)])
    rotation_error = near(corotated, internal, 'Rotating internal coordinates', 2e-8)
    hidden_ripple = float(np.ptp(q[:, 2:], axis=0).max())
    if p['M'] > p['m']:
        require(hidden_ripple > .01, 'Nontrivial moving hidden coordinates')
    else:
        near(hidden_ripple, 0., 'Equal-spectrum uncoupled control')

    Bstar = .5*(1/np.sqrt(p['m'])-1/np.sqrt(p['M']))**2
    epsilon = mu*np.sqrt(p['m']*p['M'])/gamma**2
    factor = 2/((1-epsilon)**2+1)
    beta = float((measured[1, 0]-measured[0, 1])/2)
    near(C.imag, Bstar*factor, 'Exact odd-response formula')
    near(beta, Bstar*factor, 'ODE odd-response formula', 2e-8)
    C0 = complex_response(p, 0.)
    predicted_gap = np.sqrt(2)*Bstar*epsilon/np.sqrt((1-epsilon)**2+1)
    near(abs(C-C0), predicted_gap, 'Exact overdamped-limit error')
    ode_gap = float(np.linalg.norm(measured-response_matrix(C0), ord=2))
    near(ode_gap, predicted_gap, 'ODE overdamped-limit error', 2e-8)
    return dict(parameters=p, lyapunov=lyapunov_check(p),
                response=measured.tolist(), exact_response=X.tolist(),
                beta=beta, overdamped_beta=Bstar, epsilon=epsilon,
                beta_ratio=factor if Bstar > 0 else None,
                exact_gap_to_overdamped=float(abs(C-C0)),
                ode_gap_to_overdamped=ode_gap,
                maximum_position_error=state_error,
                maximum_velocity_error=velocity_error,
                measured_response_error=response_error, port_ripple=port_ripple,
                internal_rotation_error=rotation_error, hidden_ripple=hidden_ripple,
                integration=dict(method='DOP853', start='q=v=0',
                                 burn_time=burn, observed_period=period,
                                 rhs_evaluations=sol.nfev))


def run_all():
    rows = []
    for M in [1., 3.]:
        cases = []
        for mu in [.05, .01]:
            case = laboratory_case(parameters(1., M, mu))
            cases.append(case)
            rows.append(case)
            print(f'PASS finite_mass M={M:g} mu={mu:g}', flush=True)
        if M > 1:
            require(0 < cases[1]['exact_gap_to_overdamped']
                    < cases[0]['exact_gap_to_overdamped'],
                    'Response converges as mass decreases')
            require(all(c['beta'] > c['overdamped_beta'] for c in cases),
                    'The overdamped ceiling is not a finite-mass bound')
    return dict(status='PASS', cases=len(rows), rows=rows,
                environment=dict(python=platform.python_version(),
                                 numpy=np.__version__, scipy=scipy.__version__),
                scope='Finite examples of persistence for scalar mass and drag; '
                      'not a universal finite-mass response bound, physical '
                      'device validation, or numerical proof of stability.')


def main():
    if not __debug__:
        raise RuntimeError('Run without -O: scientific diagnostic assertions must be enabled')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'finite-mass.local.json')
    args = parser.parse_args()
    if args.output.resolve() == (ROOT/'checks/reference.json').resolve():
        parser.error('The stored reference file cannot be overwritten by this diagnostic')
    result = run_all()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')


if __name__ == '__main__':
    main()
