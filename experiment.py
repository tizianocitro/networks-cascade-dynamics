from network import *
from utils import *
from heapq import *
import matplotlib.pyplot as plt
from datetime import datetime

def run_experiment(exp_name="experiment", epochs=10, graph_name="karate_club_graph", cost=0, n=20):
    # set for logging file
    os.environ["LOG_FILE_DIR"] = "logs"
    os.environ["LOG_FILE_PATH"] = exp_name

    log(text=f"\n{BLUE}### STARTING EXPERIMENT {exp_name} ###{RESET}\n")

    seed_sets, max_score, epoch_scores = run_simulation(epochs, graph_name, cost, n)
    save_results(seed_sets, max_score, epoch_scores, f"{exp_name}_permutation")

    seed_set, max_score = run_simulation_degree_based(graph_name, cost, n)
    epoch_scores = {epoch: max_score for epoch in range(epochs)}
    save_results([seed_set], max_score, epoch_scores, f"{exp_name}_degree")

    log(text=f"\n{BLUE}### ENDING EXPERIMENT {exp_name} ###{RESET}\n")


def run_simulation(epochs=10, graph_name="karate_club_graph", cost=0, n=20):
    graph = graphs_by_name[graph_name]
    max_degree = get_max_degree(graph)
    log(text=f"Using graph {graph_name} with max degree {max_degree}\n")
    # print_graph(graph, with_nodes=True, with_edges=False)

    nodes_threshold = generate_nodes_threshold_with_node_degrees(graph, graph.nodes)
    nodes_cost = generate_nodes_cost(graph.nodes)

    log(text=f"Generating {n} seed sets from the graph partition given a cost of {cost}\n")
    seed_sets = seed_sets_from_graph_permutation_given_cost(
        nodes=graph.nodes,
        nodes_cost_dict=nodes_cost,
        cost=cost,
        n=n,
    )

    max_score = 0
    epoch_scores = {0: 0}
    for epoch in range(epochs):
        log(text=f"\n{BLUE}### EPOCH {epoch} ###{RESET}\n")
        epoch_sets, epoch_score = run_epoch(
            graph=graph,
            seed_sets=seed_sets,
            nodes_cost=nodes_cost,
            nodes_threshold=nodes_threshold,
            cost=cost,
            n=n,
        )
        seed_sets = epoch_sets
        max_score = max(max_score, epoch_score)
        epoch_scores[epoch] = epoch_score

    log(text=f"\n{GREEN}### Final seed sets ###{RESET}\n")
    for i, s in enumerate(seed_sets):
        log(text=f"Final seed set {i} -> {s.seed_set}")

    log(text=f"\n{GREEN}### Max score ###{RESET}\n")
    log(text=f"Max score: {max_score}\n")
    log(text=f"\n{GREEN}### Epoch scores ###{RESET}\n")
    for epoch, score in epoch_scores.items():
        log(text=f"Epoch {epoch} score: {score}")

    return seed_sets, max_score, epoch_scores


def run_epoch(
    graph,
    seed_sets,
    nodes_cost,
    nodes_threshold,
    cost,
    n,
):
    max_score = 0

    # the max heap will store the seed set cost and the seed set index
    # so, if we want the top 5 seed sets, we can pop 5 times from the heap
    max_heap = []
    for i, s in enumerate(seed_sets):
        log(text="\n---------------------------------------------\n")
        log(text=f"{RED}### START Seed set {i}: {s} START ###{RESET}\n")
        s_cost = seed_set_cost(s.seed_set, nodes_cost)
        s_score = seed_set_score(s.seed_set)

        log(text=f"{YELLOW}Influencing nodes in the seed set {i} with initial cost {s_cost} and score {s_score}")
        print_seed_set(s)
        # start with a clean graph (without any influenced nodes)
        nodes_influenced = generate_nodes_influenced(graph.nodes)
        # influence the node in the seed set i
        nodes_influenced = influence_nodes(s.seed_set, nodes_influenced)
        # log(text=f"{RESET}Nodes influenced {i} at the start: {nodes_influenced}\n")

        # influence the nodes in the graph starting from the seed set i
        s_influenced, t = threshold_influence_diffusion(
            graph=graph,
            seed_set=s.seed_set,
            nodes_influenced=nodes_influenced,
            nodes_threshold=nodes_threshold,
        )
        s.seed_set = s_influenced

        log(text=f"{YELLOW}Influenced seed set {i} in {t} steps:")
        print_seed_set(s_influenced)
        # log(text=f"{RESET}Nodes influenced {i} at the end: {nodes_influenced}\n")

        s_influenced_cost = seed_set_cost(s_influenced, nodes_cost) - s_cost
        s_influenced_score = seed_set_score(s_influenced)
        log(text=f"{GREEN}Cost of influenced seed set {i}: {s_influenced_cost}{RESET}")
        log(text=f"{GREEN}Score of influenced seed set {i}: {s_influenced_score}\n{RESET}")

        max_score = max(max_score, s_influenced_score)

        heappush(max_heap, (-s_influenced_score, i))

        log(text=f"{RED}### ENDING Seed set {i} ENDING ###{RESET}")
        log(text="\n---------------------------------------------\n")
        log()

    log(text="\n---------------------------------------------\n")
    log(text=f"{RED}### Creating new population ###{RESET}\n")

    log(text=f"{RED}### Creating top 50% sets ###{RESET}\n")
    top_50_len = len(max_heap) // 2
    top_50_sets = []
    log(text=f"{GREEN}Top 50% ({top_50_len} sets) influencing seed sets:{RESET}")
    for _ in range(top_50_len):
        score, i = heappop(max_heap)
        log(text=f"- Seed set {i} with score {-score} -> current: {seed_sets[i].seed_set} | initial: {seed_sets[i].initial_seed_set}")
        top_50_sets.append(seed_sets[i])

    log(text=f"\n{RED}### Creating random sets ###{RESET}")
    random_len = (n - top_50_len) // 2
    random_sets = set()
    while len(random_sets) < random_len:
        random_set = seed_set_from_graph_permutation_given_cost(
            nodes=graph.nodes,
            nodes_cost_dict=nodes_cost,
            cost=cost,
        )
        if (
            random_set in random_sets or random_set in top_50_sets
        ):
            continue
        random_sets.add(random_set)

    log(text=f"\n{GREEN}Random ({random_len} sets) influencing seed sets:{RESET}")
    for i, s in enumerate(random_sets):
        log(text=f"- Seed set {i} -> {s.seed_set}")

    log(text=f"\n{GREEN}Combination ({random_len} sets) influencing seed sets:{RESET}\n")
    combined_sets = set()
    for i in range(0, len(top_50_sets), 2):
        s1 = top_50_sets[i]
        s2 = top_50_sets[i + 1]

        found = False
        iterations = cost * 2
        while not found and iterations > 0:
            combined_set = permutation_position_combine_seed_sets(
                s1=s1,
                s2=s2,
                nodes_cost_dict=nodes_cost,
                cost=cost,
                generation_opt=1,
            )
            if (
                combined_set not in combined_sets and \
                combined_set not in top_50_sets and \
                combined_set not in random_sets
            ):
                combined_sets.add(combined_set)
                found = True
                log(text=f"- Combining seed sets {i} and {i + 1} with resulting seed set {i} -> {combined_set.seed_set}")
            iterations -= 1

    log(text="\n---------------------------------------------\n")
    log(text=f"{RED}### Resulting new population ###{RESET}\n")

    seed_sets = top_50_sets + list(random_sets) + list(combined_sets)
    for i, s in enumerate(seed_sets):
        log(text=f"New seed set {i} -> {s.seed_set}")

    log(text="\n---------------------------------------------\n")

    log(text=f"{RED}### Epoch score ###{RESET}\n")
    log(text=f"Epoch score: {max_score}\n")

    return seed_sets, max_score


