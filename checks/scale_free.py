#!/usr/bin/env python3
"""Small checks of scale-free mechanical reciprocity bounds.

No project module is imported. Universal claims use the analytic note, not these
finite examples. Run: python scale_free.py --output scale-free.local.json
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp

I2=np.eye(2)
J=np.array([[0.,-1.],[1.,0.]])
SEED=20260930

def require(ok, message):
    if not ok: raise AssertionError(message)

def near(a,b,label,tol=2e-9):
    e=float(np.max(abs(np.asarray(a)-np.asarray(b))))
    require(np.isfinite(e) and e<tol,f'{label}: {e} >= {tol}')
    return e

def sym(A): return (A+A.T)/2

def asymmetry(A):
    S=sym(A)
    e,U=np.linalg.eigh(S)
    require(e[0]>0,'Positive symmetric response required')
    W=(U/np.sqrt(e))@U.T
    return float(np.max(abs(np.linalg.eigvalsh(1j*W@((A-A.T)/2)@W))))

def bound(m,M):
    require(0<m<=M,'Positive spectral endpoints required')
    return (M-m)**2/(4*(M+m)*np.sqrt(m*M))

def plane_response(m,M,h,nu):
    g=m+M-h; b=np.sqrt((M-h)*(h-m))
    G=h*I2-b*b*np.linalg.inv(g*I2-nu*J)
    return np.linalg.inv(G),G,b

def stage_response(Ks,weights,Gamma,clamped=False):
    """Exact affine maps/integrals over a unit-period step sequence."""
    n=len(Gamma); stages=[]
    if clamped:
        nh=n-2
        if nh==0: return sum(w*K for w,K in zip(weights,Ks))
        drag=Gamma[2:,2:]
        for K,t in zip(Ks,weights):
            C=K[2:,2:]; B=K[:2,2:]
            H=np.linalg.solve(drag,C); E=expm(-t*H)
            eq=-np.linalg.solve(C,B.T)
            stages.append((t,H,E,eq,K[:2,:2],B))
    else:
        nh=n; P=np.eye(n)[:,:2]
        for K,t in zip(Ks,weights):
            H=np.linalg.solve(Gamma,K); E=expm(-t*H)
            stages.append((t,H,E,np.linalg.solve(K,P),None,None))
    phi=np.eye(nh); offset=np.zeros((nh,2))
    for t,H,E,eq,A,B in stages:
        phi=E@phi; offset=E@offset+(np.eye(nh)-E)@eq
    initial=np.linalg.solve(np.eye(nh)-phi,offset); q=initial.copy()
    out=np.zeros((2,2))
    for t,H,E,eq,A,B in stages:
        integral=t*eq+np.linalg.solve(H,(np.eye(nh)-E)@(q-eq))
        out+= t*A+B@integral if clamped else integral[:2]
        q=E@q+(np.eye(nh)-E)@eq
    near(q,initial,'periodic solution')
    return out

def universal_checks():
    rng=np.random.default_rng(SEED); ncase=0
    worst_lens=1.; worst_sector=1.; worst_full=0.
    rows=[]
    for n in [2,3,4,6]:
        for ratio in [1.2,3.,9.]:
            for _ in range(3):
                m=1.; M=ratio; D=m*M; k=(m+M)/2
                Ks=[]
                for step in range(3):
                    Q,_=np.linalg.qr(rng.normal(size=(n,n)))
                    e=rng.uniform(m,M,n); e[0]=m; e[-1]=M
                    Ks.append((Q*e)@Q.T)
                W=rng.normal(size=(n,n)); Gamma=.3*np.eye(n)+W@W.T/n
                weights=rng.uniform(.1,1,3); weights/=weights.sum()
                chi=stage_response(Ks,weights,Gamma)
                G=stage_response(Ks,weights,Gamma,True)
                rec={}
                for name,Q in [('force',chi),('clamped',G)]:
                    a=asymmetry(Q); cap=bound(m,M)
                    near(a,abs(Q[1,0]-Q[0,1])/2/np.sqrt(np.linalg.det(sym(Q))),'two-by-two index')
                    require(a<=cap+1e-10,'sector ceiling')
                    eig=np.linalg.eigvalsh(cap*sym(Q)+1j*(Q-Q.T)/2)
                    worst_sector=min(worst_sector,float(eig.min()))
                    require(eig.min()>-2e-10,'sector matrix positivity')
                    for _ in range(10):
                        z=rng.normal(size=2)+1j*rng.normal(size=2); z/=np.linalg.norm(z)
                        zz=np.vdot(z,Q@z)
                        zz=zz*np.sqrt(D) if name=='force' else zz/np.sqrt(D)
                        eta=k/np.sqrt(D)
                        margin=2*eta*zz.real-abs(zz)**2-2*abs(zz.imag)-1
                        worst_lens=min(worst_lens,float(margin))
                        require(margin>-2e-9,'full numerical-range lens')
                    rec[name]=a
                    # Norm is independently invariant under inverse and real congruence.
                    near(asymmetry(np.linalg.inv(Q)),a,'inverse index')
                    T=np.array([[1.,.3],[-.2,1.7]])@np.diag([.4,2.])
                    near(asymmetry(T@Q@T.T),a,'congruence index')
                    for z in range(3):
                        B=rng.normal(size=(2,2)); L=.1*B@B.T
                        require(asymmetry(Q+L)<=a+1e-10,'passive addition')
                worst_full=max(worst_full,float(np.linalg.norm(G@chi-I2)))
                rows.append(dict(dimension=n,contrast=ratio,**rec))
                ncase+=1
    return dict(cases=ncase,rows=rows,minimum_numerical_range_margin=worst_lens,
                minimum_sector_matrix_eigenvalue=worst_sector,
                maximum_G_chi_minus_identity=worst_full,
                scope='General mean force and clamped maps need not be inverses; each has its own bound.')

def equality_checks():
    rows=[]
    for m,M in [(1.,1.2),(1.,3.),(.2,4.),(2.,7.)]:
        k=(m+M)/2; D=m*M; a=(M-m)/2
        chi,G,b=plane_response(m,M,k,np.sqrt(D))
        r=bound(m,M)
        near(asymmetry(chi),r,'balanced force attainment')
        near(asymmetry(G),r,'balanced clamped attainment')
        beta=(chi[1,0]-chi[0,1])/2; kap=(G[0,1]-G[1,0])/2
        prod=(a*a/(k*k+D))**2
        near(beta*kap,prod,'joint product attainment')
        near(np.linalg.det(chi),1/D,'balanced determinant')
        for h in np.linspace(m+.05*(M-m),M-.05*(M-m),11):
            for nu in [.1,1.,5.]:
                C,H,_=plane_response(m,M,h,nu)
                pb=(C[1,0]-C[0,1])/2; pk=(H[0,1]-H[1,0])/2
                require(pb*pk<=prod+1e-10,'joint product bound')
        rows.append(dict(m=m,M=M,index=r,force_compliance=chi.tolist(),clamped_stiffness=G.tolist(),
                         beta=beta,kappa=kap,joint_product=prod))
    # Compare the three existing allocations at one fixed spectrum and rate.
    compare=[]
    for name,h in [('displacement',np.sqrt(3.)),('balanced',2.),('work_per_area',4-np.sqrt(3.))]:
        C,G,b=plane_response(1.,3.,h,np.sqrt(3.))
        compare.append(dict(name=name,h=h,beta=float((C[1,0]-C[0,1])/2),
                            kappa=float((G[0,1]-G[1,0])/2),index=asymmetry(C)))
    return dict(cases=len(rows),rows=rows,comparison=compare)

def loaded_control():
    C,G,b=plane_response(1.,3.,2.,np.sqrt(3.))
    kap=(G[0,1]-G[1,0])/2
    L=kap*np.array([[1.,-1.],[-1.,1.]])
    GL=G+L; CL=np.linalg.inv(GL)
    near(CL[0,1],0.,'one-way cancellation')
    require(abs(CL[1,0])>.01,'nonzero opposite response')
    require(asymmetry(CL)<asymmetry(C),'one-way ratio is not maximal index')
    K0=np.block([[2*I2+L,I2],[I2,2*I2]])
    eig=np.linalg.eigvalsh(K0)
    require(asymmetry(CL)<=bound(eig[0],eig[-1])+1e-12,'loaded actual budget')
    # Independent laboratory-frame integration, from rest.
    P=np.eye(4)[:,:2]; nu=np.sqrt(3.); T=2*np.pi/nu
    def rhs(t,q):
        R=expm(nu*t*J)
        K=np.block([[2*I2+L,R],[R.T,2*I2]])
        return (P-K@q.reshape(4,2)).ravel()
    sol=solve_ivp(rhs,[0,14*T],np.zeros(8),method='DOP853',rtol=1e-10,atol=1e-12,
                  max_step=T/50,dense_output=True)
    require(sol.success,sol.message)
    times=np.linspace(13*T,14*T,501); xs=sol.sol(times).T.reshape(-1,4,2)[:,:2]
    measured=np.trapezoid(xs,times,axis=0)/T
    near(measured,CL,'loaded full dynamics',1e-8)
    ripple=float(np.ptp(xs,axis=0).max()); require(ripple<1e-8,'stationary ports')
    return dict(cases=1,unloaded_index=asymmetry(C),loaded_index=asymmetry(CL),load=L.tolist(),
                loaded_compliance=CL.tolist(),loaded_stiffness_interval=[float(eig[0]),float(eig[-1])],
                response_error=float(np.max(abs(measured-CL))),port_ripple=ripple,
                interpretation='A reciprocal load cancels one cross-response but lowers the asymmetry index; not broadband isolation.')

def force_displacement_product_control():
    # Analytical family supplies inverse maps; unrelated tests must not be multiplied.
    r=bound(1.,3.); product=r*r/(1+r*r)
    B=.5*(1-1/np.sqrt(3.))**2; K=.5*(np.sqrt(3.)-1)**2
    require(product<B*K,'separate ceilings cannot be reached at once by inverse maps')
    # The familiar rotating planar trap has nonzero force beta but symmetric clamped G.
    k=2.;a=1.;nu=1.5
    C=1/(k-a*a/(k-2j*nu))
    G=k*I2
    require(abs(C.imag)>.01 and asymmetry(G)==0.,'different measurements control')
    # Existing rotary-friction model has nonzero index at m=M, outside this resource class.
    k0=1.; alpha=2.; Gdisk=k0*I2-alpha*J
    near(asymmetry(Gdisk),2.,'rotary substrate model')
    # No claim it is admissible: drive-induced viscous force is an additional resource.
    return dict(cases=3,joint_product_ceiling=product,product_of_separate_ceilings=B*K,
                planar_force_beta=C.imag,planar_clamped_index=0.,rotary_friction_index=2.,
                scalar_spring_only_bound=bound(k0,k0),rotary_model_is_in_class=False)

def calibration_example():
    # Same positive fixed spring basis as the existing construction, at balanced allocation.
    k=2.;b=1.;eta=.1;dfill=b*(1.5+2*eta); ground=k-dfill
    require(ground>0,'positive ground coefficients')
    err=0.
    for phi in np.linspace(0,2*np.pi,65):
        R=expm(phi*J); K=ground*np.eye(4)
        for i in range(2):
            for j in range(2):
                for sig in [-1,1]:
                    v=np.zeros(4); v[i]=1/np.sqrt(2); v[j+2]=sig/np.sqrt(2)
                    coeff=.5*b*(R[i,j]+sig)**2+b*eta
                    require(coeff>=.1-1e-14,'positive connector')
                    K+=coeff*np.outer(v,v)
        target=np.block([[k*I2,b*R],[b*R.T,k*I2]])
        err=max(err,near(K,target,'balanced positive spring synthesis'))
    return dict(cases=65,fixed_support_stiffness=ground,connecting_spring_range=[.1,2.1],max_matrix_error=err)

def run_all():
    groups={}
    for name,fn in [('general_matrix_bounds',universal_checks),('attainment',equality_checks),
                    ('loaded_directionality',loaded_control),('scope_controls',force_displacement_product_control),
                    ('positive_spring_synthesis',calibration_example)]:
        groups[name]=fn(); print('PASS',name,flush=True)
    return dict(status='PASS',seed=SEED,groups=groups,top_level_groups=len(groups),
                interpretation='Analytic consequences of existing bounds; finite diagnostics are not proof or a novelty certificate.')

def main():
    if not __debug__: raise RuntimeError('Run without -O')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=Path('scale-free.local.json'))
    args=p.parse_args(); result=run_all()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')

if __name__=='__main__': main()
