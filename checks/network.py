#!/usr/bin/env python3
"""Small decisive checks for the internal-coordinate mechanics result.

The proof is in RESULT.md. Random waveforms test algebra, not optimality.
No source code from preceding rounds is imported. Requires NumPy and SciPy.
"""
from __future__ import annotations
import argparse
import json
import math
import platform
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import expm
from scipy.integrate import solve_ivp

I2 = np.eye(2)
J = np.array([[0., -1.], [1., 0.]])
SEED = 20260929


def close(actual, expected, label: str, tol: float = 2e-9) -> float:
    err = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    if not np.isfinite(err) or err > tol:
        raise AssertionError(f'{label}: {err} > {tol}')
    return err


def rotation(phi: float) -> np.ndarray:
    return np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])


def complex_matrix(z: complex) -> np.ndarray:
    return np.array([[z.real, -z.imag], [z.imag, z.real]])


def response_parameters(chi: np.ndarray) -> tuple[float, float]:
    return float(np.trace(chi) / 2), float((chi[1, 0] - chi[0, 1]) / 2)


def hidden_parameters(m: float, M: float, h: float | None = None):
    if not 0 < m < M:
        raise ValueError('Require 0 < m < M')
    D = m * M
    h = math.sqrt(D) if h is None else h
    if not m < h < M:
        raise ValueError('Interior h required for a nonzero coupling')
    g = m + M - h
    coupling = math.sqrt((M - h) * (h - m))
    return dict(m=m, M=M, D=D, h=h, g=g, coupling=coupling)


def hidden_stiffness(t: float, params: dict, omega: float) -> np.ndarray:
    h, g, b = (params[key] for key in ('h', 'g', 'coupling'))
    R = rotation(omega * t)
    return np.block([[h * I2, b * R], [b * R.T, g * I2]])


def exact_hidden(params: dict, omega: float, hidden_drag: float = 1., load=None):
    h, g, b = (params[key] for key in ('h', 'g', 'coupling'))
    load = np.zeros((2, 2)) if load is None else np.asarray(load)
    effective = h * I2 - b*b * np.linalg.inv(g * I2 - hidden_drag * omega * J)
    return np.linalg.inv(effective + load), effective


def stepped_solution(Ks: list[np.ndarray], durations: np.ndarray,
                     Gamma: np.ndarray, ports: np.ndarray) -> dict:
    """Exact matrix exponentials for the periodic forced solution; quadrature for energies."""
    n = len(Gamma)
    phi, aff = np.eye(n), np.zeros_like(ports)
    segments = []
    for K, dt in zip(Ks, durations):
        B = np.linalg.solve(Gamma, K)
        E = expm(-dt * B)
        eq = np.linalg.solve(K, ports)
        segments.append((K, dt, B, E, eq))
        phi, aff = E @ phi, E @ aff + (np.eye(n) - E) @ eq
    first = np.linalg.solve(np.eye(n) - phi, aff)
    cur = first.copy()
    integral = np.zeros_like(ports)
    f = (ports[:, 0] + 1j * ports[:, 1]) / np.sqrt(2)
    period = float(sum(durations))
    h = jstat = energy = rk_norm = 0.
    constraint = 0j
    # h is known before evaluating the projection residual.
    for K, dt in zip(Ks, durations):
        h += dt * float(np.vdot(f, K @ f).real) / period
        jstat += dt * float(np.vdot(f, np.linalg.solve(K, f)).real) / period
    nodes, weights = np.polynomial.legendre.leggauss(24)
    for K, dt, B, E, eq in segments:
        integral += eq * dt + np.linalg.solve(B, (np.eye(n) - E) @ (cur - eq))
        for z, w in zip(nodes, weights):
            time = dt * (z + 1) / 2
            X = eq + expm(-time * B) @ (cur - eq)
            y = (X[:, 0] + 1j * X[:, 1]) / np.sqrt(2)
            r = y - f/h
            wt = dt*w/(2*period)
            energy += wt * float(np.vdot(y, K @ y).real)
            rk_norm += wt * float(np.vdot(r, K @ r).real)
            constraint += wt * np.vdot(f, K @ y)
        cur = E @ cur + (np.eye(n) - E) @ eq
    periodic_error = close(cur, first, 'periodic closure')
    chi = ports.T @ integral / period
    alpha, beta = response_parameters(chi)
    close(energy, alpha, 'periodic quadratic balance', 1e-8)
    close(constraint, 1., 'constant-force projection', 1e-8)
    close(rk_norm, alpha - 1/h, 'weighted residual norm', 1e-8)
    margin = (alpha - 1/h) * (jstat - alpha) - beta*beta
    if margin < -1e-9:
        raise AssertionError(f'Conditional disk violation: {margin}')
    return dict(alpha=alpha, beta=beta, h=h, jstat=jstat,
                conditional_margin=margin, periodic_error=periodic_error)


