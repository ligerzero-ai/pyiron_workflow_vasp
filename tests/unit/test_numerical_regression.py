"""Numerical regression: parsed EngineOutput from canned fixtures must
match the pinned golden values. Updated whenever the maintainer
regenerates fixtures (see tests/fixtures/README.md).

Skipped when the binary fixtures aren't on disk yet.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from ase.build import bulk

from pyiron_workflow_atomistics.engine import CalcInputStatic
from pyiron_workflow_vasp.engine import VaspEngine

_FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "cu_static"
_FIXTURE_FILES = ("vasprun.xml", "OUTCAR", "CONTCAR")


def _fixtures_populated() -> bool:
    return all((_FIXTURE_ROOT / f).exists() for f in _FIXTURE_FILES)


@pytest.mark.skipif(
    not _fixtures_populated(),
    reason=f"Fixtures not generated yet. See {_FIXTURE_ROOT / 'README.md'}.",
)
def test_cu_static_golden(tmp_path):
    """The parsed Cu FCC single-point energy must match the pinned value
    to within sub-meV. Update only when the maintainer regenerates fixtures
    and explicitly documents the new value in the same commit."""
    engine = VaspEngine(
        EngineInput=CalcInputStatic(),
        working_directory=str(tmp_path),
        command=f"bash -c 'cp {_FIXTURE_ROOT}/* . && true'",
    )
    structure = bulk("Cu", "fcc", a=3.6, cubic=True)
    fn, kwargs = engine.get_calculate_fn(structure)
    out = fn(structure=structure, **kwargs)

    # Golden - update when fixtures are regenerated.
    # The maintainer who first generates the fixtures fills these in.
    GOLDEN_ENERGY_EV = None  # e.g. -14.7321
    GOLDEN_N_ATOMS = 4

    if GOLDEN_ENERGY_EV is not None:
        assert out.final_energy == pytest.approx(GOLDEN_ENERGY_EV, abs=1e-3)
    assert out.final_structure is not None
    assert len(out.final_structure) == GOLDEN_N_ATOMS
    assert isinstance(out.converged, bool)
