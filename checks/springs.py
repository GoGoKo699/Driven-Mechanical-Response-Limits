#!/usr/bin/env python3
"""Small tests of the guided-slider realization and equality constraints.

All scientific inequalities are proved in RESULT.md; finite computations are
consistency checks, not exhaustive searches or experimental observations.
Python >=3.10, NumPy, SciPy. No earlier research code is imported.
"""
from __future__ import annotations
import argparse
import json
import math
import platform
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp, simpson
from scipy.linalg import expm

J = np.array([[0.,-1.],[1.,0.]])
I2 = np.eye(2)
MLOW, MHIGH = 1., 3.
H = math.sqrt(MLOW*MHIGH)
G = MLOW+MHIGH-H
B = math.sqrt((MHIGH-H)*(H-MLOW))
ETA = .1
OMEGA = math.sqrt(MLOW*MHIGH)
PERIOD = 2*math.pi/OMEGA
DIAG_FILL = B*(1.5+2*ETA)
GROUNDS = np.array([H-DIAG_FILL]*2+[G-DIAG_FILL]*2)
BETA_STAR = .5*(1/math.sqrt(MLOW)-1/math.sqrt(MHIGH))**2
CHI_STAR = np.array([[2/3,-BETA_STAR],[BETA_STAR,2/3]])
P = np.eye(4)[:,:2]


def rotation(phi: float) -> np.ndarray:
    c,s=np.cos(phi),np.sin(phi)
    return np.array([[c,-s],[s,c]])


def stiffness(t: float) -> np.ndarray:
    R=rotation(OMEGA*t)
    return np.block([[H*I2,B*R],[B*R.T,G*I2]])


def elements(t: float):
    """Eight modulated axial springs. sigma selects elongation (x_i+sigma*y_j)/sqrt2."""
    R=rotation(OMEGA*t); Rd=OMEGA*J@R
    out=[]
    for i in range(2):
        for j in range(2):
            for sigma in (-1,1):
                v=np.zeros(4);v[i]=1/math.sqrt(2);v[j+2]=sigma/math.sqrt(2)
                k=.5*B*(R[i,j]+sigma)**2+B*ETA
                kd=B*(R[i,j]+sigma)*Rd[i,j]
                out.append((i,j,sigma,k,kd,v))
    return out


def axial_force_energy(t: float,q: np.ndarray,L0: float=1.):
    """Exact lengths of unprestressed axial springs on perpendicular guided sliders.

    Fixed reference separation n=(1,-sigma)/sqrt2. The relative endpoint
    displacement is (-x_i,y_j). All spring rest lengths L0 are fixed.
    """
    force=-GROUNDS*q
    energy=.5*float(np.dot(GROUNDS*q,q))
    drive=0.
    max_strain=0.
    for i,j,sigma,k,kd,v in elements(t):
        n=np.array([1.,-sigma])/math.sqrt(2)
        rel=np.array([-q[i],q[j+2]])
        vec=L0*n+rel
        ell=np.linalg.norm(vec)
        if ell <= .2*L0:
            raise ValueError('Outside the small-displacement geometric regime')
        # Avoid catastrophic cancellation in ell-L0 at small amplitude.
        extension=(2*L0*np.dot(n,rel)+np.dot(rel,rel))/(ell+L0)
        unit=vec/ell
        force[i]+=k*extension*unit[0]
        force[j+2]-=k*extension*unit[1]
        energy+=.5*k*extension**2
        drive+=.5*kd*extension**2
        max_strain=max(max_strain,abs(extension)/L0)
    return force,energy,drive,max_strain


def synthesis_checks():
    max_matrix=max_spectrum=max_hessian=0.
    min_spring=math.inf
    max_spring=0.
    for t in np.linspace(0,PERIOD,65):
        reconstructed=np.diag(GROUNDS)
        for *_,k,kd,v in elements(float(t)):
            reconstructed+=k*np.outer(v,v)
            min_spring=min(min_spring,k);max_spring=max(max_spring,k)
        max_matrix=max(max_matrix,float(np.max(abs(reconstructed-stiffness(float(t))))))
        max_spectrum=max(max_spectrum,float(np.max(abs(np.linalg.eigvalsh(reconstructed)-[1,1,3,3]))))
        # Force Jacobian from actual spring lengths, not from the rank-one formula.
        step=1e-5
        jac=np.zeros((4,4))
        for j in range(4):
            q=np.eye(4)[j]*step
            jac[:,j]=(axial_force_energy(float(t),q)[0]-axial_force_energy(float(t),-q)[0])/(2*step)
        max_hessian=max(max_hessian,float(np.max(abs(jac+stiffness(float(t))))))
    assert min(GROUNDS)>0 and min_spring>0
    assert max_matrix<3e-14 and max_spectrum<3e-14 and max_hessian<2e-9
    return dict(times=65,modulated_springs=8,fixed_support_springs=4,
                fixed_support_constants=GROUNDS.tolist(),minimum_modulated_spring=min_spring,
                maximum_modulated_spring=max_spring,max_stiffness_error=max_matrix,
                max_eigenvalue_error=max_spectrum,max_geometric_jacobian_error=max_hessian)


