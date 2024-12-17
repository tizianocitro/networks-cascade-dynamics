from graph import *
from seed_set import *
from network import *


if __name__ == "__main__":
    graph_name = "karate_club_graph"

    graph = graphs_by_name[graph_name]
    max_degree = get_max_degree(graph)
    # print_graph(graph)
    print(f"Using graph {graph_name} with max degree {max_degree}\n")

    nodes_threshold = generate_nodes_threshold_with_node_degrees(graph, graph.nodes)
    nodes_cost = generate_nodes_cost(graph.nodes)
    nodes_influenced = generate_nodes_influenced(graph.nodes)

    S = random_seed_set(graph, 5)
    print("Starting seed set:")
    print_seed_set(S)
    S_cost = seed_set_cost(S, nodes_cost)
    print(f"Cost of seed set: {S_cost}\n")

    print("Influencing nodes in the seed set")
    nodes_influenced = influence_nodes(S, nodes_influenced)
    print(f"Nodes influenced: {nodes_influenced}\n")

    S_influenced, t = threshold_influence_diffusion(graph, S, nodes_influenced, nodes_threshold)
    print(f"Influenced seed set in {t} steps:")
    print_seed_set(S_influenced)
    S_influenced_cost = seed_set_cost(S_influenced, nodes_cost)
    print(f"Cost of influenced seed set: {S_influenced_cost}\n")
    print(f"Nodes influenced: {nodes_influenced}\n")