"""Engine shape tests: VaspEngine satisfies the Protocol class-level
contract without needing the conformance suite. The conformance suite
in test_engine_conformance.py covers the full mixin once fixtures are
populated.

Written as ``unittest.TestCase`` subclasses so the pyiron shared CI
(which runs ``unittest discover``) picks them up. Pytest also runs
them via its unittest compatibility layer.
"""

from __future__ import annotations

import os
import tempfile
import unittest


class TestVaspEngineImport(unittest.TestCase):
    def test_vasp_engine_imports(self) -> None:
        from pyiron_workflow_vasp.engine import VaspEngine

        self.assertIsNotNone(VaspEngine)


class TestVaspEngineShape(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmp_path = self._tmpdir.name

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_vasp_engine_satisfies_protocol(self) -> None:
        from pyiron_workflow_atomistics.engine import CalcInputStatic, Engine

        from pyiron_workflow_vasp.engine import VaspEngine

        eng = VaspEngine(
            EngineInput=CalcInputStatic(),
            working_directory=self.tmp_path,
        )
        self.assertIsInstance(
            eng,
            Engine,
            msg="VaspEngine does not satisfy the runtime_checkable Engine Protocol",
        )

    def test_with_working_directory_is_pure(self) -> None:
        from pyiron_workflow_atomistics.engine import CalcInputStatic

        from pyiron_workflow_vasp.engine import VaspEngine

        eng = VaspEngine(EngineInput=CalcInputStatic(), working_directory=self.tmp_path)
        sub = eng.with_working_directory("subdir")
        self.assertEqual(sub.working_directory, os.path.join(self.tmp_path, "subdir"))
        self.assertEqual(eng.working_directory, self.tmp_path)
        self.assertIsNot(sub, eng)
        self.assertIs(type(sub), type(eng))

    def test_md_input_raises(self) -> None:
        from pyiron_workflow_atomistics.engine import CalcInputMD

        from pyiron_workflow_vasp.engine import VaspEngine

        with self.assertRaisesRegex(NotImplementedError, "MD"):
            VaspEngine(EngineInput=CalcInputMD(), working_directory=self.tmp_path)


if __name__ == "__main__":
    unittest.main()