def test_arbitrary_dimensions() -> dict:
    rng = np.random.default_rng(SEED)
    rows = []
    for n in (2, 3, 4, 6):
        for case in range(4):
            ports, _ = np.linalg.qr(rng.normal(size=(n, 2)))
            G = rng.normal(size=(n, n))
            Gamma = .4*np.eye(n) + G.T @ G / n
            Ks = []
            for _ in range(3 + case % 2):
                Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
                eigs = rng.uniform(1., 3., n)
                # Both endpoints occur; the other eigenvalues need not have fixed trace.
                eigs[0], eigs[-1] = 1., 3.
                Ks.append((Q * eigs) @ Q.T)
            durations = rng.uniform(.1, 1., len(Ks))
            r = stepped_solution(Ks, durations, Gamma, ports)
            a, b, h = r['alpha'], r['beta'], r['h']
            if r['jstat'] > (4-h)/3 + 2e-10:
                raise AssertionError('Inverse chord inequality')
            lens = (2/3)**2 - (a - 2/3)**2 - (abs(b) + 1/np.sqrt(3))**2
            if lens < -2e-9:
                raise AssertionError('Universal response envelope')
            rows.append(dict(dimension=n, anisotropic_drag=True, **r, lens_margin=lens))
    return dict(cases=len(rows), rows=rows,
                scope='Structured finite-waveform diagnostics; universal claims use the proof.')


def test_sharpness() -> dict:
    rows = []
    for m, M in ((1., 2.), (1., 3.), (.2, 4.), (2., 5.)):
        for frac in (.15, .5, .85):
            p = hidden_parameters(m, M, m+frac*(M-m))
            h, g, b, D = (p[x] for x in ('h', 'g', 'coupling', 'D'))
            for rate in (.3, 1., 3.):
                omega = rate * D/h
                chi, _ = exact_hidden(p, omega)
                alpha, beta = response_parameters(chi)
                close(beta*beta, (alpha-1/h)*(g/D-alpha), 'Fixed-h boundary')
                specerr = 0.
                for phase in (0., .31, 1.7):
                    specerr = max(specerr, close(np.linalg.eigvalsh(hidden_stiffness(phase/omega, p, omega)),
                                                [m,m,M,M], 'Instantaneous stiffness spectrum'))
                rows.append(dict(m=m,M=M,h=h,omega=omega,alpha=alpha,beta=beta,spectral_error=specerr))
        p = hidden_parameters(m, M)
        chi, _ = exact_hidden(p, p['D']/p['h'])
        alpha, beta = response_parameters(chi)
        bound = .5*(1/np.sqrt(m)-1/np.sqrt(M))**2
        close(beta, bound, 'Unrestricted local-allocation optimum')
        close(alpha, (m+M)/(2*m*M), 'Optimal direct compliance')
    # Equality at all positive-beta envelope points, not a numerical envelope search.
    m, M = 1., 3.
    envelope_rows=[]
    for alpha in np.linspace(1/M+.015, 1/m-.015, 11):
        h = math.sqrt((m+M)/alpha-m*M)
        beta = (math.sqrt((m+M)*alpha-m*M*alpha*alpha)-1)/math.sqrt(m*M)
        p = hidden_parameters(m, M, h)
        omega = p['D']*beta/(h*(alpha-1/h))
        chi, _ = exact_hidden(p, omega)
        aa,bb=response_parameters(chi)
        close([aa,bb],[alpha,beta], 'Envelope boundary realization', 1e-8)
        envelope_rows.append(dict(alpha=alpha,beta=beta,h=h,omega=omega))
    return dict(gate_free_closed_form_checks=len(rows), rows=rows, envelope_points=envelope_rows)


