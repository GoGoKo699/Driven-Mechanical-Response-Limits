#!/usr/bin/env python3
"""Displacement-controlled response and fully charged work-cycle diagnostics.

No inherited scientific module is imported. Proofs and source comparisons are in
    docs/PORT_WORK.md
Run from any directory: python checks/port_work.py --output port-work.local.json
"""
from __future__ import annotations
import argparse
import json
import math
import platform
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.linalg import expm

I = np.eye(2)
J = np.array([[0., -1.], [1., 0.]])
SEED = 2026093008


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def near(a, b, message, tol=3e-9):
    error = float(np.max(np.abs(np.asarray(a)-np.asarray(b))))
    require(np.isfinite(error) and error <= tol, f'{message}: {error} > {tol}')
    return error


def rot(phi):
    c, s = np.cos(phi), np.sin(phi)
    return np.array([[c, -s], [s, c]])


def design(m=1., M=3., kind='compliance', drag=1.):
    require(0 < m < M and drag > 0, 'Positive stiffness interval and drag required')
    root = np.sqrt(m*M)
    h = root if kind == 'compliance' else m+M-root
    g = m+M-h
    b = np.sqrt((M-h)*(h-m))
    return dict(m=m, M=M, h=h, g=g, b=b, gamma_y=drag,
                gamma_x=1., Omega=root/drag, kind=kind)


def Kmatrix(t, p):
    B = p['b']*rot(p['Omega']*t)
    return np.block([[p['h']*I, B], [B.T, p['g']*I]])


def stiffness_dc(p, Omega=None):
    Omega = p['Omega'] if Omega is None else Omega
    return p['h']*I-p['b']**2*np.linalg.inv(p['g']*I-p['gamma_y']*Omega*J)


def odd_stiffness(G):
    return float((G[0, 1]-G[1, 0])/2)


def stepped_clamp(Ks, fractions, damping, speed):
    """Exact periodic affine solution at fixed measured coordinates x.

    Hidden solution is y=Y(t)x. Integrated reaction includes A+B Y, not an
    inverse of a separately measured force-controlled mean compliance.
    """
    r = damping.shape[0]
    period = 1/speed
    phi, affine = np.eye(r), np.zeros((r, 2))
    segments = []
    for K, fraction in zip(Ks, fractions):
        A, B, C = K[:2, :2], K[:2, 2:], K[2:, 2:]
        dt = fraction*period
        rate = np.linalg.solve(damping, C)
        E = expm(-dt*rate)
        eq = -np.linalg.solve(C, B.T)
        phi, affine = E@phi, E@affine+(np.eye(r)-E)@eq
        segments.append((A, B, C, dt, rate, E, eq))
    initial = np.linalg.solve(np.eye(r)-phi, affine)
    Y = initial.copy()
    integral = np.zeros((2, 2))
    for A, B, C, dt, rate, E, eq in segments:
        integrated = dt*eq+np.linalg.solve(rate, (np.eye(r)-E)@(Y-eq))
        integral += dt*A+B@integrated
        Y = E@Y+(np.eye(r)-E)@eq
    near(Y, initial, 'Periodic hidden closure')
    return integral/period


def clamp_references(Ks, fractions):
    slow = sum(w*(K[:2, :2]-K[:2, 2:]@np.linalg.solve(K[2:, 2:], K[2:, :2]))
               for w, K in zip(fractions, Ks))
    mean = sum(w*K for w, K in zip(fractions, Ks))
    fast = mean[:2, :2]-mean[:2, 2:]@np.linalg.solve(mean[2:, 2:], mean[2:, :2])
    rho = sum(w*np.trace(K[:2, 2:]@np.linalg.solve(K[2:, 2:], K[2:, :2]))/2
              for w, K in zip(fractions, Ks))
    return slow, fast, float(rho)


