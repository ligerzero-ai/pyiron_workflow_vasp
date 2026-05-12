# VASP conformance test fixtures

The two subdirectories (`cu_static/`, `cu_minimize/`) hold canned VASP
output (`vasprun.xml`, `OUTCAR`, `CONTCAR`) from a 4-atom FCC Cu
single-point and a 5-step relaxation. The conformance suite at
`tests/unit/test_engine_conformance.py` uses a mock VASP command of
the form

    bash -c 'cp -r <fixture-dir>/* . && true'

so the parser can be exercised end-to-end in CI without a real
`vasp_std` binary.

## Regenerating

Requires a real VASP install + a configured `~/.pyiron_vasp_config`
that resolves POTCAR paths. From the repo root:

    python tests/fixtures/generate.py \
        --command 'mpirun -n 4 vasp_std' \
        --potcar-config ~/.pyiron_vasp_config

This re-runs both calculations and overwrites the canned files. After
the script completes, commit the regenerated binaries:

    git add tests/fixtures/cu_static tests/fixtures/cu_minimize
    git commit -m 'test(fixtures): refresh cu_static and cu_minimize'

Pinned golden values in `tests/unit/test_numerical_regression.py`
will need updating in the same commit if VASP semantics shifted.

## CI behaviour without fixtures

When the binaries are absent (e.g. first PR, before a maintainer has
generated them), `test_engine_conformance.py::test_run_returns_engine_output`
is automatically skipped via `pytest.skip`. The other four mixin
methods (Protocol satisfaction, `with_working_directory`, pickle,
`get_calculate_fn` signature) run regardless and gate the PR.
