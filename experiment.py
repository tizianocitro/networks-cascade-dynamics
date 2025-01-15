from typing import Any, Dict
from network import *
from utils import *
from heapq import *
import matplotlib.pyplot as plt
from datetime import datetime
from genetic_simulation import GeneticSimulation
from degree_simulation import DegreeSimulation, DegreeCostSimulation
from genetic_degree_simulation import GeneticDegreeSimulation, GeneticDegreeCostSimulation


def run_experiment(
    exp_name="experiment",
    epochs=10,
    graph_name="karate_club_graph",
    cost=0,
    n=20,
    options: Dict[Any, Any]=None,
):
    do_genetic_degree = load_options(options)

    results = {}

    log_important(text=f"\n{BLUE}### STARTING EXPERIMENT {exp_name} ###{RESET}")

    nodes_threshold, nodes_cost = setup_graph(graph_name)

    log_important(text=f"\n{YELLOW}### STARTING GENETIC ###{RESET}")
    genetic_sim = GeneticSimulation(
        name="Genetic",
        cost=cost,
        n=n,
        epochs=epochs,
        nodes_threshold=nodes_threshold,
        nodes_cost=nodes_cost,
    )
    _, genetic_score, epoch_scores = genetic_sim.run(graph_name)
    results[genetic_sim.name] = (epoch_scores, LINE_BLUE)
    log_important(text=f"Genetic score: {genetic_score}")

    if do_genetic_degree:
        log_important(text=f"\n{YELLOW}### STARTING GENETIC DEGREE ###{RESET}")
        genetic_degree_sim = GeneticDegreeSimulation(
            name="Genetic Degree",
            cost=cost,
            n=n,
            epochs=epochs,
            a_range=[0.1, 1],
            nodes_threshold=nodes_threshold,
            nodes_cost=nodes_cost,
        )
        _, genetic_degree_score, epoch_scores = genetic_degree_sim.run(graph_name)
        results[genetic_degree_sim.name] = (epoch_scores, LINE_YELLOW)
        log_important(text=f"Genetic Degree score: {genetic_degree_score}")

    log_important(text=f"\n{YELLOW}### STARTING GENETIC DEGREE/COST ###{RESET}")
    while True:
        try:
            genetic_degree_cost_sim = GeneticDegreeCostSimulation(
                name="Genetic Degree/Cost",
                cost=cost,
                n=n,
                epochs=epochs,
                a_range=[0.1, 1],
                b_range=[0.1, 1],
                nodes_threshold=nodes_threshold,
                nodes_cost=nodes_cost,
            )
            _, genetic_degree_cost_score, epoch_scores = genetic_degree_cost_sim.run(graph_name)
            results[genetic_degree_cost_sim.name] = (epoch_scores, LINE_PURPLE)
            log_important(text=f"Genetic Degree/Cost score: {genetic_degree_cost_score}")

            break
        except Exception as e:
            log_important(text=f"Retrying Genetic Degree/Cost because of \"{e}\"")

    log_important(text=f"\n{YELLOW}### STARTING GENETIC DEGREE/COST NO FIRST TOTAL ###{RESET}")
    try:
        genetic_degree_cost_no_total_sim = GeneticDegreeCostSimulation(
            name="Genetic Degree/Cost",
            cost=cost,
            n=n,
            epochs=epochs,
            a_range=[0.1, 1],
            b_range=[0.1, 1],
            nodes_threshold=nodes_threshold,
            nodes_cost=nodes_cost,
            with_first_total=False,
        )
        _, genetic_degree_cost_no_total_score, epoch_scores = genetic_degree_cost_no_total_sim.run(graph_name)
        log_important(text=f"Genetic Degree/Cost No First Total score: {genetic_degree_cost_no_total_score}")
        if genetic_degree_cost_no_total_score > genetic_degree_cost_score:
            log_important(text=f"Genetic Degree/Cost No First Total score performed better")
            genetic_degree_cost_score = genetic_degree_cost_no_total_score
            results[genetic_degree_cost_sim.name] = (epoch_scores, LINE_PURPLE)
    except Exception as e:
        log_important(text=f"Skipping Genetic Degree/Cost No First Total because of \"{e}\"")

    log_important(text=f"\n{YELLOW}### STARTING DEGREE ###{RESET}")
    degree_sim = DegreeSimulation(
        name="Degree",
        cost=cost,
        nodes_threshold=nodes_threshold,
        nodes_cost=nodes_cost,
    )
    _, degree_score = degree_sim.run(graph_name)
    epoch_scores = {epoch: degree_score for epoch in range(epochs)}
    results[degree_sim.name] = (epoch_scores, LINE_RED)
    log_important(text=f"Degree score: {degree_score}")

    log_important(text=f"\n{YELLOW}### STARTING DEGREE/COST ###{RESET}")
    degree_cost_sim = DegreeCostSimulation(
        name="Degree/Cost",
        cost=cost,
        nodes_threshold=nodes_threshold,
        nodes_cost=nodes_cost,
    )
    _, degree_cost_score = degree_cost_sim.run(graph_name)
    epoch_scores = {epoch: degree_cost_score for epoch in range(epochs)}
    results[degree_cost_sim.name] = (epoch_scores, LINE_GREEN)
    log_important(text=f"Degree/Cost score: {degree_cost_score}")

    log_important(text=f"\n{GREEN}### FINAL RESULTS ###{RESET}")
    log_important(text=f"- Genetic score: {genetic_score}")
    if do_genetic_degree:
        log_important(text=f"- Genetic Degree score: {genetic_degree_score}")
    log_important(text=f"- Genetic Degree/Cost score: {genetic_degree_cost_score}")
    log_important(text=f"- Degree score: {degree_score}")
    log_important(text=f"- Degree/Cost score: {degree_cost_score}")

    save_results(exp_name, graph_name, results)

    log_important(text=f"\n{BLUE}### ENDING EXPERIMENT {exp_name} ###{RESET}")


def save_results(exp_name, graph_name, simulation_results):
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
    plt.title(f"Score per Epoch", fontsize=12)
    plt.suptitle(f"Used graph: {graph_name}", fontsize=8)

    plt.xlabel("Epoch", fontsize=10)
    plt.xticks(epochs, rotation=90, ha="right", fontsize=9)

    plt.ylabel("Score", fontsize=10)
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


def setup_graph(graph_name):
    """
    Setup graph for the experiment.

    Args:
        graph_name (str): Name of the graph.
    """
    graph = graphs_by_name[graph_name]
    max_degree = get_max_degree(graph)
    log_important(text=f"\nUsing graph \"{graph_name}\" with max degree {max_degree}\n")
    print_graph_statistics(graph_name=graph_name)

    nodes_threshold = generate_nodes_threshold_with_node_degrees(graph, graph.nodes)
    nodes_cost = generate_nodes_cost(graph.nodes)
    log_important(text=f"Generated nodes threshold and cost for graph \"{graph_name}\"")

    return nodes_threshold, nodes_cost


def load_options(options: Dict[Any, Any]):
    """
    Load options for the experiment.

    Args:
        options (dict): Dictionary with options.
    """
    do_genetic_degree = False

    if options:
        do_genetic_degree = options.get("do_genetic_degree", False)

    return do_genetic_degree