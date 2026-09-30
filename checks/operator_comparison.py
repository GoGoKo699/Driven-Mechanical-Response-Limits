#!/usr/bin/env python3
"""Check the fixed-schedule disk and the positive/skew resolvent connection.

Self-contained finite-dimensional diagnostics, not a universal proof or a new
thermal/stochastic model. The continuum argument is in docs/OPERATOR_CONNECTION.md.
Run directly, or through checks/run.py. NumPy and SciPy only.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import block_diag, expm, null_space

SEED = 20260930
J = np.array([[0., -1.], [1., 0.]])


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def near(x, y, message: str, tol: float = 3e-9) -> float:
    err = float(np.max(np.abs(np.asarray(x) - np.asarray(y))))
    require(np.isfinite(err) and err <= tol, f'{message}: {err} > {tol}')
    return err


def herm(a):
    return (a + a.conj().T) / 2


def root(a, power):
    eig, vec = np.linalg.eigh(herm(a))
    require(eig.min() > 0, 'Positive matrix required')
    return (vec * eig**power) @ vec.conj().T


def random_spd(rng, n, lo=.8, hi=3.2):
    q, _ = np.linalg.qr(rng.normal(size=(n, n)))
    return (q * rng.uniform(lo, hi, n)) @ q.T


def response_scalars(chi):
    return float(np.trace(chi) / 2), float((chi[1, 0]-chi[0, 1])/2)


def finite_operator_checks():
    rng = np.random.default_rng(SEED)
    worst = dict(spectral=0., projector=0., deficit=0., symmetry=0.)
    min_disk = min_loewner = float('inf')
    cases = 0
    for n in (4, 6, 8):
        for _ in range(4):
            A = random_spd(rng, n)
            raw = rng.normal(size=(n-2, n-2))
            S = block_diag(np.zeros((2, 2)), raw-raw.T)
            P = np.eye(n)[:, :2]
            f = (P[:, 0]+1j*P[:, 1])/np.sqrt(2)
            Ap, Am = root(A, .5), root(A, -.5)
            T = herm(-1j * Am @ S @ Am)
            eig, vec = np.linalg.eigh(T)
            w = Am @ f
            weights = np.abs(vec.conj().T @ w)**2
            ker = null_space(S)
            gram = ker.conj().T @ A @ ker
            w0 = Ap @ ker @ np.linalg.solve(gram, ker.conj().T @ f)
            a0 = float(np.vdot(w0, w0).real)
            j = float(np.vdot(w, w).real)
            zero = np.abs(eig) < 1e-10
            worst['projector'] = max(worst['projector'], near(weights[zero].sum(), a0, 'kernel weight'))
            require(a0 >= 1/float((f.conj()@A@f).real)-1e-9, 'original bound containment')
            previous = None
            for speed in (.015, .08, .4, 2., 10., 60.):
                chi = P.T @ np.linalg.solve(A+speed*S, P)
                z = np.vdot(f, np.linalg.solve(A+speed*S, f))
                factors = 1/(1+1j*speed*eig)
                zs = np.dot(weights, factors)
                worst['spectral'] = max(worst['spectral'], near(z, zs, 'spectral resolvent'))
                a, b = response_scalars(chi)
                worst['spectral'] = max(worst['spectral'], near(z, a-1j*b, 'complex force orientation'))
                rho = j-a0
                mean = np.dot(weights[~zero], factors[~zero])/rho
                variance = np.dot(weights[~zero], np.abs(factors[~zero]-mean)**2)/rho
                disk = (a-a0)*(j-a)-b*b
                min_disk = min(min_disk, disk)
                worst['deficit'] = max(worst['deficit'], near(disk, rho*rho*variance, 'modal variance identity'))
                require(disk >= -2e-10, 'endpoint disk')
                H = herm(chi)
                if previous is not None:
                    monotonic = float(np.linalg.eigvalsh(previous-H).min())
                    min_loewner = min(min_loewner, monotonic)
                    require(monotonic >= -2e-10, 'symmetric response not decreasing')
                previous = H
                reverse = P.T @ np.linalg.solve(A-speed*S, P)
                worst['symmetry'] = max(worst['symmetry'], near(reverse, chi.T, 'reversal'))
                cases += 1
    return dict(cases=cases, maximum_errors=worst, minimum_disk_margin=min_disk,
                minimum_loewner_decrease=min_loewner,
                scope='Finite positive-plus-skew systems with forced vectors in the skew kernel.')


def stepped_response(Ks, fractions, Gamma, P, speed):
    n = len(Gamma)
    phi, aff = np.eye(n), np.zeros_like(P)
    data = []
    for K, frac in zip(Ks, fractions):
        dt = frac/speed
        B = np.linalg.solve(Gamma, K)
        E = expm(-dt*B)
        eq = np.linalg.solve(K, P)
        data.append((B, E, eq, dt))
        phi, aff = E@phi, E@aff + (np.eye(n)-E)@eq
    initial = np.linalg.solve(np.eye(n)-phi, aff)
    cur = initial.copy()
    integral = np.zeros_like(P)
    for B, E, eq, dt in data:
        integral += eq*dt + np.linalg.solve(B, (np.eye(n)-E)@(cur-eq))
        cur = E@cur + (np.eye(n)-E)@eq
    near(cur, initial, 'exact periodic closure')
    return P.T @ integral * speed


def periodic_waveform_checks():
    rng = np.random.default_rng(SEED+1)
    rows = []
    min_disk = min_order = float('inf')
    speeds = np.array([.002, .01, .05, .25, 1.25, 6.25, 31.25, 156.25])
    for n in (2, 3, 5):
        for _ in range(3):
            Ks = [random_spd(rng, n) for _ in range(3)]
            fractions = rng.uniform(.1, 1., 3); fractions /= fractions.sum()
            Gamma = random_spd(rng, n, .6, 2.)
            P, _ = np.linalg.qr(rng.normal(size=(n, 2)))
            Kbar = sum(t*K for t,K in zip(fractions,Ks))
            slow = sum(t*(P.T@np.linalg.solve(K, P)) for t,K in zip(fractions,Ks))
            fast = P.T@np.linalg.solve(Kbar, P)
            alow, afast = float(np.trace(slow)/2), float(np.trace(fast)/2)
            h = float(np.trace(P.T@Kbar@P)/2)
            require(afast >= 1/h-2e-10, 'endpoint projection improvement')
            old = None
            path = []
            for speed in speeds:
                chi = stepped_response(Ks, fractions, Gamma, P, float(speed))
                a, b = response_scalars(chi)
                slack = (a-afast)*(alow-a)-b*b
                min_disk = min(min_disk, slack)
                require(slack >= -3e-9, 'periodic endpoint disk')
                if old is not None:
                    dec = float(np.linalg.eigvalsh(herm(old-chi)).min())
                    min_order = min(min_order, dec)
                    require(dec >= -3e-9, 'periodic symmetric monotonicity')
                old = chi
                reverse = stepped_response(list(reversed(Ks)), fractions[::-1], Gamma, P, float(speed))
                near(reverse, chi.T, 'periodic time reversal', 2e-8)
                path.append(dict(speed=float(speed), alpha=a, beta=b))
            rows.append(dict(dimension=n, alpha_slow=alow, alpha_fast=afast,
                             old_left_endpoint=1/h, new_max_beta=(alow-afast)/2, rates=path))
    return dict(cases=len(rows)*len(speeds), waveforms=len(rows), minimum_disk_margin=min_disk,
                minimum_loewner_decrease=min_order, rows=rows,
                scope='Exact affine/exponential solution, not a sampled time derivative.')


def controls():
    # Direct skew force at the observed port violates the required kernel property.
    A = 2*np.eye(2); S = J
    chi = np.linalg.inv(A+S)
    a, b = response_scalars(chi)
    require(abs(b) > .1, 'negative control did not expose missing condition')
    # A two-stage reciprocal schedule has a positive endpoint gap but no odd response.
    R = np.array([[np.cos(.57), -np.sin(.57)], [np.sin(.57), np.cos(.57)]])
    Ks = [np.diag([1.,3.]), R@np.diag([1.,3.])@R.T]
    fractions = np.array([.37,.63])
    Kbar = sum(t*K for t,K in zip(fractions,Ks))
    slow = sum(t*np.linalg.inv(K) for t,K in zip(fractions,Ks))
    fast = np.linalg.inv(Kbar)
    gap = float(np.trace(slow-fast)/2)
    require(gap > 1e-3, 'two-stage endpoint gap')
    betas=[]
    for speed in (.01, .1, 1., 10., 100.):
        c = stepped_response(Ks,fractions,np.eye(2),np.eye(2),speed)
        beta = response_scalars(c)[1]
        near(beta,0.,'two-stage reciprocity',2e-9)
        betas.append(beta)
    # A static anisotropic matrix has equal endpoints: no dynamic budget at all.
    static = np.diag([1.,3.])
    sscalar = np.trace(np.linalg.inv(static))/2
    return dict(cases=7, forbidden_direct_skew_beta=b,
                forbidden_kernel_condition_norm=float(np.linalg.norm(S)),
                two_stage_gap=gap, two_stage_betas=betas,
                static_alpha_slow=sscalar, static_alpha_fast=sscalar,
                static_old_scalar_disk_width=float(sscalar-1/(np.trace(static)/2)),
                scope='A nonzero endpoint gap is necessary, not sufficient, for nonreciprocity.')


def attaining_record():
    h=np.sqrt(3.); g=4-h; b=np.sqrt((3-h)*(h-1))
    A=np.block([[h*np.eye(2),b*np.eye(2)],[b*np.eye(2),g*np.eye(2)]])
    S=block_diag(np.zeros((2,2)),-J)
    P=np.eye(4)[:,:2]; f=(P[:,0]+1j*P[:,1])/np.sqrt(2)
    Am=root(A,-.5); T=herm(-1j*Am@S@Am)
    eig,vec=np.linalg.eigh(T); weights=np.abs(vec.conj().T@Am@f)**2
    active=(weights>1e-10)&(np.abs(eig)>1e-10)
    require(int(active.sum())==1, 'attaining forcing is not single active mode')
    afast=1/h; alow=g/3; cap=(alow-afast)/2
    near(cap,.5*(1-1/np.sqrt(3))**2,'global/endpoint ceiling match')
    rows=[]
    for speed in (.01,.2,np.sqrt(3.),4.,30.):
        c=P.T@np.linalg.solve(A+speed*S,P)
        a,be=response_scalars(c)
        near(be*be,(a-afast)*(alow-a),'attaining endpoint circle')
        rows.append(dict(speed=float(speed),alpha=a,beta=be))
    return dict(cases=len(rows), alpha_slow=float(alow), alpha_fast=float(afast),
                endpoint_ceiling=float(cap), active_nonzero_eigenvalue=float(eig[active][0]),
                active_nonzero_weight=float(weights[active].sum()),
                expected_active_eigenvalue=float(h/3), rows=rows,
                rate_convention='Angular coupling rate Omega; period-one phase speed v=Omega/(2*pi).')


def run_all():
    if not __debug__:
        raise RuntimeError('Run without -O')
    groups={}
    for name, fn in [('finite_resolvents',finite_operator_checks),
                     ('periodic_waveforms',periodic_waveform_checks),
                     ('scope_controls',controls),('attaining_single_mode',attaining_record)]:
        groups[name]=fn()
    return dict(status='PASS', seed=SEED, groups=groups,
                cases=sum(g['cases'] for g in groups.values()),
                scope='Proof diagnostics and prior-art normalization; not a novelty certificate.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=Path('operator-results.local.json'))
    args=p.parse_args()
    result=run_all()
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print('PASS operator comparison:',result['cases'],'finite diagnostic cases')


if __name__=='__main__':
    main()
