# Mesoscopic chart J0 — d=2 transverse contact rows

[Research home](https://github.com/d6g8k5htny-coder/main) · [Proof](PROOF.md) · [PR7 reduction](https://github.com/d6g8k5htny-coder/Math-/pull/7)

Exact algebraic enumeration of contact divided-difference rows and gradient Jacobian `r`-power on one declared scaled-annulus chart (`C_transverse`, d=2). Complements PR7; does not edit its body; does not close the annulus or discharge 24-jet / RN certificates.

```sh
python -B -S mesoscopic_chart.py
python -B -S -m unittest -v test_mesoscopic_chart
python -B -S run_validation.py --output /tmp/mesoscopic-chart-new-run
```

19 distinct tests and seven semantic mutations. Scientific effect: NONE.
