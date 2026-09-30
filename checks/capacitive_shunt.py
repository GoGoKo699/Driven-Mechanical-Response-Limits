#!/usr/bin/env python3
"""Small diagnostics of a direct capacitive piezoelectric shunt.

Two leaky cases use a one-period fundamental map, avoiding long transients.
They illustrate the exact no-go identity: constant positive conductance and
periodic charge imply mean(V)=0 and K_E*mean(q)=P*F. A separate zero-charge,
lossless case recovers the ideal stiffness modulation. These are model checks,
not apparatus data or a numerical proof of the no-go statement.

Run: python checks/capacitive_shunt.py --output capacitive-shunt.local.json
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


def near(actual, expected, label, tolerance=2e-9):
    error = float(np.max(np.abs(np.asarray(actual)-np.asarray(expected))))
    require(np.isfinite(error) and error <= tolerance,
            f'{label}: {error} > {tolerance}')
    return error


def rotation(phase):
    c, s = np.cos(phase), np.sin(phase)
    return np.array([[c, -s], [s, c]])


def design():
    r, reserve, m, gamma = 1.1, .25, 1., 1.
    M = m*np.exp(4*np.arcsinh((1-reserve)*(r-1)/(3*r+5)))
    h = np.sqrt(m*M)
    g, b, eta = m+M-h, np.sqrt((M-h)*(h-m)), 2/(r-1)
    filler = b*(1.5+2*eta)
    support = np.diag([h-filler, h-filler, g-filler, g-filler])
    elements, columns = [], []
    for i in range(2):
        for j in range(2):
            for sign in [-1., 1.]:
                a = np.zeros(4)
                a[i], a[j+2] = 1/np.sqrt(2), sign/np.sqrt(2)
                elements.append((i, j, sign))
                columns.append(a)
    A = np.array(columns).T
    kmin, kmax = b*eta, b*(eta+2)
    kE, kD, Cp = .95*kmin, 1.05*kmax, 1.
    theta = np.sqrt((kD-kE)*Cp)
    KE = support+kE*A@A.T
    return dict(r=r, support_reserve=reserve, m=m, M=M, h=h, g=g,
                b=b, eta=eta, gamma=gamma, Omega=h/gamma,
                kappa_min=kmin, kappa_max=kmax, kE=kE, kD=kD,
                Cp=Cp, theta=theta), support, A, elements, KE


def electrical_state(t, p, elements):
    R = rotation(p['Omega']*t)
    kappa = np.array([.5*p['b']*(R[i, j]+sign)**2+p['b']*p['eta']
                      for i, j, sign in elements])
    Cs = p['theta']**2/(kappa-p['kE'])-p['Cp']
    return kappa, Cs, p['Cp']+Cs


def synthesis_check(p, support, A, elements, KE):
    near(p['kappa_max']/p['kappa_min'], p['r'], 'Spring ratio')
    near(support[0, 0]/p['h'], p['support_reserve'], 'Support reserve')
    require(np.linalg.eigvalsh(support).min() > 0, 'Strictly positive supports')
    require(0 < p['kE'] < p['kappa_min'] < p['kappa_max'] < p['kD'],
            'Piezoelectric stiffness brackets target springs')
    Cs_min = p['theta']**2/(p['kappa_max']-p['kE'])-p['Cp']
    Cs_max = p['theta']**2/(p['kappa_min']-p['kE'])-p['Cp']
    require(0 < Cs_min <= Cs_max and np.isfinite(Cs_max),
            'Finite positive direct shunt capacitance')
    error, spectrum_error = 0., 0.
    for phase in np.linspace(0., 2*np.pi, 17):
        kappa, Cs, S = electrical_state(phase/p['Omega'], p, elements)
        require(np.all(Cs >= Cs_min-1e-12) and np.all(Cs <= Cs_max+1e-12),
                'Capacitance stays in its analytic interval')
        piezo_K = KE+(A*(p['theta']**2/S))@A.T
        spring_K = support+(A*kappa)@A.T
        R = rotation(phase)
        ideal_K = np.block([[p['h']*I2, p['b']*R],
                            [p['b']*R.T, p['g']*I2]])
        error = max(error, near(piezo_K, spring_K, 'Charge-conserving stiffness'),
                    near(piezo_K, ideal_K, 'Eight-spring synthesis'))
        spectrum_error = max(spectrum_error, near(
            np.linalg.eigvalsh(piezo_K), [p['m'], p['m'], p['M'], p['M']],
            'Global stiffness spectrum'))
    return dict(phases=17, capacitance_interval=[Cs_min, Cs_max],
                minimum_support=float(np.linalg.eigvalsh(support).min()),
                maximum_matrix_error=error, maximum_spectrum_error=spectrum_error)


def lossless_check(p, A, elements, KE):
    """Integrate the zero-total-charge branch directly from mechanical rest."""
    period, burn = 2*np.pi/p['Omega'], 30*p['gamma']/p['m']

    def rhs(t, flat):
        q = flat.reshape(4, 2)
        _, _, S = electrical_state(t, p, elements)
        V = -p['theta']*(A.T@q)/S[:, None]
        return ((P-KE@q+A@(p['theta']*V))/p['gamma']).ravel()

    sol = solve_ivp(rhs, (0., burn+period), np.zeros(8), method='DOP853',
                    rtol=1e-10, atol=1e-12, max_step=period/40,
                    dense_output=True)
    require(sol.success, sol.message)
    times = np.linspace(burn, burn+period, 129)
    q = sol.sol(times).T.reshape(-1, 4, 2)
    C = ((p['g']-1j*p['gamma']*p['Omega'])
         /(p['m']*p['M']-1j*p['h']*p['gamma']*p['Omega']))
    X = C.real*I2+C.imag*J
    mean = np.trapezoid(q[:, :2], times, axis=0)/period
    error = near(mean, X, 'Lossless ideal compliance')
    ripple = float(np.ptp(q[:, :2], axis=0).max())
    require(ripple < 2e-9, 'Lossless stationary measured coordinates')
    beta = float((mean[1, 0]-mean[0, 1])/2)
    Bstar = .5*(1/np.sqrt(p['m'])-1/np.sqrt(p['M']))**2
    near(beta, Bstar, 'Lossless sharp odd response')
    require(beta > 1e-5, 'Resolved nonzero lossless response')
    return dict(charge='Z=0 conserved', beta=beta, ideal_beta=Bstar,
                mean_compliance=mean.tolist(), response_error=error,
                port_ripple=ripple, rhs_evaluations=sol.nfev)


def leaky_check(G, p, A, elements, KE):
    """Find the periodic state by its fundamental map, then integrate means."""
    require(G > 0, 'Constant positive conductance')
    period = 2*np.pi/p['Omega']
    drive = np.vstack((P/p['gamma'], np.zeros((8, 2))))

    def generator(t):
        _, _, S = electrical_state(t, p, elements)
        coupling = A*(p['theta']/S)
        K = KE+coupling@(p['theta']*A.T)
        return np.block([[-K/p['gamma'], coupling/p['gamma']],
                         [G*coupling.T, -np.diag(G/S)]])

    def fundamental(t, flat):
        Y = flat.reshape(12, 14)
        dY = generator(t)@Y
        dY[:, 12:] += drive
        return dY.ravel()

    initial = np.hstack((np.eye(12), np.zeros((12, 2))))
    fund = solve_ivp(fundamental, (0., period), initial.ravel(), method='DOP853',
                     rtol=2e-11, atol=2e-13, max_step=period/64)
    require(fund.success, fund.message)
    endpoint = fund.y[:, -1].reshape(12, 14)
    phi, affine = endpoint[:, :12], endpoint[:, 12:]
    radius = float(np.max(np.abs(np.linalg.eigvals(phi))))
    require(radius < 1-1e-7, 'Stable periodic state in this finite example')
    initial_state = np.linalg.solve(np.eye(12)-phi, affine)
    static_q = np.linalg.solve(KE, P)
    static_state = np.vstack((static_q, p['theta']*A.T@static_q))
    static_error = near(initial_state, static_state,
                        'Attracting periodic state is the static zero-voltage state')
    maximum_static_residual = 0.
    for phase_fraction in [0., .37, .81]:
        maximum_static_residual = max(maximum_static_residual, near(
            generator(phase_fraction*period)@initial_state+drive, 0.,
            'Static state satisfies the driven equations at every sampled phase'))

    def state_and_means(t, flat):
        Y = flat[:24].reshape(12, 2)
        q, Z = Y[:4], Y[4:]
        _, _, S = electrical_state(t, p, elements)
        V = (Z-p['theta']*(A.T@q))/S[:, None]
        # Re-evaluate the constitutive equations independently of generator().
        qdot = (P-KE@q+A@(p['theta']*V))/p['gamma']
        Zdot = -G*V
        return np.r_[qdot.ravel(), Zdot.ravel(), q.ravel(), V.ravel()]

    sol = solve_ivp(state_and_means, (0., period),
                    np.r_[initial_state.ravel(), np.zeros(24)], method='DOP853',
                    rtol=2e-11, atol=2e-13, max_step=period/64)
    require(sol.success, sol.message)
    closure = near(sol.y[:24, -1].reshape(12, 2), initial_state,
                   'Full periodic-state closure')
    mean_q = sol.y[24:32, -1].reshape(4, 2)/period
    mean_V = sol.y[32:48, -1].reshape(8, 2)/period
    q_error = near(mean_q, np.linalg.solve(KE, P), 'Leaky reciprocal mean response')
    V_error = near(mean_V, 0., 'Leaky mean voltage vanishes')
    balance_error = near(KE@mean_q-A@(p['theta']*mean_V), P,
                         'Mean mechanical force balance')
    beta = float((mean_q[1, 0]-mean_q[0, 1])/2)
    near(beta, 0., 'Leaky odd mean response vanishes')
    return dict(conductance=G, floquet_radius=radius,
                static_state_error=static_error,
                maximum_static_equation_residual=maximum_static_residual,
                periodic_solve_condition=float(np.linalg.cond(np.eye(12)-phi)),
                mean_compliance=mean_q[:2].tolist(), beta=beta,
                maximum_mean_voltage=V_error, reciprocal_response_error=q_error,
                mean_force_balance_error=balance_error, periodic_closure_error=closure,
                rhs_evaluations=fund.nfev+sol.nfev,
                integrated_periods=2)


def main():
    if not __debug__:
        raise RuntimeError('Run without -O: scientific diagnostic assertions must be enabled')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'capacitive-shunt.local.json')
    args = parser.parse_args()
    if args.output.resolve() == (ROOT/'checks/reference.json').resolve():
        parser.error('The stored reference file cannot be overwritten by this diagnostic')
    p, support, A, elements, KE = design()
    synthesis = synthesis_check(p, support, A, elements, KE)
    print('PASS positive_capacitive_synthesis', flush=True)
    lossless = lossless_check(p, A, elements, KE)
    print('PASS charge_conserving_lossless_response', flush=True)
    leaky = []
    for G in [.2, .02]:
        leaky.append(leaky_check(G, p, A, elements, KE))
        print(f'PASS leaky_periodic_no_go G={G:g}', flush=True)
    result = dict(status='PASS', parameters=p, synthesis=synthesis,
                  lossless=lossless, leaky=leaky,
                  environment=dict(python=platform.python_version(),
                                   numpy=np.__version__, scipy=scipy.__version__),
                  scope='Synthetic constitutive-model diagnostics, not apparatus data. '
                        'The leaky result concerns the asymptotic periodic DC mean; '
                        'it does not exclude finite-time effects or other shunt circuits.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')


if __name__ == '__main__':
    main()