def test_universal_clamp_bound():
    rng = np.random.default_rng(SEED)
    rows = []
    cap = .5*(np.sqrt(3.)-1.)**2
    for hidden in [1, 2, 4, 6]:
        for _ in range(3):
            n = hidden+2
            Ks = []
            for _ in range(3):
                U, _ = np.linalg.qr(rng.normal(size=(n, n)))
                eigen = rng.uniform(1., 3., n)
                eigen[0], eigen[-1] = 1., 3.
                Ks.append((U*eigen)@U.T)
            fractions = rng.uniform(.1, 1., 3); fractions /= fractions.sum()
            V = rng.normal(size=(hidden, hidden))
            damping = .6*np.eye(hidden)+V.T@V/hidden
            slow, fast, rho = clamp_references(Ks, fractions)
            s, f = np.trace(slow)/2, np.trace(fast)/2
            require(f >= s-1e-11 and rho <= 2*cap+1e-11, 'Static coupling allowance')
            for speed in [.15, 1., 6.]:
                G = stepped_clamp(Ks, fractions, damping, speed)
                alpha, kappa = np.trace(G)/2, odd_stiffness(G)
                slack = (alpha-s)*(f-alpha)-kappa*kappa
                require(slack >= -3e-9, 'Clamped response disk')
                require(abs(kappa) <= cap+2e-10, 'Global clamped ceiling')
                if hidden == 1:
                    require(abs(kappa) <= cap/2+2e-10, 'One-hidden-coordinate half-ceiling')
                reverse = stepped_clamp(Ks[::-1], fractions[::-1], damping, speed)
                near(reverse, G.T, 'Clamped schedule reversal', 2e-8)
                rows.append(dict(hidden=hidden, speed=speed, even=float(alpha), odd=kappa,
                                 disk_slack=float(slack), scalar_coupling_budget=rho))
    return dict(cases=len(rows), rows=rows,
                scope='Exact stage propagation; these samples do not establish the universal proof.')


def test_attainment_and_budget():
    rows = []
    for m, M in [(1., 3.), (1., 2.), (.5, 4.), (2., 5.)]:
        cap = .5*(np.sqrt(M)-np.sqrt(m))**2
        p = design(m, M, 'work', drag=.7)
        G = stiffness_dc(p)
        near(G, .5*(m+M)*I-cap*J, 'Attaining clamped stiffness')
        near(odd_stiffness(G), cap, 'Sharp work-density ceiling')
        for t in [0., .17, 1.3]:
            near(np.linalg.eigvalsh(Kmatrix(t, p)), [m, m, M, M], 'Full spectrum')
        rows.append(dict(m=m, M=M, ceiling=cap, G=G.tolist()))
    comparison = []
    for kind in ['compliance', 'work']:
        p = design(kind=kind); G = stiffness_dc(p); chi = np.linalg.inv(G)
        comparison.append(dict(kind=kind, h=p['h'], g=p['g'], Omega=p['Omega'],
                               beta=float((chi[1, 0]-chi[0, 1])/2),
                               kappa=odd_stiffness(G), work_per_oriented_area=2*odd_stiffness(G)))
        # Same fixed geometry and positive coefficients; only support constants exchange.
        b = p['b']; filler=1.7*b
        require(min(p['h'], p['g']) > filler, 'Positive support constants')
    require(comparison[0]['beta'] > comparison[1]['beta'], 'Compliance selection')
    require(comparison[1]['kappa'] > comparison[0]['kappa'], 'Work-density selection')
    return dict(cases=len(rows)+2, sharp_cases=rows, allocation_comparison=comparison,
                physical_scope='Work per fixed displacement-loop area, not efficiency or maximum power.')


def circular_formula(p, speed, radius):
    require(speed != 0 and radius > 0, 'A nonzero oriented loop is required')
    delta = p['Omega']-speed
    kap = p['b']**2*p['gamma_y']*delta/(p['g']**2+(p['gamma_y']*delta)**2)
    T = 2*np.pi/abs(speed)
    Pdrive = p['Omega']*kap*radius**2
    Pout = speed*(kap-p['gamma_x']*speed)*radius**2
    Dvisible = p['gamma_x']*speed**2*radius**2
    Dhidden = delta*kap*radius**2
    require(Dhidden >= -1e-13, 'Internal dissipation sign')
    return dict(T=T, delta=delta, kappa_at_difference=kap,
                work_out=Pout*T, work_drive=Pdrive*T,
                loss_visible=Dvisible*T, loss_hidden=Dhidden*T,
                efficiency=Pout/Pdrive if Pdrive > 0 and Pout > 0 else None)