def steady_integrate(fun,n: int,T: float,cycles: int=11):
    sol=solve_ivp(fun,(0,cycles*T),np.zeros(n),method='DOP853',rtol=2e-10,atol=2e-12,
                  max_step=T/70,dense_output=True)
    if not sol.success:raise RuntimeError(sol.message)
    t=np.linspace((cycles-1)*T,cycles*T,801)
    y=sol.sol(t)
    mean=simpson(y,x=t,axis=1)/T
    return t,y,mean


def geometry_checks():
    rows=[]
    for amplitude in (.02,.005):
        means=np.zeros((4,2,2))
        max_strain=0.;balance=0.;max_port_ripple=0.
        for j in range(2):
            for si,sgn in enumerate((-1,1)):
                f=P[:,j]*amplitude*sgn
                t,q,avg=steady_integrate(lambda tt,xx:axial_force_energy(tt,xx)[0]+f,4,PERIOD)
                means[:,j,si]=avg
                powers=[]; losses=[]; probe=[];energies=[]
                for tt,xx in zip(t,q.T):
                    force,energy,power,strain=axial_force_energy(float(tt),xx)
                    vel=force+f
                    max_strain=max(max_strain,strain)
                    powers.append(power);losses.append(float(vel@vel));probe.append(float(f@vel));energies.append(energy)
                net=(simpson(np.array(powers)+np.array(probe)-np.array(losses),x=t)-(energies[-1]-energies[0]))/PERIOD
                balance=max(balance,abs(float(net))/(amplitude**2))
                max_port_ripple=max(max_port_ripple,float(np.max(np.ptp(q[:2],axis=1))))
        chi=(means[:2,:,1]-means[:2,:,0])/(2*amplitude)
        err=float(np.linalg.norm(chi-CHI_STAR,2))
        beta=float((chi[1,0]-chi[0,1])/2)
        rows.append(dict(force_amplitude=amplitude,rest_length=1.,central_difference_compliance=chi.tolist(),
                         operator_error_against_tangent=err,beta=beta,relative_beta_error=abs(beta-BETA_STAR)/BETA_STAR,
                         maximum_axial_strain=max_strain,maximum_port_ripple=max_port_ripple,
                         normalized_power_balance_residual=balance))
        assert abs(beta-BETA_STAR)<3e-4 and balance<2e-8
    assert rows[1]['operator_error_against_tangent']<rows[0]['operator_error_against_tangent']/10
    return {'force_cases':8,'interpretation':'Nonlinear finite-length realizations; theorem applies to their tangent limit.', 'rows':rows}


def positivity_control():
    """Cooperative scalar-node spring networks: off-diagonal compliance nonnegative."""
    Ks=[]
    for edge,grounds in [((0,1),[1,2,1,2]),((1,2),[2,1,2,1]),((2,3),[1.5,1,1.5,1])]:
        k=np.diag(np.array(grounds,float));v=np.zeros(4);v[edge[0]]=1;v[edge[1]]=-1
        k+=.8*np.outer(v,v)
        # Connect the remaining nodes weakly in a chain.
        for j in range(3):
            w=np.zeros(4);w[j]=1;w[j+1]=-1;k+=.15*np.outer(w,w)
        Ks.append(k)
    # Exact affine stage map including integrated response, all forces basis at once.
    n=4;aug=np.zeros((3*n,3*n)); duration=.8
    propagators=[]
    for k in Ks:
        aug[:n,:n]=-k;aug[:n,n:2*n]=np.eye(n);aug[2*n:,:n]=np.eye(n)
        propagators.append(expm(aug*duration))
    cycle=np.eye(3*n)
    for e in propagators:cycle=e@cycle
    x0=np.linalg.solve(np.eye(n)-cycle[:n,:n],cycle[:n,n:2*n])
    init=np.vstack((x0,np.eye(n),np.zeros((n,n))))
    chi=(cycle@init)[2*n:]/(duration*len(Ks))
    assert chi.min()>0
    assert CHI_STAR[0,1]<0 and CHI_STAR[1,0]>0
    return dict(node_compliance=chi.tolist(),minimum_entry=float(chi.min()),
                optimized_two_port_cross_product=float(CHI_STAR[0,1]*CHI_STAR[1,0]),
                limitation='The analytic positivity exclusion assumes parallel scalar node coordinates and diagonal drag, not arbitrary geometry or hydrodynamic coupling.')


