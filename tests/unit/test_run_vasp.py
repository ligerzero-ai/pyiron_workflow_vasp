"""Unit tests for the run_vasp callable. Uses an artificial 'mock command'
that does nothing (no fixtures yet) - verifies the function imports and
matches the expected signature shape. End-to-end parser coverage lives
in test_engine_conformance.py once fixtures are populated.

Written as ``unittest.TestCase`` subclasses so the pyiron shared CI
(which runs ``unittest discover``) picks them up.
"""

from __future__ import annotations

import inspect
import unittest


class TestRunVaspSignature(unittest.TestCase):
    def test_run_vasp_importable(self) -> None:
        from pyiron_workflow_vasp._run import run_vasp

        self.assertTrue(callable(run_vasp))

    def test_run_vasp_signature(self) -> None:
        """Signature must accept the kwargs VaspEngine.get_calculate_fn
        promises to supply: working_directory, engine_input,
        potcar_config_file, functional, encut, kpoints_density, command,
        mode. Plus the positional `structure` argument that the caller
        passes."""
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
        missing = expected - actual
        self.assertFalse(missing, msg=f"missing parameters: {missing}")


if __name__ == "__main__":
    unittest.main()
