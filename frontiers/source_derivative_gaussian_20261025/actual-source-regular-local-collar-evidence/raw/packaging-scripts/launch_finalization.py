#!/usr/bin/env python3
"""Prepared stage66 outer capture; no execution on import."""
import sys
from capture_boundary import capture
from custody import R

if __name__=='__main__':
    raise SystemExit(capture('outer',[sys.executable,str(R/'run_finalization.py')]))
