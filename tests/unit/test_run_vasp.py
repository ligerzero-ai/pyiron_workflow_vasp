"""Unit-test the run_vasp callable. Uses an artificial 'mock command'
that does nothing (no fixtures yet) - verifies the function imports
and matches the expected signature shape. End-to-end parser coverage
lives in test_engine_conformance.py once fixtures are populated."""


def test_run_vasp_importable():
    from pyiron_workflow_vasp._run import run_vasp

    assert callable(run_vasp)


def test_run_vasp_signature():
    """Signature must accept the kwargs VaspEngine.get_calculate_fn
    promises to supply: working_directory, engine_input, potcar_config_file,
    functional, encut, kpoints_density, command, mode. Plus the
    positional `structure` argument that the caller passes."""
    import inspect

    from pyiron_workflow_vasp._run import run_vasp

    sig = inspect.signature(run_vasp)
    expected = {
        "structure",
        "working_directory",
        "engine_input",
        "potcar_config_file",
        "functional",
        "encut",
        "kpoints_density",
        "command",
        "mode",
    }
    actual = set(sig.parameters.keys())
    assert expected.issubset(actual), f"missing: {expected - actual}"
