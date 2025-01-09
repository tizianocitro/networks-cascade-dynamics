from network import *
from utils import *
from heapq import *
import matplotlib.pyplot as plt
from datetime import datetime
from genetic_simulation import GeneticSimulation
from degree_simulation import DegreeSimulation, DegreeCostSimulation


def run_experiment(exp_name="experiment", epochs=10, graph_name="karate_club_graph", cost=0, n=20):
    results = {}

    log(text=f"\n{BLUE}### STARTING EXPERIMENT {exp_name} ###{RESET}\n")

    genetic_sim = GeneticSimulation(name="Genetic", cost=cost, n=n, epochs=epochs)
    _, _, epoch_scores = genetic_sim.run(graph_name)
    results[genetic_sim.name] = (epoch_scores, LINE_BLUE)

    degree_sim = DegreeSimulation(name="Degree", cost=cost)
    _, max_score = degree_sim.run(graph_name)
    epoch_scores = {epoch: max_score for epoch in range(epochs)}
    results[degree_sim.name] = (epoch_scores, LINE_RED)

    degree_cost_sim = DegreeCostSimulation(name="Degree/Cost", cost=cost)
    _, max_score = degree_cost_sim.run(graph_name)
    epoch_scores = {epoch: max_score for epoch in range(epochs)}
    results[degree_cost_sim.name] = (epoch_scores, LINE_GREEN)

    save_results(exp_name, results)

    log(text=f"\n{BLUE}### ENDING EXPERIMENT {exp_name} ###{RESET}\n")


def save_result(seed_sets, max_score, epoch_scores, exp_name):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    epochs = list(epoch_scores.keys())
    scores = list(epoch_scores.values())

    plt.figure(figsize=(8, 5))
    plt.title("Score in Each Epoch", fontsize=15)
    plt.plot(epochs, scores, marker="o", linestyle="-", color="b", label="Score")

    plt.xlabel("Epoch", fontsize=13)
    plt.xticks(epochs, rotation=90, ha="right", fontsize=9)

    plt.ylabel("Score", fontsize=13)
    plt.yticks(fontsize=10)

    plt.legend(fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.4)

    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    output_filename = os.path.join(results_dir, f"{exp_name}_{timestamp}.png")
    plt.savefig(output_filename, dpi=300, bbox_inches="tight")


def save_results(exp_name, simulation_results):
    """
    Save results and plot epoch scores for multiple experiments.

    Args:
        exp_name (str): Name of the main experiment (used in the filename).
        results (dict): Dictionary where keys are experiment names, and values are tuples:
                        (epoch_scores: dict, color: str).
                        Example: {"Exp1": ({1: 10, 2: 15}, "b"), "Exp2": ({1: 12, 2: 18}, "r")}
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    first_exp_epoch_scores = simulation_results[list(simulation_results.keys())[0]][0]
    epochs = list(first_exp_epoch_scores.keys())

    plt.figure(figsize=(8, 5))
    plt.title("Score in Each Epoch", fontsize=15)

    plt.xlabel("Epoch", fontsize=13)
    plt.xticks(epochs, rotation=90, ha="right", fontsize=9)

    plt.ylabel("Score", fontsize=13)
    plt.yticks(fontsize=10)

    for sim_name, (epoch_scores, color) in simulation_results.items():
        scores = list(epoch_scores.values())
        plt.plot(epochs, scores, marker="", linestyle="-", color=color, label=sim_name)

    plt.legend(fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.4)

    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    output_filename = os.path.join(results_dir, f"{exp_name}_{timestamp}.png")
    plt.savefig(output_filename, dpi=300, bbox_inches="tight")
    plt.close()