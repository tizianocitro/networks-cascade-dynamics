from experiment import run_experiment


if __name__ == "__main__":
    epochs = 50
    graph_name = "erdos_renyi_graph"
    cost = 500
    n = 20
    for i in range(1):
        run_experiment(f"testing experiment {i}", epochs, graph_name, cost, n)