def test_time_domain() -> dict:
    p = hidden_parameters(1., 3.)
    omega=p['D']/p['h']; period=2*np.pi/omega
    rows=[]
    cases=[('unloaded',np.zeros((2,2)),np.eye(2)),
           ('spring',np.eye(2),np.eye(2)),
           ('anisotropic_spring',np.array([[.7,.2],[.2,.3]]),np.eye(2)),
           ('visible_damper',np.zeros((2,2)),np.diag([2.,3.]))]
    ports=np.vstack([I2,np.zeros((2,2))])
    for name, load, port_drag in cases:
        Gamma=np.block([[port_drag,np.zeros((2,2))],[np.zeros((2,2)),I2]])
        def rhs(t, state):
            K=hidden_stiffness(t,p,omega)
            K[:2,:2] += load
            return np.linalg.solve(Gamma, ports-K@state.reshape(4,2)).ravel()
        end=22*period
        sol=solve_ivp(rhs,(0,end),np.zeros(8),method='DOP853',rtol=2e-10,atol=2e-12,
                      dense_output=True,max_step=period/36)
        if not sol.success: raise RuntimeError(sol.message)
        times=np.linspace(end-period,end,301)
        traj=sol.sol(times).T.reshape(-1,4,2)
        mean=np.trapezoid(traj,times,axis=0)/period
        pred,effective=exact_hidden(p,omega,load=load)
        error=close(mean[:2],pred,'From-rest loaded response',2e-8)
        ripple=float(np.ptp(traj[:,:2,:],axis=0).max())
        if ripple>3e-8: raise AssertionError('Port retains micromotion')
        base,_=exact_hidden(p,omega)
        close(pred,np.linalg.inv(np.linalg.inv(base)+load),'Static port composition')
        power_mod=[]; diss=[]
        for t,Y in zip(times,traj):
            r=rotation(omega*t)
            dK=np.block([[np.zeros((2,2)),p['coupling']*omega*J@r],
                         [(p['coupling']*omega*J@r).T,np.zeros((2,2))]])
            v=rhs(t,Y.ravel()).reshape(4,2)
            # First probe force only. Port is stationary in the periodic state.
            power_mod.append(.5*Y[:,0]@dK@Y[:,0])
            diss.append(v[:,0]@Gamma@v[:,0])
        power=float(np.trapezoid(power_mod,times)/period)
        drag_power=float(np.trapezoid(diss,times)/period)
        close(power,drag_power,'Modulation supplies internal drag loss',2e-8)
        rows.append(dict(name=name,port_response=mean[:2].tolist(),max_response_error=error,
                         port_peak_to_peak_motion=ripple,modulation_power=power,drag_power=drag_power))
    # Independent clamped-port run; the reaction must match inverse DC compliance.
    x=np.array([1.,.2])
    def hidden_rhs(t,y): return -p['g']*y-p['coupling']*rotation(omega*t).T@x
    end=18*period
    sol=solve_ivp(hidden_rhs,(0,end),np.zeros(2),method='DOP853',rtol=2e-10,atol=2e-12,
                  dense_output=True,max_step=period/36)
    times=np.linspace(end-period,end,301);ys=sol.sol(times).T
    forces=np.array([p['h']*x+p['coupling']*rotation(omega*t)@y for t,y in zip(times,ys)])
    _,eff=exact_hidden(p,omega)
    mean=np.trapezoid(forces,times,axis=0)/period
    err=close(mean,eff@x,'Clamped reaction and free-force inverse agree',2e-8)
    return dict(from_rest_cases=rows,clamped_reaction=mean.tolist(),clamped_error=err)


