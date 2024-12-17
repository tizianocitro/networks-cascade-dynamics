from random import sample


def random_seed_set(graph, size):
    return sample(graph.nodes(), size)


def random_seed_set_with_data(graph, size, with_data=True):
    nodes = graph.nodes(data=with_data)
    if not with_data:
        # add empty data dict to each node
        nodes = [(node, {}) for node in nodes]

    return sample(nodes, size)


def seed_set_cost(seed_set, nodes_cost, with_print=False):
    if with_print:
        print("Nodes cost:")
        for node_id, _ in seed_set:
            print(f"Node {node_id} has cost {nodes_cost[node_id]}")

    return sum(nodes_cost[node_id] for node_id in seed_set)


def seed_set_cost_with_data(seed_set, nodes_cost, with_print=False):
    if with_print:
        print("Nodes cost:")
        for node_id, _ in seed_set:
            print(f"Node {node_id} has cost {nodes_cost[node_id]}")

    return sum(nodes_cost[node_id] for node_id, _ in seed_set)


def print_seed_set(seed_set):
    print(f"Seed set\'s nodes: {seed_set} with size {len(seed_set)}")