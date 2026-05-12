"""Conformance: VaspEngine satisfies pyiron_workflow_atomistics.engine.Engine.

Wraps the upstream EngineConformanceTests mixin (pytest-style) in a
unittest.TestCase subclass so the shared pyiron CI (which runs
``unittest discover``) picks it up.

The run() smoke uses a mock VASP command - the command simply copies
canned vasprun.xml/OUTCAR/CONTCAR files into the test working directory,
then `_run.run_vasp` continues into the parser path. This sidesteps the
need for a real VASP binary in CI.

If the canned fixtures haven't been generated yet (`.gitkeep` only),
test_run_returns_engine_output is skipped via SkipTest. The other four
mixin methods always run.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

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


class _VaspEngineConformance(EngineConformanceTests):
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


class TestVaspEngineConformance(unittest.TestCase):
    """Wraps the pytest-style EngineConformanceTests mixin so unittest
    discover picks it up. Each test method delegates to a fresh
    _VaspEngineConformance() instance with a unittest-managed tmp_path.
    """

    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmpdir.name)
        self._mixin = _VaspEngineConformance()

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_satisfies_engine_protocol(self) -> None:
        self._mixin.test_satisfies_engine_protocol(self.tmp_path)

    def test_with_working_directory_is_pure(self) -> None:
        self._mixin.test_with_working_directory_is_pure(self.tmp_path)

    def test_pickleable(self) -> None:
        self._mixin.test_pickleable(self.tmp_path)

    def test_get_calculate_fn_signature(self) -> None:
        self._mixin.test_get_calculate_fn_signature(self.tmp_path)

    def test_run_returns_engine_output(self) -> None:
        if not _fixtures_populated():
            self.skipTest(
                f"Canned fixtures not populated at {_FIXTURE_ROOT}. "
                "Run `python tests/fixtures/generate.py` with a real "
                "vasp_std to regenerate."
            )
        self._mixin.test_run_returns_engine_output(self.tmp_path)


if __name__ == "__main__":
    unittest.main()
