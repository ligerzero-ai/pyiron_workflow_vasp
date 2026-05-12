"""One-off fixture generator. Run locally with a real `vasp_std` to
populate tests/fixtures/{cu_static, cu_minimize}/ with the canned
vasprun.xml, OUTCAR, CONTCAR that the conformance suite copies into
the test working directory via a mock command.

Usage:
    cd pyiron_workflow_vasp
    python tests/fixtures/generate.py \\
        --command 'mpirun -n 4 vasp_std' \\
        --potcar-config ~/.pyiron_vasp_config

After this completes, commit the generated binaries:

    git add tests/fixtures/cu_static tests/fixtures/cu_minimize
    git commit -m 'test(fixtures): populate cu_static and cu_minimize'
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ase.build import bulk

HERE = Path(__file__).resolve().parent
OUTPUT_FILES = ("vasprun.xml", "OUTCAR", "CONTCAR")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--command",
        default="vasp_std",
        help="The VASP run command to pass to VaspEngine.",
    )
    parser.add_argument(
        "--potcar-config",
        type=Path,
        required=True,
        help="Path to a .pyiron_vasp_config file resolving POTCAR paths.",
    )
    args = parser.parse_args()

    from pyiron_workflow_atomistics.engine import (
        CalcInputMinimize,
        CalcInputStatic,
    )

    from pyiron_workflow_vasp.engine import VaspEngine

    structure = bulk("Cu", "fcc", a=3.6, cubic=True)

    for sub, engine_input in (
        ("cu_static", CalcInputStatic()),
        (
            "cu_minimize",
            CalcInputMinimize(
                force_convergence_tolerance=0.05,
                max_iterations=5,
                relax_cell=False,
            ),
        ),
    ):
        workdir = HERE / sub
        workdir.mkdir(parents=True, exist_ok=True)
        # Wipe stale outputs before re-running
        for fname in OUTPUT_FILES:
            (workdir / fname).unlink(missing_ok=True)

        engine = VaspEngine(
            EngineInput=engine_input,
            working_directory=str(workdir),
            potcar_config_file=args.potcar_config,
            command=args.command,
        )
        fn, kwargs = engine.get_calculate_fn(structure)
        output = fn(structure=structure, **kwargs)
        assert output is not None
        print(f"{sub}: E = {output.final_energy} eV, converged = {output.converged}")

        # Sanity: ensure the three canned files we care about exist
        for fname in OUTPUT_FILES:
            assert (workdir / fname).exists(), f"missing {workdir / fname}"


if __name__ == "__main__":
    main()
