import unittest
from fractions import Fraction as F
import geometry as g

class InitialTests(unittest.TestCase):
    def test_volume_parts(self):
        self.assertEqual(g.shape_integrals(), (F(231744,35), F(2112,5)))
    def test_total_volume(self):
        self.assertEqual(sum(g.shape_integrals()), F(246528,35))
    def test_tail_factor(self):
        self.assertEqual(g.radial_factor(1), F(53250048,385))
    def test_k_scaling(self):
        self.assertEqual(g.radial_factor(2), 128*g.radial_factor(1))
    def test_height_mass(self):
        self.assertEqual(g.height_moment(0), F(246528,35))
    def test_height_mean(self):
        self.assertEqual(g.height_moment(1)/g.height_moment(0), F(5771,7062))
    def test_height_second(self):
        self.assertEqual(g.height_moment(2)/g.height_moment(0), F(2440,3531))
    def test_point_map(self):
        # k=1,u=-1,z=2,v=6 => s=-3/2,B=-9/4,D=-3/8.
        self.assertEqual(g.point_map(1,-1,6,2,0), (F(-3,2),F(0),F(-9,4),F(-3,4)))
    def test_cusp_curve(self):
        self.assertEqual(g.raw_jet(1,6,0,0), (F(3),F(3,2)))
    def test_exponent(self):
        self.assertEqual(g.tail_power(),11)


class AdditionalTests(unittest.TestCase):
    def test_sparse_algebra(self):
        p={(1,0):F(1),(0,0):F(1)}
        self.assertEqual(g.power(p,2),{(2,0):F(1),(1,0):F(2),(0,0):F(1)})
        self.assertEqual(g.add(p,g.scale(p,-1)),{})
    def test_exact_rectangular_integral(self):
        self.assertEqual(g.integrate_strip({(2,1):F(1)},{},{(0,0):F(2)},0,3),18)
    def test_constant_integral(self):
        self.assertEqual(g.integrate_strip({(0,0):F(1)},{},{(0,0):F(1)},0,1),1)
    def test_empty_polynomial(self):
        self.assertEqual(g.integrate_strip({}, {}, {(0,0):F(1)},0,1),0)
    def test_bad_order(self):
        with self.assertRaises(ValueError): g.height_moment(-1)
    def test_float_rejected(self):
        with self.assertRaises(ValueError): g.radial_factor(1.0)
    def test_bool_rejected(self):
        with self.assertRaises(ValueError): g.radial_factor(True)
    def test_zero_k_rejected(self):
        with self.assertRaises(ValueError): g.radial_factor(0)
    def test_zero_z_rejected(self):
        with self.assertRaises(ValueError): g.point_map(1,0,1,0,0)
    def test_invalid_strip(self):
        with self.assertRaises(ValueError): g.integrate_strip({}, {}, {(0,1):F(1)},0,1)
    def test_height_moments_independent(self):
        for q in range(8):
            self.assertEqual(sum(g.shape_integrals(q)),g.height_moment(q))
    def test_height_variance_positive(self):
        mass=g.height_moment(0)
        self.assertGreater(g.height_moment(2)/mass-(g.height_moment(1)/mass)**2,0)
    def test_root_jacobian_independent(self):
        def det(a):
            return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
                    -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
                    +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
        for k in (F(1,2),F(1),F(3)):
            for u in (F(-5,4),F(-3,4),F(-1,4),F(1,4)):
                b=3-12*u*u; bp=-24*u
                v=(abs(b)/2+3-6*u)/2
                for z in (F(-3),F(1),F(4)):
                    rows=[[k/z**2,0,-2*k*v/z**3],
                          [0,k*bp/z**2,-2*k*b/z**3],
                          [k/z**3,-k*(bp*u+b)/z**3,-3*k*(v-b*u)/z**4]]
                    self.assertEqual(det(rows),g.root_jacobian(k,u,v,z))
    def test_raw_inverse(self):
        for k in (F(1,2),F(1),F(3)):
            for a in (F(-3),F(0),F(4)):
                for B,D in ((F(-2),F(1,3)),(F(1),F(-1))):
                    beta,c=g.raw_jet(k,a,B,D)
                    self.assertEqual(beta-a*a/(12*k),B)
                    self.assertEqual((c-a*beta/(4*k)+a**3/(72*k*k))/2,D)
    def test_root_homogeneity(self):
        k,u,v,z,a=F(1),F(-3,4),F(3),F(2),F(3)
        s,a,beta,c=g.point_map(k,u,v,z,a)
        B=beta-a*a/(12*k); D=(c-a*beta/(4*k)+a**3/(72*k*k))/2
        for t in (F(2),F(5),F(10)):
            st,at,betat,ct=g.point_map(k,u,v,t*z,a)
            self.assertEqual(st,s/t**2)
            self.assertEqual(betat-a*a/(12*k),B/t**2)
            self.assertEqual((ct-a*betat/(4*k)+a**3/(72*k*k))/2,D/t**3)
    def test_factorial_localization_inequality(self):
        def falling(n,q):
            out=1
            for j in range(q):out*=max(n-j,0)
            return out
        for near in range(5):
            for mid in range(5):
                for far in range(5):
                    n=near+mid+far
                    bad=bool(mid or (near and far) or far>=2 or near>=3)
                    for q in range(2,6):
                        loss=falling(n,q)-falling(near,q)
                        self.assertGreaterEqual(loss,0)
                        self.assertLessEqual(loss,n**q*bad)
    def test_moment_uniform_integrability_bound(self):
        for q in range(5):
            for M in range(1,10):
                for n in range(M+1,30):
                    self.assertLessEqual(F(n**q),F(n**(q+1),M))
    def test_counting_grid(self):
        self.assertEqual(g.run_checks()['stationary_map_cases'],648)
    def test_cli_modes_and_mutants(self):
        import subprocess,sys
        from pathlib import Path
        script=str(Path(g.__file__).resolve())
        reference=None
        for flags in (['-B','-S'],['-B','-O','-S']):
            out=subprocess.run([sys.executable,*flags,script],capture_output=True,timeout=30)
            self.assertEqual(out.returncode,0,out.stderr)
            if reference is None: reference=out.stdout
            self.assertEqual(out.stdout,reference)
            for name in g.MUTANTS:
                bad=subprocess.run([sys.executable,*flags,script,'--mutant',name],capture_output=True,timeout=30)
                self.assertEqual(bad.returncode,1,(name,bad.stdout,bad.stderr))
            bad=subprocess.run([sys.executable,*flags,script,'--mutant','unknown'],capture_output=True,timeout=30)
            self.assertEqual(bad.returncode,2)

if __name__=='__main__': unittest.main()
