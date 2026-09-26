#!/usr/bin/env python3
"""Reproduce the source-bound H5 rim literal finding; no numerical hunt."""
import argparse
import json
from pathlib import Path

from rim_contract import reproduction_report


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
HUNT = REPO / 'imports/upper2d_stage_e_20260926/raw/STAGE_E/hunt_rim.py'
LEDGER = (REPO / 'imports/upper2d_h5_ledgers_20260926/raw/H5_closure'
          / 'h5_results_r0.05_s0p1_rimprobes.jsonl')
HUNT_SHA256 = 'de73e5fed00782c3709d2f9a8b1cddca23926606a8ef5ffc4cf0de8aefb66f90'
LEDGER_SHA256 = '22c7107e93ba9c02bea1f6f34085044ab535f29c067ce79c0cd7d8b1911ecc63'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--emit', action='store_true', help='emit the JSON reproduction receipt')
    args = parser.parse_args()
    report = reproduction_report(HUNT, LEDGER)
    if report['historical_hunt_sha256'] != HUNT_SHA256:
        raise ValueError('historical hunt source identity changed')
    if report['ledger_sha256'] != LEDGER_SHA256:
        raise ValueError('radius-0.05 rim ledger identity changed')
    if args.emit:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print('H5 RIM CONTRACT REPRODUCED: angle 175 is the only literal mismatch')
        print('Scientific effect NONE; numerical hunt and bound certification not performed.')


if __name__ == '__main__':
    main()