def integrate_circle(p, speed, radius=.1):
    """Integrate the laboratory hidden coordinates and independent power ledger."""
    O, gy = p['Omega'], p['gamma_y']
    period = 2*np.pi/abs(speed)
    x = lambda t: radius*rot(speed*t)[:, 0]
    xd = lambda t: speed*J@x(t)
    def hidden(t, y):
        return (-p['g']*y-p['b']*rot(O*t).T@x(t))/gy
    step = min(2*np.pi/max(abs(O), abs(speed)), period)/32
    burn = 32*gy/p['g']
    pre = solve_ivp(hidden, (-burn, 0.), np.zeros(2), method='DOP853',
                    rtol=2e-10, atol=2e-12, max_step=step)
    require(pre.success, 'Transient integration')
    def rhs(t, state):
        y = state[:2]; dy = hidden(t, y)
        B = p['b']*rot(O*t)
        F = p['gamma_x']*xd(t)+p['h']*x(t)+B@y
        Pagent = float(F@xd(t))
        Pmod = float(x(t)@(O*J@B)@y)
        return np.r_[dy, -Pagent, Pmod,
                     p['gamma_x']*float(xd(t)@xd(t)), gy*float(dy@dy)]
    start = np.r_[pre.y[:, -1], np.zeros(4)]
    sol = solve_ivp(rhs, (0., period), start, method='DOP853', rtol=2e-10,
                    atol=2e-12, max_step=step)
    require(sol.success, 'Work-cycle integration')
    final = sol.y[:, -1]; q0=np.r_[x(0.), start[:2]]; q1=np.r_[x(period), final[:2]]
    dV = .5*q1@Kmatrix(period, p)@q1-.5*q0@Kmatrix(0., p)@q0
    expected = circular_formula(p, speed, radius)
    vals = [expected[k] for k in ['work_out', 'work_drive', 'loss_visible', 'loss_hidden']]
    err = near(final[2:]/radius**2, np.array(vals)/radius**2,
               'Independent laboratory energy integration', 2e-7)
    balance = final[3]-final[2]-final[4]-final[5]-dV
    require(abs(balance)/radius**2 < 2e-7, 'Full energy balance')
    return dict(design=p['kind'], speed=speed, radius=radius,
                **expected, max_integral_error_per_radius_squared=err,
                stored_energy_change=float(dV), energy_balance_residual=float(balance))


def test_closed_cycles():
    rows=[]
    for kind in ['compliance', 'work']:
        p=design(kind=kind)
        for speed in [.03, p['Omega']/20, .15, -.15, p['Omega'], 1.3*p['Omega']]:
            rows.append(integrate_circle(p, speed))
    # Quasistatic limit: finite signed work, divergent pump cost, vanishing efficiency.
    p=design(kind='work'); quasistatic=2*np.pi*odd_stiffness(stiffness_dc(p))
    asymptotic=[]
    for speed in [1e-2, 1e-3, 1e-4, 1e-5]:
        v=circular_formula(p, speed, 1.)
        asymptotic.append(dict(speed=speed, **v))
        require(0 < v['efficiency'] < speed/p['Omega'], 'Efficiency inequality')
    require(abs(asymptotic[-1]['work_out']-quasistatic) < 1e-4, 'Quasistatic work')
    require(asymptotic[-1]['work_drive'] > 1e4, 'Internal holding loss not removed')
    return dict(cases=len(rows)+len(asymptotic), full_ode_cases=rows,
                slow_limit=asymptotic, signed_quasistatic_work_per_radius_squared=quasistatic)


