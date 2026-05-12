"""Conformance: VaspEngine satisfies pyiron_workflow_atomistics.engine.Engine.

Uses a mock VASP command for the run() smoke - the command simply copies
canned vasprun.xml/OUTCAR/CONTCAR files into the test working directory,
then `_run.run_vasp` continues into the parser path. This sidesteps the
need for a real VASP binary in CI.

If the canned fixtures haven't been generated yet (`.gitkeep` only),
test_run_returns_engine_output skips via pytest.skip. The other four
mixin methods always run.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from ase.build import bulk

from pyiron_workflow_atomistics.engine import CalcInputStatic
from pyiron_workflow_atomistics.testing import EngineConformanceTests

from pyiron_workflow_vasp.engine import VaspEngine

_FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "cu_static"
_FIXTURE_FILES = ("vasprun.xml", "OUTCAR", "CONTCAR")


def _fixtures_populated() -> bool:
    return all((_FIXTURE_ROOT / f).exists() for f in _FIXTURE_FILES)


def _mock_command() -> str:
    """Construct the mock command: cp the fixture files into cwd, exit 0."""
    if not _fixtures_populated():
        # No fixtures -> return a command that lets the engine construct but
        # would fail at run(). The run() test below skips before reaching this.
        return "/bin/true"
    return f"bash -c 'cp {_FIXTURE_ROOT}/* . && true'"


class TestVaspEngineConformance(EngineConformanceTests):
    @staticmethod
    def engine_factory(tmp_path):
        return VaspEngine(
            EngineInput=CalcInputStatic(),
            working_directory=str(tmp_path),
            command=_mock_command(),
        )

    @staticmethod
    def test_structure_factory():
        # Match the 4-atom Cu FCC the canned fixture was generated for
        return bulk("Cu", "fcc", a=3.6, cubic=True)

    # Override only the run() smoke - guard with fixture presence
    def test_run_returns_engine_output(self, tmp_path):
        if not _fixtures_populated():
            pytest.skip(
                f"Canned fixtures not populated at {_FIXTURE_ROOT}. "
                "Run `python tests/fixtures/generate.py` with a real "
                "vasp_std to regenerate."
            )
        # Otherwise defer to the base implementation
        return super().test_run_returns_engine_output(tmp_path)
