"""Engine shape pre-test: VaspEngine satisfies the Protocol class-level
contract without needing the conformance suite. Refined into the full
EngineConformanceTests subclass in Task 7."""

from pathlib import Path

import pytest


def test_vasp_engine_imports():
    from pyiron_workflow_vasp.engine import VaspEngine

    assert VaspEngine is not None


def test_vasp_engine_satisfies_protocol(tmp_path: Path):
    from pyiron_workflow_atomistics.engine import CalcInputStatic, Engine

    from pyiron_workflow_vasp.engine import VaspEngine

    eng = VaspEngine(
        EngineInput=CalcInputStatic(),
        working_directory=str(tmp_path),
    )
    assert isinstance(
        eng, Engine
    ), "VaspEngine does not satisfy the runtime_checkable Engine Protocol"


def test_with_working_directory_is_pure(tmp_path: Path):
    import os

    from pyiron_workflow_atomistics.engine import CalcInputStatic

    from pyiron_workflow_vasp.engine import VaspEngine

    eng = VaspEngine(EngineInput=CalcInputStatic(), working_directory=str(tmp_path))
    sub = eng.with_working_directory("subdir")
    assert sub.working_directory == os.path.join(str(tmp_path), "subdir")
    assert eng.working_directory == str(tmp_path)
    assert sub is not eng
    assert type(sub) is type(eng)


def test_md_input_raises(tmp_path: Path):
    from pyiron_workflow_atomistics.engine import CalcInputMD

    from pyiron_workflow_vasp.engine import VaspEngine

    with pytest.raises(NotImplementedError, match="MD"):
        VaspEngine(EngineInput=CalcInputMD(), working_directory=str(tmp_path))
