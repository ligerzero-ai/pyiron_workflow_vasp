"""VaspEngine new knobs (ediff, lreal, compress_outputs, remove_workdir).

The first two reach INCAR via _build_incar_overrides; the last two are
post-run cleanup flags handled in run_vasp.
"""

import pytest
from pyiron_workflow_atomistics.engine import CalcInputStatic

from pyiron_workflow_vasp._run import _build_incar_overrides
from pyiron_workflow_vasp.engine import VaspEngine


class TestEdiffLreal:
    def test_ediff_lands_in_overrides(self):
        overrides = _build_incar_overrides(ediff=1e-5, lreal=None)
        assert overrides["EDIFF"] == pytest.approx(1e-5)
        assert "LREAL" not in overrides

    def test_lreal_false_lands_in_overrides(self):
        overrides = _build_incar_overrides(ediff=None, lreal=False)
        assert overrides["LREAL"] is False
        assert "EDIFF" not in overrides

    def test_lreal_auto_string_passes_through(self):
        overrides = _build_incar_overrides(ediff=None, lreal="Auto")
        assert overrides["LREAL"] == "Auto"

    def test_both_none_means_empty(self):
        assert _build_incar_overrides(ediff=None, lreal=None) == {}


class TestCleanupKnobsExist:
    def test_defaults(self):
        eng = VaspEngine(EngineInput=CalcInputStatic())
        assert eng.compress_outputs is False
        assert eng.remove_workdir is False

    def test_can_set(self):
        eng = VaspEngine(
            EngineInput=CalcInputStatic(),
            compress_outputs=True,
            remove_workdir=True,
        )
        assert eng.compress_outputs is True
        assert eng.remove_workdir is True


class TestKwargsPropagate:
    def test_get_calculate_fn_passes_all_four(self):
        eng = VaspEngine(
            EngineInput=CalcInputStatic(),
            ediff=1e-5,
            lreal=False,
            compress_outputs=True,
            remove_workdir=False,
        )
        # Build a dummy structure since the API needs one to return kwargs.
        from ase.build import bulk

        _fn, kwargs = eng.get_calculate_fn(bulk("Cu", "fcc", a=3.6, cubic=True))
        assert kwargs["ediff"] == pytest.approx(1e-5)
        assert kwargs["lreal"] is False
        assert kwargs["compress_outputs"] is True
        assert kwargs["remove_workdir"] is False