def run_simulation_degree_based(graph_name="karate_club_graph", cost=0, n=20):
    graph = graphs_by_name[graph_name]
    max_degree = get_max_degree(graph)
    log(text=f"Using graph {graph_name} with max degree {max_degree}\n")
    # print_graph(graph, with_nodes=True, with_edges=False)

    nodes_threshold = generate_nodes_threshold_with_node_degrees(graph, graph.nodes)
    nodes_cost = generate_nodes_cost(graph.nodes)

    log(text=f"Generating seed sets from cost ordered graph given a cost of {cost}\n")
    seed_set, _ = seed_set_from_degree_ordered_graph_given_cost(
        nodes=graph.nodes,
        degrees=graph.degree(),
        nodes_cost_dict=nodes_cost,
        cost=cost,
    )

    epoch_sets, epoch_score = run_epoch_degree_based(
        graph=graph,
        seed_sets=[seed_set], # only one seed set in this case
        nodes_cost=nodes_cost,
        nodes_threshold=nodes_threshold,
    )

    log(text=f"\n{GREEN}### Final degree seed set ###{RESET}\n")
    log(text=f"- {epoch_sets[0].seed_set}")

    log(text=f"\n{GREEN}### Max score ###{RESET}\n")
    log(text=f"Max score: {epoch_score}\n")

    return seed_set, epoch_score


def run_epoch_degree_based(
    graph,
    seed_sets,
    nodes_cost,
    nodes_threshold,
):
    max_score = 0

    for i, s in enumerate(seed_sets):
        log(text="\n---------------------------------------------\n")
        log(text=f"{RED}### START Seed set {i}: {s} START ###{RESET}\n")
        s_cost = seed_set_cost(s.seed_set, nodes_cost)
        s_score = seed_set_score(s.seed_set)

        log(text=f"{YELLOW}Influencing nodes in the seed set {i} with initial cost {s_cost} and score {s_score}")
        print_seed_set(s)
        # start with a clean graph (without any influenced nodes)
        nodes_influenced = generate_nodes_influenced(graph.nodes)
        # influence the node in the seed set i
        nodes_influenced = influence_nodes(s.seed_set, nodes_influenced)
        # log(text=f"{RESET}Nodes influenced {i} at the start: {nodes_influenced}\n")

        # influence the nodes in the graph starting from the seed set i
        s_influenced, t = threshold_influence_diffusion(
            graph=graph,
            seed_set=s.seed_set,
            nodes_influenced=nodes_influenced,
            nodes_threshold=nodes_threshold,
        )
        s.seed_set = s_influenced

        log(text=f"{YELLOW}Influenced seed set {i} in {t} steps:")
        print_seed_set(s_influenced)
        # log(text=f"{RESET}Nodes influenced {i} at the end: {nodes_influenced}\n")

        s_influenced_cost = seed_set_cost(s_influenced, nodes_cost) - s_cost
        s_influenced_score = seed_set_score(s_influenced)
        log(text=f"{GREEN}Cost of influenced seed set {i}: {s_influenced_cost}{RESET}")
        log(text=f"{GREEN}Score of influenced seed set {i}: {s_influenced_score}\n{RESET}")

        max_score = max(max_score, s_influenced_score)

    return seed_sets, max_score


def save_results(seed_sets, max_score, epoch_scores, exp_name):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    epochs = list(epoch_scores.keys())
    scores = list(epoch_scores.values())

    plt.figure(figsize=(8, 5))
    plt.plot(epochs, scores, marker="o", linestyle="-", color="b", label="Score")
    plt.title("Score in Each Epoch", fontsize=15)

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