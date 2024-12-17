import networkx as nx
from random import randint


graphs_by_name = {
    "karate_club_graph": nx.karate_club_graph(),
    "davis_southern_women_graph": nx.davis_southern_women_graph(),
    "florentine_families_graph": nx.florentine_families_graph(),
    "les_miserables_graph": nx.les_miserables_graph(),
    "erdos_renyi_graph": nx.erdos_renyi_graph(100, 0.1),
}


def line_graph(n=5):
    graph = nx.Graph()
    for i in range(1, n):
        graph.add_edge(i - 1, i)
    return graph


def networkx_graph_by_name(name):
    if name not in graphs_by_name:
        raise ValueError(f"Graph {name} not found.")
    return graphs_by_name[name]


def print_all_graphs_statistics():
    for name, graph in graphs_by_name.items():
        num_nodes = graph.number_of_nodes()
        num_edges = graph.number_of_edges()
        graph_density = nx.density(graph)

        print(f"{name} statistics:")
        print(f"Number of nodes: {num_nodes}")
        print(f"Number of edges: {num_edges}")
        print(f"Density: {graph_density:.4f}")

        print()


def print_graph(graph, with_nodes=True, with_edges=False):
    if with_nodes:
        print_nodes(graph.nodes(data=True))

    if with_edges:
        print("Edges:")
        for edge in graph.edges(data=True):
            print(edge)
        print()


def print_nodes(nodes):
    print("Nodes:")
    for node in nodes:
        print(node)
    print()


def generate_nodes_threshold(nodes, min=1, max=100, with_print=False):
    nodes_threshold = {node: randint(min, max) for node in nodes}

    if with_print:
        print("Nodes threshold:")
        for node in nodes:
            print(f"Node {node} has threshold {nodes_threshold[node]}")
        print()

    return nodes_threshold


def generate_nodes_threshold_with_node_degrees(graph, nodes, min=1, with_print=False):
    nodes_threshold = {node: randint(min, graph.degree(node)) for node in nodes}

    if with_print:
        print("Nodes threshold:")
        for node in nodes:
            print(f"Node {node} has threshold {nodes_threshold[node]}")
        print()

    return nodes_threshold


def generate_nodes_cost(nodes, min=1, max=100, with_print=False):
    nodes_cost = {node: randint(min, max) for node in nodes}

    if with_print:
        print("Nodes cost:")
        for node in nodes:
            print(f"Node {node} has cost {nodes_cost[node]}")
        print()

    return nodes_cost


def generate_nodes_influenced(nodes):
    return {node: False for node in nodes}


def get_max_degree(graph):
    degrees = [degree for _, degree in graph.degree()]
    return max(degrees) if degrees else 0