def test_spring_synthesis() -> dict:
    p=hidden_parameters(1.,3.); omega=p['D']/p['h']; eta=.1
    e=np.eye(4); maxerr=0.; minimum=math.inf
    for phase in np.linspace(0,2*np.pi,81,endpoint=False):
        R=rotation(phase); K=np.zeros((4,4)); rowdiag=np.zeros(2); coldiag=np.zeros(2)
        for i in range(2):
            for j in range(2):
                c=p['coupling']*math.sqrt(R[i,j]**2+eta**2)
                rowdiag[i]+=c; coldiag[j]+=c
                for sign in (-1,1):
                    n=(e[i]+sign*e[2+j])/math.sqrt(2)
                    spring=c+sign*p['coupling']*R[i,j]
                    minimum=min(minimum,spring)
                    K+=spring*np.outer(n,n)
        for i in range(2):
            kp=p['h']-rowdiag[i];kh=p['g']-coldiag[i]
            minimum=min(minimum,kp,kh)
            K+=kp*np.outer(e[i],e[i])+kh*np.outer(e[2+i],e[2+i])
        maxerr=max(maxerr,close(K,hidden_stiffness(phase/omega,p,omega),'Positive elastic-element synthesis'))
    if minimum<=0: raise AssertionError('A spring coefficient becomes nonpositive')
    return dict(phases=81,rank_one_elements=12,smoothing_eta=eta,
                minimum_coefficient=minimum,max_matrix_error=maxerr,
                qualification='Generalized Hookean elements on fixed signed coordinate combinations, not a laboratory layout.')


def test_fair_budget() -> dict:
    m,M=1.,3.; k=2.;a=1.;D=3.
    p=hidden_parameters(m,M)
    newchi,_=exact_hidden(p,D/p['h'])
    newbeta=response_parameters(newchi)[1]
    oldbeta=a*a/(2*k*D)
    # Four-mode reference = old two-mode rotation plus an uncoupled static pair.
    maxspectral=0.
    for phi in (0.,.2,2.1):
        A=np.array([[np.cos(phi),np.sin(phi)],[np.sin(phi),-np.cos(phi)]])
        oldK=np.block([[k*I2+a*A,np.zeros((2,2))],[np.zeros((2,2)),np.diag([m,M])]])
        maxspectral=max(maxspectral,close(np.linalg.eigvalsh(oldK),[m,m,M,M],'Padded reference spectrum'))
    # Fixing mean port stiffness h=k prevents the spectral-allocation improvement.
    fixed=hidden_parameters(m,M,k); fixedchi,_=exact_hidden(fixed,D/k)
    close(response_parameters(fixedchi)[1],oldbeta,'Fixed port budget retains planar ceiling')
    return dict(old_beta=oldbeta,new_beta=newbeta,relative_increase=newbeta/oldbeta-1,
                old_port_mean_stiffness=k,new_port_mean_stiffness=p['h'],
                common_instantaneous_spectrum=[m,m,M,M],common_trace=2*(m+M),
                fixed_port_budget_max_beta=response_parameters(fixedchi)[1],reference_spectral_error=maxspectral,
                qualification='Same four coordinates, drag, spectral bounds and total trace; different allocation to measured coordinates.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('results.json'))
    args=parser.parse_args()
    result=dict(status='PASS',date='2026-09-29',seed=SEED,
                versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
                scope='Analytic follow-up; numerical consistency checks, not an independent proof or novelty audit.')
    for name,fn in [('arbitrary_dimensions',test_arbitrary_dimensions),('sharpness',test_sharpness),
                    ('time_domain',test_time_domain),('positive_spring_synthesis',test_spring_synthesis),
                    ('resource_matched_comparison',test_fair_budget)]:
        result[name]=fn();print(name,'PASS',flush=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print('WROTE',args.output)


if __name__=='__main__': main()
