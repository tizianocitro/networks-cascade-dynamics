from experiment import run_experiment
from argparse import ArgumentParser
import os


def setup(exp_name="experiment"):
    # set for logging file
    os.environ["LOG_FILE_ENABLED"] = "True"
    os.environ["LOG_FILE_DIR"] = "logs"
    os.environ["LOG_FILE_PATH"] = exp_name

    os.environ["LOG_CONSOLE_ENABLED"] = "False"


if __name__ == "__main__":
    parser = ArgumentParser(description="Run experiments.")
    parser.add_argument("-g", "--graph_name", type=str, default="erdos_renyi_graph", help="Graph name")
    parser.add_argument("-c", "--cost", type=int, default=500, help="Cost value")
    parser.add_argument("-n", "--set_size", type=int, default=20, help="Size of seed set")
    parser.add_argument("-mt", "--majority_thresholds", action="store_true", help="Use majority thresholds")
    parser.add_argument("-bop", "--best_of_population", action="store_true", help="Use best of genetic degree/cost population as degree/cost seed set")
    parser.add_argument("-e", "--epochs", type=int, default=50, help="Number of epochs")
    parser.add_argument("-r", "--runs", type=int, default=1, help="Number of experiments to run")
    parser.add_argument("-exp", "--experiment_name", type=str, default="Experiment", help="Experiment name")
    args = parser.parse_args()

    graph_name = args.graph_name
    cost = args.cost
    n = args.set_size
    epochs = args.epochs
    runs = args.runs
    exp_name = args.experiment_name
    thresholds_as_majority = args.majority_thresholds
    with_best_of_starting_population = args.best_of_population

    options = {
        "thresholds_as_majority": thresholds_as_majority,
        "with_best_of_starting_population": with_best_of_starting_population,
    }

    for i in range(runs):
        run_name = f"{exp_name} {i}"
        setup(run_name)
        run_experiment(run_name, epochs, graph_name, cost, n, options)