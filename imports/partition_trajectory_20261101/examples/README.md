# Examples

Run every built-in suite from the package root:

```bash
python3 -m partition_trajectory
```

Run only the verification tests:

```bash
python3 -m unittest discover -s tests -v
```

`custom_analysis.py` is a minimal starting point for a new finite model. The important convention is that required suffix partitions and observation functions are stage-indexed. Use `lambda h: None` when no new observation arrives between stages.

The model suites return native Python dictionaries. The top-level command serializes them to JSON for inspection or downstream analysis.