def sharpness_and_three_coordinate_control():
    hstar=math.sqrt(3);jstar=(4-hstar)/3
    f=np.array([1,1j,0,0])/math.sqrt(2)
    z=2/3-1j*BETA_STAR
    lam=(z-1/hstar)/(jstar-1/hstar)
    portchi=CHI_STAR
    max_equality=0.;max_portconst=0.
    for t in np.linspace(0,PERIOD,31):
        R=rotation(OMEGA*t)
        xp=portchi@f[:2]
        w=-B*np.linalg.solve(G*I2-OMEGA*J,xp)
        state=np.r_[xp,R.T@w]
        reference=f/hstar+lam*(np.linalg.solve(stiffness(t),f)-f/hstar)
        max_equality=max(max_equality,float(np.linalg.norm(state-reference)))
        max_portconst=max(max_portconst,float(np.linalg.norm(stiffness(t)[:2,:2]-hstar*I2)))
    rank_matrix=I2-hstar*portchi
    singular=np.linalg.svd(rank_matrix,compute_uv=False)
    assert max_equality<1e-12 and min(singular)>0
    # A three-coordinate device with constant ports and nonzero nonreciprocity,
    # below the universal ceiling. This defeats an overbroad 'four needed for any effect' claim.
    r=.25;g=1.;h=2.;omega=1.;kodd=r*r*omega/2
    G3=h*I2-kodd*J;chi3=np.linalg.inv(G3)
    min_eig=math.inf;max_eig=0.;max_resid=0.
    for t in np.linspace(0,2*math.pi,31):
        y=r*np.array([np.cos(t),np.sin(t)])
        dy=r*np.array([-np.sin(t),np.cos(t)])
        coupling=-(g*y+dy)
        pp=h*I2+g*np.outer(y,y)+(np.outer(dy,y)+np.outer(y,dy))/2
        K=np.block([[pp,coupling[:,None]],[coupling[None,:],np.array([[g]])]])
        eig=np.linalg.eigvalsh(K);min_eig=min(min_eig,float(eig[0]));max_eig=max(max_eig,float(eig[-1]))
        for force in [np.array([1.,0.]),np.array([0.,1.])]:
            x=chi3@force;full=np.r_[x,y@x];velocity=np.r_[np.zeros(2),dy@x]
            max_resid=max(max_resid,float(np.linalg.norm(velocity+K@full-np.r_[force,0.])))
    ceiling=.5*(1/np.sqrt(min_eig)-1/np.sqrt(max_eig))**2
    beta3=float((chi3[1,0]-chi3[0,1])/2)
    assert min_eig>0 and max_resid<2e-12 and 0<beta3<ceiling
    return dict(equality_times=31,equality_residual=max_equality,port_block_residual=max_portconst,
                rank_obstruction_singular_values=singular.tolist(),three_coordinate_stiffness_interval=[min_eig,max_eig],
                three_coordinate_beta=beta3,three_coordinate_ceiling=ceiling,three_coordinate_residual=max_resid,
                scope='Four is minimal for exact global-ceiling attainment with stationary measured ports and block-diagonal port/internal drag; not for all nonreciprocal devices.')


def tolerance_checks():
    eps=.01
    # Every positive spring receives its own fixed relative calibration error.
    gains=np.array([.7,-.3,.9,-.5,.1,-.8,.4,-1.,.2,.7,-.4,.1])*eps
    def perturbed(t):
        K=np.diag(GROUNDS*(1+gains[:4]))
        for gain,item in zip(gains[4:],elements(t)):
            *_,k,kd,v=item
            K+=(1+gain)*k*np.outer(v,v)
        return K
    cs=[]
    for j in range(2):
        _,_,avg=steady_integrate(lambda t,x:P[:,j]-perturbed(t)@x,4,PERIOD)
        cs.append(avg[:2])
    chi=np.column_stack(cs)
    actual=float(np.linalg.norm(chi-CHI_STAR,2))
    bound=eps*MHIGH/(MLOW*MLOW*(1-eps))
    beta=float((chi[1,0]-chi[0,1])/2)
    assert actual<bound and beta>=BETA_STAR-bound
    return dict(relative_spring_error_bound=eps,measured_test_compliance=chi.tolist(),actual_operator_error=actual,
                universal_error_bound=bound,certified_beta_floor=BETA_STAR-bound,realized_test_beta=beta,
                actual_allowed_stiffness_interval=[(1-eps)*MLOW,(1+eps)*MHIGH],
                scope='Same constant drag and homogeneous linear springs; not a bound on guide friction, controller energy, or arbitrary nonlinear excursions.')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=Path(__file__).with_name('results.json'))
    args=ap.parse_args()
    groups={}
    for name,fun in [('positive_fixed_geometry',synthesis_checks),('finite_axial_geometry',geometry_checks),
                     ('parallel_slider_exclusion',positivity_control),('stationary_optimum_dimension',sharpness_and_three_coordinate_control),
                     ('calibration_bound',tolerance_checks)]:
        groups[name]=fun();print(name,'PASS',flush=True)
    report={'date':'2026-09-29','status':'PASS','environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'diagnostic_groups':groups,'limits':['Analytic claims require the accompanying proofs.','No experimental hardware was tested.','No independent scientific audit or priority certificate.']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('Saved',args.output)

if __name__=='__main__':main()
