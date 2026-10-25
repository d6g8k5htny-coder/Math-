"""Falsification checks against the hash-pinned, unmodified #297 implementation.
The source replay is high-precision diagnostic arithmetic, not interval evidence.
The certificate's error bounds do not come from these comparisons.
"""
import argparse
import decimal
import hashlib
import importlib.util
import json
import math
import pathlib
import certificate as c

EXPECTED='59b53e5c2e8fdcacc9983f705b9d301fcfcf9242ac6c4d8b7bfbcf0ada7caf9f'


def disk_diagnostic(B,n=160):
    """Independent 2D disk integral with floating midpoint arithmetic; NOT a bound."""
    b=[[float(x.mid()) for x in row] for row in B]
    _,det=c.inverse3(B)
    total=0.0
    trig=[(math.cos(2*math.pi*(j+.5)/n),math.sin(2*math.pi*(j+.5)/n)) for j in range(n)]
    for i in range(n):
        r=(i+.5)/n
        for co,si in trig:
            v=[-1.0,r*co,r*si]
            q=sum(v[a]*b[a][d]*v[d] for a in range(3) for d in range(3))
            total+=r*(1-r*r)**2*q**(-3.5)
    return 15/(4*math.pi)*math.sqrt(float(det.mid()))*total*(2*math.pi/n)/n


def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--source',required=True)
    args=ap.parse_args(); path=pathlib.Path(args.source)
    c.need(hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED,'upstream source SHA256 mismatch')
    spec=importlib.util.spec_from_file_location('pinned_297',path)
    s=importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
    D=decimal.Decimal; I=c.I; p=c.parameters()
    # Uniform envelopes make 1e9*tail a conservative image allowance for these point quantities.
    Dmax=(p['c0']*p['c1']**2/(p['Bmin']*p['Bsmin']**2)).sqrt()*c.diagonal_cone(1/p['Bmin'],1/p['Bsmin'])
    c.need(Dmax.hi<10 and p['Tmax'].hi<10 and p['Rmax'].hi<10,'point image envelope failed')
    with decimal.localcontext() as ctx:
        ctx.prec=270
        q2,q4,q6,tail=s.q_derivatives(D(4)); a=-q2
        kk={2:a,4:q4-3*a*a,6:-q6-15*q4*a+30*a**3}
        for tag,x in [('a',a),('m4',q4),('m6',-q6)]:
            c.need(p[tag].lo<=x<=p[tag].hi,'moment does not contain upstream '+tag)
        rows=[]
        for label,raw in [('axis',(1,0,0)),('face',(1,1,0)),('body',(1,1,1)),
                          ('generic123',(1,2,3)),('generic257',(2,5,7))]:
            X,Y,Z=map(D,raw); rn=(X*X+Y*Y+Z*Z).sqrt(); xy=(X*X+Y*Y).sqrt()
            st,ct,sp,cp=xy/rn,Z/rn,Y/xy,X/xy
            u=[st*cp,st*sp,ct]; w=[ct*cp,ct*sp,-st]; v=[-sp,cp,D(0)]
            jd=s.jet_data(u,kk,[w,v]); S=jd['S_AgV']
            conv=[[D(1)/2,0,D(1)/2],[D(1)/2,0,-D(1)/2],[0,1,0]]
            sourceC=[[sum(conv[i][a]*S[a][b]*conv[j][b] for a in range(3) for b in range(3)) for j in range(3)] for i in range(3)]
            # Enclose the exact algebraic trig components, not rounded binary input.
            rnI=(I(int(X))**2+I(int(Y))**2+I(int(Z))**2).sqrt()
            xyI=(I(int(X))**2+I(int(Y))**2).sqrt()
            value,err,meta=c.direction_trig(xyI/rnI,I(int(Z))/rnI,I(int(Y))/xyI,I(int(X))/xyI,p)
            for i in range(3):
                for j in range(3):
                    z=meta['C'][i][j]
                    c.need(z.lo<=sourceC[i][j]<=z.hi,'Schur/precision mismatch '+label)
            c.need(meta['tau2'].lo<=jd['tau2']<=meta['tau2'].hi,'tau mismatch '+label)
            detV=p['detH']*meta['detB']/4
            c.need(detV.lo<=jd['det_V']<=detV.hi,'density determinant mismatch '+label)
            C=meta['C']; trA=2*(C[0][0]+C[1][1]+C[2][2])
            c.need(trA.lo<=jd['tr_AgV']<=trA.hi,'Frobenius trace mismatch '+label)
            # Exact rational transverse-frame rotation by cos=3/5,sin=4/5.
            R=[[I(1),I(0),I(0)],[I(0),-I(7)/25,I(24)/25],[I(0),-I(24)/25,-I(7)/25]]
            B=meta['precision']
            turned=[[sum(R[i][a]*B[a][b]*R[j][b] for a in range(3) for b in range(3)) for j in range(3)] for i in range(3)]
            td,te,_=c.cone(turned); d=meta['D'].widen(meta['cone_error_D']); td=td.widen(te)
            c.need(d.lo<=td.hi and td.lo<=d.hi,'cone transverse rotation mismatch')
            direct=disk_diagnostic(B)
            c.need(abs(direct-float(d.mid()))<2e-4,'independent disk falsification failed')
            rows.append(dict(direction=raw,D_interval=d.widen(10**9*p['tail']).pair(),
                             tau2_interval=meta['tau2'].widen(10**9*p['tail']).pair(),
                             ratio_direction_interval=value.widen(err).widen(10**9*p['tail']).pair(),
                             upstream_Schur_contained=True,frame_rotation_overlap=True,
                             independent_disk_midpoint_diagnostic=direct,
                             disk_diagnostic_is_certificate=False))
    # Independent high-precision evaluation of the already-known nonperiodic closed form.
    # This is a falsification check on normalization, not a replacement for the imported enclosure.
    with decimal.localcontext() as ctx:
        ctx.prec=270
        D0=D(29)/6-D(6).sqrt()
        cref=s.stirling_gamma(D(7)/6)*(D(3)/2)**(D(1)/3)*D0/(2*D(3).sqrt()*s.PI**2*s.PI.sqrt())
        inside=D('0.04177593184059834334')<cref<D('0.04177593184059834335')
        c.need(inside,'nonperiodic coefficient falsification failed')
        unconditioned_or_untruncated_half=D(29)/6
        refcheck=dict(nonperiodic_cone_closed_form=str(D0),
                      nonperiodic_coefficient_diagnostic=str(cref),
                      inside_imported_side24_interval=inside,
                      gamma_diagnostic_is_certificate=False,
                      half_untruncated_moment_rejected=str(unconditioned_or_untruncated_half))
    print(json.dumps(dict(source_sha256=EXPECTED,rows=rows,reference_checks=refcheck),indent=2,sort_keys=True))

if __name__=='__main__': main()
