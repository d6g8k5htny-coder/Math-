"""Boundary-ray controls only; no grid simulation or Gaussian claim."""
import unittest
import elder_grid as G


class OutwardRayTests(unittest.TestCase):
    def test_three_increasing_samples_do_not_establish_connection(self):
        # P(tu,tZ) = .2 t^3 - .25 t^2 - .15 t - .5.
        # P'(1) = -.05, although P(1),P(1.5),P(2),P(3) increase.
        args = (1.0, -1/18, 0.0, 0.022, 0.1, 3.0)
        k, s, B, D, u, z = args
        vals = [G.P(k,s,B,D,t*u,t*z) for t in (1,1.5,2,3)]
        self.assertTrue(-k < vals[0] < vals[1] < vals[2] < vals[3])
        self.assertGreater(vals[-1], 0)
        self.assertFalse(G.outward_ray_older(*args))

    def test_monotone_ray_to_positive_value_is_accepted(self):
        self.assertTrue(G.outward_ray_older(1.0, -1.0, 0.0, 0.0, 1.0, 0.0))

    def test_decreasing_ray_is_rejected(self):
        self.assertFalse(G.outward_ray_older(1.0, -1.0, 0.0, 0.0, -1.0, 0.0))

    def test_interior_derivative_minimum_is_checked(self):
        # Derivative .9*t^2 - 3.6*t + 3 is positive at 1 and 3,
        # but negative at 2. The endpoint P(3) is positive.
        self.assertFalse(G.outward_ray_older(1.0, -3.6, 0.0, 48.9, -2.0, 1.0))

    def test_increasing_ray_must_reach_positive_value(self):
        self.assertFalse(G.outward_ray_older(1.0, -0.0001, 0.0, 0.03, 0.0, 1.0))


if __name__ == '__main__':
    unittest.main()
