#!/usr/bin/env python3
"""Prepared stage66 original entry capture; no execution on import."""
import sys
from capture_boundary import capture
from custody import R

if __name__=='__main__':
    raise SystemExit(capture('entry',[sys.executable,str(R/'launch_finalization.py')]))
