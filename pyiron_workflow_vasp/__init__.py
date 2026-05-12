"""pyiron_workflow_vasp - VASP integration for the pyiron workflow system.

Public API:
    VaspEngine - satisfies pyiron_workflow_atomistics.engine.Engine
                  for Static + Minimize modes; wraps the helpers in
                  vasp.py and vasp_parser/output.py.

Plus the existing standalone helper functions in vasp and generic
(re-exported via wildcard for backwards compatibility with the 0.0.x
script-style API).
"""

from .engine import VaspEngine
from .generic import *  # noqa: F401,F403  -- legacy helpers
from .vasp import *  # noqa: F401,F403      -- legacy helpers

__version__ = "0.1.0"
__all__ = ["VaspEngine"]
