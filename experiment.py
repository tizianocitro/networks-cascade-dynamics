from network import *
from utils import *
from heapq import *


def run_experiment(exp_name="experiment"):
    print(f"\n{BLUE}### STARTING EXPERIMENT {exp_name} ###{RESET}\n")

    run_simulation()

    # save_results(results)

    print(f"\n{BLUE}### ENDING EXPERIMENT {exp_name} ###{RESET}\n")


def run_simulation():
    graph_name = "karate_club_graph"

    graph = graphs_by_name[graph_name]
    max_degree = get_max_degree(graph)
    # print_graph(graph)
    print(f"Using graph {graph_name} with max degree {max_degree}\n")

    nodes_threshold = generate_nodes_threshold_with_node_degrees(graph, graph.nodes)
    nodes_cost = generate_nodes_cost(graph.nodes)

    n = 20
    cost = 50
    print(f"Generating {n} seed sets from the graph partition given a cost of {cost}\n")
    seed_sets = seed_sets_from_graph_partition_given_cost(graph, nodes_cost_dict=nodes_cost, cost=cost, n=n)

    # the max heap will store the seed set cost and the seed set index
    # so, if we want the top 5 seed sets, we can pop 5 times from the heap
    max_heap = []
    for i, s in enumerate(seed_sets):
        print("\n---------------------------------------------\n")
        print(f"{RED}### START Seed set {i}: {s} START ###{RESET}\n")
        s_cost = seed_set_cost(s, nodes_cost)
        s_score = seed_set_score(s)

        print(f"{YELLOW}Influencing nodes in the seed set {i} with initial cost {s_cost} and score {s_score}")
        print_seed_set(s)
        # start with a clean grap (without any influenced nodes)
        nodes_influenced = generate_nodes_influenced(graph.nodes)
        # influence the node in the seed set i
        nodes_influenced = influence_nodes(s, nodes_influenced)
        print(f"{RESET}Nodes influenced {i} at the start: {nodes_influenced}\n")

        # influence the nodes in the graph starting from the seed set i
        s_influenced, t = threshold_influence_diffusion(graph, s, nodes_influenced, nodes_threshold)

        print(f"{YELLOW}Influenced seed set {i} in {t} steps:")
        print_seed_set(s_influenced)
        print(f"{RESET}Nodes influenced {i} at the end: {nodes_influenced}\n")

        s_influenced_cost = seed_set_cost(s_influenced, nodes_cost) - s_cost
        s_influenced_score = seed_set_score(s_influenced)
        print(f"{GREEN}Cost of influenced seed set {i}: {s_influenced_cost}{RESET}")
        print(f"{GREEN}Score of influenced seed set {i}: {s_influenced_score}\n{RESET}")

        heappush(max_heap, (-s_influenced_score, i))

        print(f"{RED}### ENDING Seed set {i} ENDING ###{RESET}")
        print("\n---------------------------------------------\n")
        print()

    print(f"{GREEN}Top influencing seed set:{RESET}")
    while max_heap:
        score, i = heappop(max_heap)
        print(f"- Seed set {i} ({seed_sets[i]}) with score {-score}")