"""Driver script for piglot."""
import os
import os.path
import argparse
import shutil
from yaml import safe_dump
from piglot.yaml_parser import parse_parameters, parse_optimiser, parse_config_file
from piglot.yaml_parser import parse_objective, parse_stop_criteria
from piglot.objectives import read_objective
from piglot.optimisers import read_optimiser


def parse_args():
    """Parse command line arguments of the script.

    Returns
    -------
    argparse.Namespace
        Parsed arguments
    """
    # Global argument parser settings
    parser = argparse.ArgumentParser(
        prog='piglot',
        description='Parameter identification toolbox',
    )

    # Add arguments: configuration file
    parser.add_argument(
        'config',
        type=str,
        help='Configuration file to use',
    )

    return parser.parse_args()



def main():
    """Entry point for piglot."""
    args = parse_args()
    config = parse_config_file(args.config)
    # Build output directory with a copy of the configuration file
    output_dir = config["output"]
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "config"), 'w', encoding='utf8') as file:
        safe_dump(config, file)
    # Build piglot problem
    parameters = parse_parameters(config)
    objective = read_objective(config["objective"], parameters, output_dir)
    optimiser = read_optimiser(config["optimiser"], objective)
    stop = parse_stop_criteria(config)
    # Run the optimisation
    _, best_params = optimiser.optimise(
        config["iters"],
        parameters,
        output_dir,
        verbose=not config["quiet"],
        stop_criteria=stop,
    )
    # Re-run the best case
    if 'skip_last_run' not in config:
        objective(parameters.normalise(best_params))



if __name__ == '__main__':
    main()
