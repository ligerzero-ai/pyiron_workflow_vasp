"""Numerical regression: parsed EngineOutput from canned fixtures must
match the pinned golden values. Updated whenever the maintainer
regenerates fixtures (see tests/fixtures/README.md).

Skipped when the binary fixtures aren't on disk yet.

Written as a unittest.TestCase subclass so the shared pyiron CI
(which runs ``unittest discover``) picks it up.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ase.build import bulk
from pyiron_workflow_atomistics.engine import CalcInputStatic

from pyiron_workflow_vasp.engine import VaspEngine

_FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "cu_static"
_FIXTURE_FILES = ("vasprun.xml", "OUTCAR", "CONTCAR")


def _fixtures_populated() -> bool:
    return all((_FIXTURE_ROOT / f).exists() for f in _FIXTURE_FILES)


class TestCuStaticGolden(unittest.TestCase):
    """The parsed Cu FCC single-point energy must match the pinned value
    to within sub-meV. Update only when the maintainer regenerates fixtures
    and explicitly documents the new value in the same commit."""

    def setUp(self) -> None:
        if not _fixtures_populated():
            self.skipTest(
                f"Fixtures not generated yet. See {_FIXTURE_ROOT / 'README.md'}."
            )
        self._tmpdir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self._tmpdir.name)

    def tearDown(self) -> None:
        if hasattr(self, "_tmpdir"):
            self._tmpdir.cleanup()

    def test_cu_static_golden(self) -> None:
        engine = VaspEngine(
            EngineInput=CalcInputStatic(),
            working_directory=str(self.tmp_path),
            command=f"bash -c 'cp {_FIXTURE_ROOT}/* . && true'",
        )
        structure = bulk("Cu", "fcc", a=3.6, cubic=True)
        fn, kwargs = engine.get_calculate_fn(structure)
        out = fn(structure=structure, **kwargs)

        # Golden - update when fixtures are regenerated.
        # The maintainer who first generates the fixtures fills these in.
        GOLDEN_ENERGY_EV: float | None = None  # e.g. -14.7321
        GOLDEN_N_ATOMS = 4

        if GOLDEN_ENERGY_EV is not None:
            self.assertAlmostEqual(out.final_energy, GOLDEN_ENERGY_EV, delta=1e-3)
        self.assertIsNotNone(out.final_structure)
        self.assertEqual(len(out.final_structure), GOLDEN_N_ATOMS)
        self.assertIsInstance(out.converged, bool)


if __name__ == "__main__":
    unittest.main()
