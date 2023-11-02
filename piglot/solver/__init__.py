"""Interface for solvers."""
from typing import Any, Dict, Type
from piglot.parameter import ParameterSet
from piglot.solver.solver import Solver
from piglot.solver.links.solver import LinksSolver


AVAILABLE_SOLVERS: Dict[str, Type[Solver]] = {
    'links': LinksSolver,
}


def read_solver(config: Dict[str, Any], parameters: ParameterSet, output_dir: str) -> Solver:
    """Read the solver from the configuration dictionary.

    Parameters
    ----------
    config : Dict[str, Any]
        Configuration dictionary.
    parameters : ParameterSet
        Parameter set for this problem.
    output_dir : str
        Path to the output directory.

    Returns
    -------
    Solver
        Solver to use for this problem.
    """
    # Read the solver name (and pop it from the dictionary)
    if not 'name' in config:
        raise ValueError("Missing name for solver.")
    name = config.pop('name')
    # Delegate to the solver reader
    if not name in AVAILABLE_SOLVERS:
        raise ValueError(f"Unknown solver '{name}'.")
    return AVAILABLE_SOLVERS[name].read(config, parameters, output_dir)