def test_non_circular_loop():
    p=design(kind='work'); g=p['g']; gy=p['gamma_y']; b=p['b']; O=p['Omega']
    G=stiffness_dc(p); A=g*I-gy*O*J; radius=.1
    rows=[]
    for speed in [.2, .06, .02]:
        T=2*np.pi/speed
        def x(t):
            z=speed*t
            return radius*np.array([1.2*np.cos(z)+.15*np.cos(2*z), .8*np.sin(z)])
        def xd(t):
            z=speed*t
            return radius*speed*np.array([-1.2*np.sin(z)-.3*np.sin(2*z), .8*np.cos(z)])
        def rhs0(t, w): return (-A@w-b*x(t))/gy
        pre=solve_ivp(rhs0,(-32*gy/g,0),np.zeros(2),method='DOP853',rtol=1e-10,atol=1e-12)
        def rhs(t,state):
            w=state[:2]; v=xd(t); F=p['gamma_x']*v+p['h']*x(t)+b*w
            return np.r_[rhs0(t,w), -F@v, v@v]
        sol=solve_ivp(rhs,(0,T),np.r_[pre.y[:,-1],0.,0.],method='DOP853',rtol=1e-10,
                      atol=1e-12,max_step=min(T/100,.2))
        require(sol.success,'Noncircular loop')
        area=np.pi*radius**2*1.2*.8
        work_qs=2*odd_stiffness(G)*area
        work=sol.y[2,-1]; v2=sol.y[3,-1]
        bound=(p['gamma_x']+gy*b*b/(g*np.sqrt(g*g+(gy*O)**2)))*v2
        require(abs(work-work_qs) <= bound+2e-9, 'Finite-rate work error')
        rows.append(dict(speed=speed, area=area, work=work, quasistatic_work=work_qs,
                         finite_rate_error_bound=bound))
    return dict(cases=len(rows), rows=rows,
                scope='An exact architecture-specific bound for a smooth displacement loop after transients.')


def test_controls():
    p=design(kind='work')
    # Stopped modulation makes static stiffness reciprocal; circular motion costs work.
    stopped={**p, 'Omega':0.}
    q=circular_formula(stopped,.1,.1)
    near(odd_stiffness(stiffness_dc(stopped)),0.,'Drive-off reciprocity')
    require(q['work_out'] < 0 and abs(q['work_drive']) < 1e-13,'Drive-off energy')
    # Simultaneous reversal of pump and imposed loop preserves work and loss totals.
    f=circular_formula(p,.1,.1)
    b=circular_formula({**p,'Omega':-p['Omega']},-.1,.1)
    for k in ['work_out','work_drive','loss_visible','loss_hidden']:
        near(f[k],b[k],'Full reversal '+k)
    # A planar rotating stiffness with every coordinate clamped has zero mean odd stiffness.
    phases=np.linspace(0,2*np.pi,80,endpoint=False)
    mean=sum(2*I+np.array([[np.cos(t),np.sin(t)],[np.sin(t),-np.cos(t)]]) for t in phases)/len(phases)
    near(mean,2*I,'Clamped planar reference')
    # A lossless mechanical gyrator acts on velocity; its skew part does no power.
    rng=np.random.default_rng(SEED+1)
    for _ in range(8):
        v=rng.normal(size=2); near(v@J@v,0.,'Skew velocity force has zero power')
    return dict(cases=4, no_drive_work_out=q['work_out'],
                clamped_planar_odd_stiffness=odd_stiffness(mean),
                meaning='Odd stiffness is not a velocity gyrator or a generic inverse mean compliance.')


def main():
    require(__debug__,'Run without -O')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=Path('port-work.local.json'))
    args=ap.parse_args()
    reference = Path(__file__).resolve().parent/'reference.json'
    if args.output.resolve() == reference.resolve():
        ap.error('The stored reference file cannot be overwritten by this diagnostic')
    groups={}
    for name,fn in [('clamped_bound',test_universal_clamp_bound),
                    ('sharpness_and_allocation',test_attainment_and_budget),
                    ('laboratory_work_cycles',test_closed_cycles),
                    ('noncircular_work',test_non_circular_loop),('controls',test_controls)]:
        groups[name]=fn(); print('PASS '+name,flush=True)
    result=dict(status='PASS',seed=SEED,groups=groups,
                counts=dict(groups=len(groups),cases=sum(r['cases'] for r in groups.values())),
                environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
                scope='Proof diagnostics; not independent review, a hardware test, or an efficiency optimum.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')


if __name__=='__main__': main()
