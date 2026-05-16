"""ISIF assignment must derive from CalcInputMinimize.cell_relaxation."""

import pytest
from pyiron_workflow_atomistics.engine import CalcInputMinimize, CalcInputStatic

from pyiron_workflow_vasp._run import _build_incar_params


@pytest.mark.parametrize(
    "mode,expected_isif",
    [("none", 2), ("volume", 7), ("shape", 5), ("full", 3)],
)
def test_isif_mapping(mode, expected_isif):
    ci = CalcInputMinimize(cell_relaxation=mode, max_iterations=42)
    params = _build_incar_params(ci, mode="minimize", encut=400.0)
    assert params["ISIF"] == expected_isif
    assert params["NSW"] == 42


def test_static_mode_sets_nsw_zero_and_omits_isif():
    params = _build_incar_params(CalcInputStatic(), mode="static", encut=400.0)
    assert params["NSW"] == 0
    # ISIF is meaningless when NSW=0; the helper should not set it.
    assert "ISIF" not in params
