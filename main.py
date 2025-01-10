from experiment import run_experiment
import argparse
import os


def setup(exp_name="experiment"):
    # set for logging file
    os.environ["LOG_FILE_DIR"] = "logs"
    os.environ["LOG_FILE_PATH"] = exp_name


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run experiments.")
    parser.add_argument("-g", "--graph_name", type=str, default="erdos_renyi_graph", help="Graph name")
    parser.add_argument("-c", "--cost", type=int, default=500, help="Cost value")
    parser.add_argument("-n", "--set_size", type=int, default=20, help="Size of seed set")
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

    for i in range(runs):
        run_name = f"{exp_name} {i}"
        setup(run_name)
        run_experiment(run_name, epochs, graph_name, cost, n)