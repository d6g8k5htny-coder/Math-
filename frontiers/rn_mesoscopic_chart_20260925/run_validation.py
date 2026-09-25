"""Replay mesoscopic-chart controls in both Python modes; preserve mutation logs."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EXPECTED_TESTS = 65
MUTANTS = {
    'wrong_grad_x_power': (
        "'grad_x': 2,\n    'grad_y': 1,",
        "'grad_x': 1,\n    'grad_y': 1,",
    ),
    'wrong_grad_y_power': (
        "'grad_y': 1,\n    'height': 2,\n}",
        "'grad_y': 2,\n    'height': 2,\n}",
    ),
    'wrong_axial_grad_y_power': (
        "'grad_y': 2,\n    'height': 3,",
        "'grad_y': 1,\n    'height': 3,",
    ),
    'drop_height_dependence': (
        "return exact(y[1]) / 2",
        "return exact(0)",
    ),
    'omit_k_term': (
        "j_x = 6 * k * y1 * y1 + b * y1 * y2 + (c * y2 * y2) / 2",
        "j_x = b * y1 * y2 + (c * y2 * y2) / 2",
    ),
    'omit_next_height_k': (
        "h1 = (\n        2 * k * y1 ** 3\n        + (b * y1 * y1 * y2) / 2",
        "h1 = (\n        0 * k * y1 ** 3\n        + (b * y1 * y1 * y2) / 2",
    ),
    'claim_annulus_closed': (
        "'height_next_order_enumerated': True,\n        'hessian_contact_rows_enumerated': True,\n        'hessian_ledger_evaluated': False,\n        'full_annulus_closed': False,",
        "'height_next_order_enumerated': True,\n        'hessian_contact_rows_enumerated': True,\n        'hessian_ledger_evaluated': False,\n        'full_annulus_closed': True,",
    ),
    'claim_cover_complete': (
        "'cover_complete': False,",
        "'cover_complete': True,",
    ),
    'wrong_pins_exterior': (
        "return exact(inner) > Q(1, 2)",
        "return exact(inner) < Q(1, 2)",
    ),
    'wrong_hessian_xx_power': (
        "'xx': 1,\n    'xy': 1,\n    'yy': 0,",
        "'xx': 0,\n    'xy': 1,\n    'yy': 0,",
    ),
    'claim_hessian_conditioned': (
        "'hessian_contact_rows_enumerated': True,\n        'hessian_ledger_evaluated': False,\n        'conditioned_expectation_evaluated': False,",
        "'hessian_contact_rows_enumerated': True,\n        'hessian_ledger_evaluated': True,\n        'conditioned_expectation_evaluated': True,",
    ),
    'claim_density_bound': (
        "'contact_density_bound_proved': False,",
        "'contact_density_bound_proved': True,",
    ),
    'wrong_integrand_net': (
        "net = spatial - grad + hess + height  # midpoint charts",
        "net = spatial - grad + height  # midpoint charts",
    ),
    'claim_thin_belt_absorbed': (
        "'uniform_integrand_bound_proved': False,\n        'absorbed_into_C_transverse': False,",
        "'uniform_integrand_bound_proved': True,\n        'absorbed_into_C_transverse': True,",
    ),
    'claim_pin_rows_enumerated': (
        "'pin_site_jet_rows_enumerated': True,\n        'pin_site_next_order_enumerated': True,\n        'pin_site_quartic_enumerated': True,\n        'pin_site_quintic_enumerated': True,\n        'pin_site_sextic_enumerated': True,\n        'pin_site_septic_enumerated': True,\n        'pin_site_octic_enumerated': True,\n        'pin_site_nonic_enumerated': True,\n        'pin_site_decic_enumerated': True,\n        'pin_site_undecic_enumerated': True,\n        'pin_site_dodecic_enumerated': True,\n        'pin_site_higher_jets_enumerated': False,",
        "'pin_site_jet_rows_enumerated': True,\n        'pin_site_next_order_enumerated': True,\n        'pin_site_quartic_enumerated': True,\n        'pin_site_quintic_enumerated': True,\n        'pin_site_sextic_enumerated': True,\n        'pin_site_septic_enumerated': True,\n        'pin_site_octic_enumerated': True,\n        'pin_site_nonic_enumerated': True,\n        'pin_site_decic_enumerated': True,\n        'pin_site_undecic_enumerated': True,\n        'pin_site_dodecic_enumerated': True,\n        'pin_site_higher_jets_enumerated': True,",
    ),
    'claim_pin_obstruction_cleared': (
        "'raw_gradient_collides_with_pin_gradient_constraints': True,\n        'near_pin_intersects_axial_thin_belt_locus': True,\n        'leading_morse_rows_enumerated_elsewhere': True,\n        'pin_site_higher_jets_enumerated': False,",
        "'raw_gradient_collides_with_pin_gradient_constraints': False,\n        'near_pin_intersects_axial_thin_belt_locus': False,\n        'leading_morse_rows_enumerated_elsewhere': True,\n        'pin_site_higher_jets_enumerated': True,",
    ),
    'wrong_pin_grad_power': (
        "PIN_CENTERED_SCALING_EXPONENTS = {\n    'grad': 1,\n    'height': 2,\n}",
        "PIN_CENTERED_SCALING_EXPONENTS = {\n    'grad': 2,\n    'height': 2,\n}",
    ),
    'claim_thin_belt_L1': (
        "'bare_conditioning_factor_L1_near_zero': False,",
        "'bare_conditioning_factor_L1_near_zero': True,",
    ),
    'claim_singular_boundary': (
        "'transition_jacobian_determinant': Q(1),\n        'singular_transition': False,",
        "'transition_jacobian_determinant': Q(0),\n        'singular_transition': True,",
    ),
    'claim_density_from_jet_map': (
        "'cancels_bare_reciprocal_pointwise': True,\n        'full_density_bound_proved': False,",
        "'cancels_bare_reciprocal_pointwise': True,\n        'full_density_bound_proved': True,",
    ),
    'claim_density_from_chart_bound': (
        "'chart_conditioning_singularity_cleared': True,\n        'gaussian_density_factor_bounded': False,",
        "'chart_conditioning_singularity_cleared': True,\n        'gaussian_density_factor_bounded': True,",
    ),
    'claim_density_from_axial_bound': (
        "'axial_chart_conditioning_singularity_cleared': True,\n        'axial_gaussian_density_factor_bounded': False,",
        "'axial_chart_conditioning_singularity_cleared': True,\n        'axial_gaussian_density_factor_bounded': True,",
    ),
    'claim_height_r_absorbed': (
        "'unmatched_height_density_r_power': 1,\n        'explicit_r_factor_still_required': True,\n        'height_r_absorbed_into_uniform_bound': False,\n        'meaning': (\n            'leading height is (y2/2)J_grad_y; independence needs H_height_next '\n            'and inserts unmatched r^1; not absorbed into a uniform density bound'\n        ),",
        "'unmatched_height_density_r_power': 1,\n        'explicit_r_factor_still_required': False,\n        'height_r_absorbed_into_uniform_bound': True,\n        'meaning': (\n            'leading height is (y2/2)J_grad_y; independence needs H_height_next '\n            'and inserts unmatched r^1; not absorbed into a uniform density bound'\n        ),",
    ),
    'claim_thin_belt_height_r_absorbed': (
        "'unmatched_height_density_r_power': 1,\n        'explicit_r_factor_still_required': True,\n        'height_r_absorbed_into_uniform_bound': False,\n        'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,\n        'contact_gaussian_density_bounded': False,\n        'meaning': (\n            'thin-belt shares transverse height–grad_y dependence; unmatched r^1 '\n            'not absorbed; Gaussian density near y2=0 still unbound'\n        ),",
        "'unmatched_height_density_r_power': 1,\n        'explicit_r_factor_still_required': False,\n        'height_r_absorbed_into_uniform_bound': True,\n        'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,\n        'contact_gaussian_density_bounded': True,\n        'meaning': (\n            'thin-belt shares transverse height–grad_y dependence; unmatched r^1 '\n            'not absorbed; Gaussian density near y2=0 still unbound'\n        ),",
    ),
    'claim_density_from_axial_height_independence': (
        "'no_unmatched_height_r_at_leading_order': True,\n        'axial_area_measure_zero': True,\n        'contact_gaussian_density_bounded': False,\n        'meaning': (\n            'axial J_height=2k y1^3 is independent at leading order; '\n            'no unmatched height r^1 (unlike C_transverse); density still unbound'\n        ),",
        "'no_unmatched_height_r_at_leading_order': True,\n        'axial_area_measure_zero': True,\n        'contact_gaussian_density_bounded': True,\n        'meaning': (\n            'axial J_height=2k y1^3 is independent at leading order; '\n            'no unmatched height r^1 (unlike C_transverse); density still unbound'\n        ),",
    ),
    'claim_density_from_axial_shared_mark': (
        "'shared_mark_forces_unmatched_height_r': False,\n        'unmatched_height_density_r_power': 0,\n        'explicit_r_factor_still_required': False,\n        'no_unmatched_height_r_at_leading_order': True,\n        'axial_area_measure_zero': True,\n        'contact_gaussian_density_bounded': False,\n        'meaning': (\n            'exact J_height=(y1/3)J_grad_x via shared gap mark k; '\n            'distinct scalings keep unmatched height r at 0; density still unbound'\n        ),",
        "'shared_mark_forces_unmatched_height_r': True,\n        'unmatched_height_density_r_power': 0,\n        'explicit_r_factor_still_required': False,\n        'no_unmatched_height_r_at_leading_order': True,\n        'axial_area_measure_zero': True,\n        'contact_gaussian_density_bounded': True,\n        'meaning': (\n            'exact J_height=(y1/3)J_grad_x via shared gap mark k; '\n            'distinct scalings keep unmatched height r at 0; density still unbound'\n        ),",
    ),
    'claim_pin_signature_always_matches': (
        "'signature_matches_pin_role': matches,\n        'morse_nondegenerate': det != 0,",
        "'signature_matches_pin_role': True,\n        'morse_nondegenerate': det != 0,",
    ),
    'wrong_pin_hess_det_power': (
        'PIN_CENTERED_HESSIAN_DET_R_POWER = 0',
        'PIN_CENTERED_HESSIAN_DET_R_POWER = 1',
    ),
    'drop_pin_cubic_identity': (
        "'z_dot_H_grad_next_minus_3_H_height_next': u * g1 + v * g2 - 3 * h,",
        "'z_dot_H_grad_next_minus_3_H_height_next': u * g1 + v * g2 - 2 * h,",
    ),
    'drop_pin_quartic_identity': (
        "'z_dot_Q_grad_next_minus_4_Q_height_next': u * g1 + v * g2 - 4 * h,",
        "'z_dot_Q_grad_next_minus_4_Q_height_next': u * g1 + v * g2 - 3 * h,",
    ),
    'drop_pin_quintic_identity': (
        "'z_dot_P_grad_next_minus_5_P_height_next': u * g1 + v * g2 - 5 * h,",
        "'z_dot_P_grad_next_minus_5_P_height_next': u * g1 + v * g2 - 4 * h,",
    ),
    'drop_pin_sextic_identity': (
        "'z_dot_S_grad_next_minus_6_S_height_next': u * g1 + v * g2 - 6 * h,",
        "'z_dot_S_grad_next_minus_6_S_height_next': u * g1 + v * g2 - 5 * h,",
    ),
    'drop_pin_septic_identity': (
        "'z_dot_T_grad_next_minus_7_T_height_next': u * g1 + v * g2 - 7 * ht,",
        "'z_dot_T_grad_next_minus_7_T_height_next': u * g1 + v * g2 - 6 * ht,",
    ),
    'drop_pin_octic_identity': (
        "'z_dot_U_grad_next_minus_8_U_height_next': u * g1 + v * g2 - 8 * ht,",
        "'z_dot_U_grad_next_minus_8_U_height_next': u * g1 + v * g2 - 7 * ht,",
    ),
    'drop_pin_nonic_identity': (
        "'z_dot_N_grad_next_minus_9_N_height_next': u * g1 + v * g2 - 9 * ht,",
        "'z_dot_N_grad_next_minus_9_N_height_next': u * g1 + v * g2 - 8 * ht,",
    ),
    'drop_pin_decic_identity': (
        "'z_dot_D_grad_next_minus_10_D_height_next': u * g1 + v * g2 - 10 * ht,",
        "'z_dot_D_grad_next_minus_10_D_height_next': u * g1 + v * g2 - 9 * ht,",
    ),
    'drop_pin_undecic_identity': (
        "'z_dot_E_grad_next_minus_11_E_height_next': u * g1 + v * g2 - 11 * ht,",
        "'z_dot_E_grad_next_minus_11_E_height_next': u * g1 + v * g2 - 10 * ht,",
    ),
    'drop_pin_dodecic_identity': (
        "'z_dot_F_grad_next_minus_12_F_height_next': u * g1 + v * g2 - 12 * ht,",
        "'z_dot_F_grad_next_minus_12_F_height_next': u * g1 + v * g2 - 11 * ht,",
    ),
    'claim_global_density_from_inventory': (
        "'target': 'gamma_AB_le_C_r_to_minus_d',\n        'global_contact_density_bound_proved': False,",
        "'target': 'gamma_AB_le_C_r_to_minus_d',\n        'global_contact_density_bound_proved': True,",
    ),
    'claim_density_from_free_jet_residual': (
        "'global_contact_density_bound_proved': False,\n        'meaning': (\n            'exact free-jet residual counts after leading gradient contact; '\n            'prerequisite inventory only — does not bound the contact density'\n        ),",
        "'global_contact_density_bound_proved': True,\n        'meaning': (\n            'exact free-jet residual counts after leading gradient contact; '\n            'prerequisite inventory only — does not bound the contact density'\n        ),",
    ),
    'claim_hessian_expectation_from_residual': (
        "'conditioned_hessian_residual_polynomials_enumerated': True,\n        'conditioned_expectation_evaluated': False,\n        'contact_gaussian_density_bounded': False,\n        'hessian_ledger_evaluated': False,\n        'meaning': (\n            'exact residual Hessian polynomials after eliminating f_yy,f_xyy; '\n            'not a conditioned Gaussian expectation of |det H|'\n        ),",
        "'conditioned_hessian_residual_polynomials_enumerated': True,\n        'conditioned_expectation_evaluated': True,\n        'contact_gaussian_density_bounded': False,\n        'hessian_ledger_evaluated': False,\n        'meaning': (\n            'exact residual Hessian polynomials after eliminating f_yy,f_xyy; '\n            'not a conditioned Gaussian expectation of |det H|'\n        ),",
    ),
    'claim_hessian_expectation_from_det_skeleton': (
        "'conditioned_hessian_det_skeleton_enumerated': True,\n        'conditioned_expectation_evaluated': False,\n        'contact_gaussian_density_bounded': False,\n        'hessian_ledger_evaluated': False,\n        'meaning': (\n            'exact linear form det=α_k·k+α_f_xxy·f_xxy after grad contact; '\n            'not a conditioned Gaussian expectation of |det H|'\n        ),",
        "'conditioned_hessian_det_skeleton_enumerated': True,\n        'conditioned_expectation_evaluated': True,\n        'contact_gaussian_density_bounded': False,\n        'hessian_ledger_evaluated': False,\n        'meaning': (\n            'exact linear form det=α_k·k+α_f_xxy·f_xxy after grad contact; '\n            'not a conditioned Gaussian expectation of |det H|'\n        ),",
    ),
    'claim_density_from_integrand_algebraic_factor': (
        "'global_contact_density_bound_proved': False,\n        'conditioned_expectation_evaluated': False,\n        'meaning': (\n            'exact algebraic Jacobian×|det H| factor products after grad contact; '\n            'does not bound the contact Gaussian density'\n        ),",
        "'global_contact_density_bound_proved': True,\n        'conditioned_expectation_evaluated': False,\n        'meaning': (\n            'exact algebraic Jacobian×|det H| factor products after grad contact; '\n            'does not bound the contact Gaussian density'\n        ),",
    ),
    'claim_density_from_algebraic_factor_times_height_r': (
        "'combined_algebraic_factor_and_height_r_recorded': True,\n        'height_r_absorbed_into_uniform_bound': False,\n        'combined_skeleton_absorbed_into_uniform_bound': False,\n        'contact_gaussian_density_bounded': False,\n        'conditioned_expectation_evaluated': False,\n        'global_contact_density_bound_proved': False,\n        'meaning': (\n            'exact (1/|det J|)·|det H| times unmatched height r^1 skeleton; '\n            'neither factor absorbed; Gaussian density still unbound'\n        ),",
        "'combined_algebraic_factor_and_height_r_recorded': True,\n        'height_r_absorbed_into_uniform_bound': True,\n        'combined_skeleton_absorbed_into_uniform_bound': True,\n        'contact_gaussian_density_bounded': True,\n        'conditioned_expectation_evaluated': False,\n        'global_contact_density_bound_proved': True,\n        'meaning': (\n            'exact (1/|det J|)·|det H| times unmatched height r^1 skeleton; '\n            'neither factor absorbed; Gaussian density still unbound'\n        ),",
    ),
    'claim_thin_belt_density_from_algebraic_factor_times_height_r': (
        "'reciprocal_diverges_as_y2_to_0': True,\n        'free_residual_coordinates': ['k', 'f_xxy'],\n        'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,\n        'combined_algebraic_factor_and_height_r_recorded': True,\n        'height_r_absorbed_into_uniform_bound': False,\n        'combined_skeleton_absorbed_into_uniform_bound': False,\n        'uniform_integrand_bound_proved': False,\n        'contact_gaussian_density_bounded': False,\n        'conditioned_expectation_evaluated': False,\n        'global_contact_density_bound_proved': False,\n        'meaning': (\n            'exact thin-belt (1/|det J|)·|det H| times unmatched height r^1; '\n            'reciprocal diverges as y2→0; neither factor absorbed; density unbound'\n        ),",
        "'reciprocal_diverges_as_y2_to_0': True,\n        'free_residual_coordinates': ['k', 'f_xxy'],\n        'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,\n        'combined_algebraic_factor_and_height_r_recorded': True,\n        'height_r_absorbed_into_uniform_bound': True,\n        'combined_skeleton_absorbed_into_uniform_bound': True,\n        'uniform_integrand_bound_proved': True,\n        'contact_gaussian_density_bounded': True,\n        'conditioned_expectation_evaluated': False,\n        'global_contact_density_bound_proved': True,\n        'meaning': (\n            'exact thin-belt (1/|det J|)·|det H| times unmatched height r^1; '\n            'reciprocal diverges as y2→0; neither factor absorbed; density unbound'\n        ),",
    ),
    'claim_height_r_from_grad_residual': (
        "'unmatched_height_density_r_power': 1,\n        'explicit_r_factor_still_required': True,\n        'height_r_absorbed_into_uniform_bound': False,\n        'contact_gaussian_density_bounded': False,\n        'meaning': (\n            'exact H_height_next residual after eliminating f_yy,f_xyy; '\n            'unmatched r^1 and density bound remain open'\n        ),",
        "'unmatched_height_density_r_power': 1,\n        'explicit_r_factor_still_required': False,\n        'height_r_absorbed_into_uniform_bound': True,\n        'contact_gaussian_density_bounded': False,\n        'meaning': (\n            'exact H_height_next residual after eliminating f_yy,f_xyy; '\n            'unmatched r^1 and density bound remain open'\n        ),",
    ),
    'claim_thin_belt_density_from_cancel': (
        "'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,\n        'uniform_integrand_bound_proved': False,\n        'contact_gaussian_density_bounded': False,\n        'full_density_bound_proved': False,",
        "'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,\n        'uniform_integrand_bound_proved': True,\n        'contact_gaussian_density_bounded': True,\n        'full_density_bound_proved': True,",
    ),
    'claim_thin_belt_density_from_algebraic_factor': (
        "'reciprocal_diverges_as_y2_to_0': True,\n        'free_residual_coordinates': ['k', 'f_xxy'],\n        'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,\n        'contact_integrand_algebraic_factor_skeleton_enumerated': True,\n        'uniform_integrand_bound_proved': False,\n        'contact_gaussian_density_bounded': False,\n        'global_contact_density_bound_proved': False,",
        "'reciprocal_diverges_as_y2_to_0': True,\n        'free_residual_coordinates': ['k', 'f_xxy'],\n        'bare_reciprocal_L1_obstruction_cleared_by_cancel': True,\n        'contact_integrand_algebraic_factor_skeleton_enumerated': True,\n        'uniform_integrand_bound_proved': True,\n        'contact_gaussian_density_bounded': True,\n        'global_contact_density_bound_proved': True,",
    ),
    'claim_density_from_grad_contact_jacobian': (
        "'global_contact_density_bound_proved': False,\n        'meaning': (\n            'exact algebraic |det| factors for leading gradient contact maps; '\n            'does not bound the contact Gaussian density'\n        ),",
        "'global_contact_density_bound_proved': True,\n        'meaning': (\n            'exact algebraic |det| factors for leading gradient contact maps; '\n            'does not bound the contact Gaussian density'\n        ),",
    ),
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def identities():
    return {
        p.name: {
            'bytes': p.stat().st_size,
            'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
        }
        for p in ROOT.iterdir() if p.is_file()
    }


def execute(command, cwd, out, name, mutant=False):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=30)
    (out / (name + '.stdout')).write_text(result.stdout)
    (out / (name + '.stderr')).write_text(result.stderr)
    if mutant:
        require(
            result.returncode != 0
            and 'AssertionError' in result.stderr
            and 'FAILED (failures=' in result.stderr,
            'mutation was not detected by a test assertion: ' + name,
        )
        require(
            'SyntaxError' not in result.stderr and 'ImportError' not in result.stderr,
            'mutation caused an invalid-program error',
        )
    else:
        require(result.returncode == 0, 'baseline failed: ' + name)
        require(
            f'Ran {EXPECTED_TESTS} tests' in result.stderr and 'skipped=' not in result.stderr,
            'unexpected test coverage',
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    require(
        not out.exists() and not out.is_relative_to(ROOT),
        'a new output outside the source directory is required',
    )
    out.mkdir(parents=True)
    before = identities()
    source = (ROOT / 'mesoscopic_chart.py').read_text()
    report = {
        'passed': False,
        'python': sys.version,
        'distinct_tests': EXPECTED_TESTS,
        'distinct_semantic_mutations': len(MUTANTS),
        'modes': [],
        'meaning': (
            'same-author exact chart algebra for d=2 transverse J0; '
            'not analytic review or RN closure'
        ),
    }
    try:
        for mode, flags in [('normal', []), ('optimized', ['-O'])]:
            cmd = [sys.executable, '-B', *flags, '-S', '-m', 'unittest', '-v', 'test_mesoscopic_chart']
            execute(cmd, ROOT, out, 'tests_' + mode)
            output = subprocess.run(
                [sys.executable, '-B', *flags, '-S', 'mesoscopic_chart.py'],
                cwd=ROOT, capture_output=True, timeout=10,
            )
            require(output.returncode == 0, 'entry point failed: ' + mode)
            require(
                output.stdout == (ROOT / 'RESULTS.json').read_bytes(),
                'result byte mismatch',
            )
            (out / ('output_' + mode + '.json')).write_bytes(output.stdout)
            for name, (old, new) in MUTANTS.items():
                require(source.count(old) == 1, 'nonunique mutation: ' + name)
                scratch = out / 'mutants' / mode / name
                scratch.mkdir(parents=True)
                (scratch / 'mesoscopic_chart.py').write_text(source.replace(old, new))
                for filename in ('test_mesoscopic_chart.py', 'RESULTS.json'):
                    shutil.copyfile(ROOT / filename, scratch / filename)
                execute(cmd, scratch, out, 'mutation_' + mode + '_' + name, mutant=True)
            report['modes'].append(mode)
        require(before == identities(), 'source files changed during execution')
        report.update(passed=True, sources_unchanged=True, source_files=before)
    finally:
        (out / 'REPORT.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
