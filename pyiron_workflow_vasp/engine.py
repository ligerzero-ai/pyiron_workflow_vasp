"""VaspEngine satisfying the pyiron_workflow_atomistics Engine Protocol.

Static + Minimize modes only. CalcInputMD is rejected at construction
time with NotImplementedError - MD support is a future PR.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Callable, Literal

from ase import Atoms

from pyiron_workflow_atomistics.engine import (
    CalcInputMD,
    CalcInputMinimize,
    CalcInputStatic,
    EngineOutput,
)


@dataclass
class VaspEngine:
    """VASP backend for the pyiron_workflow Engine ecosystem.

    Composes the existing pyiron_workflow_vasp helpers
    (write_POSCAR/INCAR/KPOINTS/POTCAR, generic.shell, vasp_parser.output)
    behind the Engine Protocol contract.

    Static and Minimize modes are supported. MD raises
    NotImplementedError at construction time - the Engine Protocol's
    type union allows CalcInputMD but this engine doesn't implement
    NSW + MDALGO + TEBEG/TEEND wiring yet.
    """

    EngineInput: CalcInputStatic | CalcInputMinimize | CalcInputMD
    working_directory: str = field(default_factory=os.getcwd)

    # VASP-specific configuration
    potcar_config_file: Path | None = None
    functional: Literal["GGA", "LDA"] = "GGA"
    encut: float = 520.0
    kpoints_density: float = 0.30
    command: str = "vasp_std"
    mode: Literal["static", "minimize"] = field(init=False)

    def __post_init__(self) -> None:
        if isinstance(self.EngineInput, CalcInputMinimize):
            self.mode = "minimize"
        elif isinstance(self.EngineInput, CalcInputStatic):
            self.mode = "static"
        else:
            raise NotImplementedError(
                f"VaspEngine MD support not yet implemented "
                f"(got {type(self.EngineInput).__name__}). "
                "Use CalcInputStatic or CalcInputMinimize for now."
            )

    def with_working_directory(self, subdir: str) -> "VaspEngine":
        """Return a pure copy with the working directory composed."""
        return replace(
            self,
            working_directory=os.path.join(self.working_directory, subdir),
        )

    def get_calculate_fn(
        self, structure: Atoms
    ) -> tuple[Callable[..., EngineOutput], dict[str, Any]]:
        """Return (callable, kwargs). The callable will be invoked as
        callable(structure=structure, **kwargs) and must return an
        EngineOutput."""
        from pyiron_workflow_vasp._run import run_vasp

        kwargs = {
            "working_directory": self.working_directory,
            "engine_input": self.EngineInput,
            "potcar_config_file": self.potcar_config_file,
            "functional": self.functional,
            "encut": self.encut,
            "kpoints_density": self.kpoints_density,
            "command": self.command,
            "mode": self.mode,
        }
        return run_vasp, kwargs
