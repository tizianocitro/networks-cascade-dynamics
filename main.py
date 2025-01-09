from experiment import run_experiment
import os


def setup(exp_name="experiment"):
    # set for logging file
    os.environ["LOG_FILE_DIR"] = "logs"
    os.environ["LOG_FILE_PATH"] = exp_name


if __name__ == "__main__":
    epochs = 50
    graph_name = "erdos_renyi_graph"
    cost = 500
    n = 20

    for i in range(1):
        exp_name = f"testing experiment {i}"
        setup(exp_name)
        run_experiment(exp_name, epochs, graph_name, cost, n)