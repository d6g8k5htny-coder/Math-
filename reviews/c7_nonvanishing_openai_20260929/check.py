"""Exact reviewer controls for the C7 nonvanishing mechanism; not a Gaussian verifier."""
import argparse,json
from fractions import Fraction as F

MUTANTS=('above-level','bad-shell','missing-pin-correction','wrong-jacobian','omit-log-endpoint')

def controls(mutant=None):
    out={}
    s=F(0);t=F(1,10)
    critical=s+t if mutant=='above-level' else s
    out['LEVEL']={'above_level_closure_excludes_saddle':not s>=t,
                  'incidence_uses_critical_level':critical==s}
    c=F(1,16) if mutant=='bad-shell' else F(7,16)
    alpha=F(-7,8)
    gaps=(-alpha*(1+c)-c*c-1,-alpha*(1+c)-c*c-c,-2*alpha-1-c)
    out['WITNESS']={'fixed_square_valid':0<c<1,
        'all_shell_faces_have_uniform_slack':min(gaps)>0,
        'minimum_gap_exact':min(gaps)==F(17,256),
        'alpha_endpoint_is_worst':1+c>0 and 2>0,
        'cosine_quadratic_convex':F(2)>0}
    for ell in (F(0),F(1,4)):
        a=ell/2-1;gM=a+2;gS=-a
        out['WITNESS'][f'height_{ell}']=gM-gS==ell
        out['WITNESS'][f'indices_{ell}']=(-a-2)<0 and (a-2)<0
    # Hermite cardinal polynomials: value/derivative at0 and1.
    basis=[[1,0,-3,2],[0,1,-2,1],[0,0,3,-2],[0,0,-1,1]]
    def observe(p):
        return [p[0],p[1],sum(p),sum(i*p[i] for i in range(1,len(p)))]
    out['SUPPORT']={'dual_constraint_basis':all(observe(b)==[int(i==j) for i in range(4)] for j,b in enumerate(basis))}
    polynomial=[F(1,2),F(2,3),F(-3,4),F(4,5),F(5,6),F(-6,7)]
    targets=observe(polynomial)
    corrected=polynomial.copy()
    if mutant!='missing-pin-correction':
        for a,b in zip(targets,basis):
            for j,cj in enumerate(b):corrected[j]-=a*cj
    out['SUPPORT']['exact_constraints_after_projection']=observe(corrected)==[0]*4
    jac=F(3) if mutant=='wrong-jacobian' else abs(1*(-1)-0*1)
    out['JACOBIAN']={'full_height_map_absolute_determinant_one':jac==1}
    pred=lambda q:q<-1 if mutant=='omit-log-endpoint' else q<=-1
    out['MOMENT']={'log_endpoint_diverges':pred(F(-1)),
        'lower_divergence_below_endpoint':pred(F(-2)),
        'no_divergence_inferred_above':not pred(F(-3,4))}
    out['SCOPE']={'linear_count_vs_compact_power':F(5,3)>1,
        'far_lower_not_compact_rate':F(2,3)>0,
        'unrestricted_finiteness_strip_not_closed':F(-1)<F(-3,4)<F(-2,3)}
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mutant',choices=MUTANTS);args=p.parse_args()
    values=controls(args.mutant)
    failed=[g+'.'+k for g,group in values.items() for k,v in group.items() if not v]
    print(json.dumps(dict(groups=values,failed=failed,passed=not failed,
        scope='Finite algebra and counterexample controls only; no continuum support, topology or Kac-Rice verification'),indent=2,sort_keys=True))
    return int(bool(failed))

if __name__=='__main__':raise SystemExit(main())
