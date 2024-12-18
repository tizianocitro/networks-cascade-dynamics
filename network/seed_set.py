from random import sample


def random_seed_set(graph, size):
    return sample(graph.nodes(), size)


def random_seed_set_with_data(graph, size, with_data=True):
    nodes = graph.nodes(data=with_data)
    if not with_data:
        # add empty data dict to each node
        nodes = [(node, {}) for node in nodes]

    return sample(nodes, size)


def seed_set_from_graph_partition_given_cost(graph, nodes_cost_dict, cost=0):
    nodes = set(graph.nodes())
    nodes_cost = sum(nodes_cost_dict.values())
    if nodes_cost < cost:
        raise ValueError("The given cost is greater than the sum of the nodes\' costs")
    if nodes_cost == cost:
        return list(graph.nodes())

    seed_set = set()
    seed_set_cost = 0

    while seed_set_cost < cost:
        # if no more nodes to sample, we break the loop and return the current seed set
        if not nodes:
            break

        sample_node = sample(nodes, 1)[0]
        sample_node_cost = nodes_cost_dict[sample_node]

        seed_set_with_sample_cost = seed_set_cost + sample_node_cost

        # we can add the node to the seed set only if it is not already in the seed set
        # and the seed set cost is less than the given cost (considering the new node)
        if sample_node not in seed_set and seed_set_with_sample_cost <= cost:
            seed_set.add(sample_node)
            seed_set_cost += nodes_cost_dict[sample_node]

        # either we add it or not (the cost does not fit our current need),
        # we remove it from the list of nodes because we do nt want to sample it again
        nodes.remove(sample_node)
        nodes_cost -= sample_node_cost

    return list(seed_set)


def seed_sets_from_graph_partition_given_cost(graph, nodes_cost_dict, cost=0, n=1):
    seed_sets = set()
    while len(seed_sets) < n:
        seed_set = seed_set_from_graph_partition_given_cost(graph, nodes_cost_dict, cost)
        seed_sets.add(tuple(seed_set))
    return [list(seed_set) for seed_set in seed_sets]


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


def seed_set_score(seed_set):
    return len(seed_set)


def print_seed_set(seed_set):
    print(f"Seed set\'s nodes: {seed_set} with size {len(seed_set)}")