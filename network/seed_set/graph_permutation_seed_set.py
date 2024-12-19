from random import shuffle
from utils import log
from heapq import heappush, heappop


class GraphPermutationSeedSet:
    def __init__(self, seed_set, permutation):
        # initial set will never change (used for comparison)
        self.initial_seed_set = seed_set
        self.seed_set = seed_set
        self.permutation = permutation


    def __len__(self):
        return len(self.seed_set)


    def __eq__(self, other):
        if not isinstance(other, GraphPermutationSeedSet):
            return False

        # compare the seed_set as sets (order doesn't matter)
        # compare the permutation as lists (order matters)
        return self.seed_set == other.seed_set


    def __hash__(self):
        # to use instances in sets or as dictionary keys, implement __hash__
        return hash(frozenset(self.seed_set))


    def __str__(self):
        return f"GraphPermutationSeedSet(seed_set={self.seed_set})"


def seed_set_from_graph_permutation_given_cost(nodes, nodes_cost_dict, cost=0):
    nodes = list(nodes)
    nodes_cost = sum(nodes_cost_dict.values())
    if nodes_cost < cost:
        raise ValueError("The given cost is greater than the sum of the nodes\' costs")
    if nodes_cost == cost:
        return GraphPermutationSeedSet(nodes, nodes)

    # permute the nodes in the graph
    shuffle(nodes)

    seed_set = set()
    seed_set_cost = 0

    ix = 0

    # while we have nodes to sample and the seed set cost is less than the given cost
    while seed_set_cost < cost and ix < len(nodes):
        sample_node = nodes[ix]
        sample_node_cost = nodes_cost_dict[sample_node]

        seed_set_with_sample_cost = seed_set_cost + sample_node_cost

        # we can add the node to the seed set only if it is not already in the seed set
        # and the seed set cost is less than the given cost (considering the new node)
        if sample_node not in seed_set and seed_set_with_sample_cost <= cost:
            seed_set.add(sample_node)
            seed_set_cost += nodes_cost_dict[sample_node]

        ix += 1

    return GraphPermutationSeedSet(list(seed_set), nodes)


def seed_sets_from_graph_permutation_given_cost(
    nodes,
    nodes_cost_dict,
    cost=0,
    n=1,
    with_print=False,
):
    seed_sets = set()

    tries = n * 5
    while len(seed_sets) < n:
        log(text=f"{tries} tries left to generate a seed set of cost {cost}", enabled=with_print)

        if tries < 1:
            log(text=f"No tries left to generate a seed set of cost {cost}, terminating the process", enabled=with_print)
            raise ValueError("Could not generate a seed set of the given cost")

        seed_set = seed_set_from_graph_permutation_given_cost(nodes, nodes_cost_dict, cost)
        seed_sets.add(seed_set)

        tries -= 1

    return list(seed_sets)


def position_combine_seed_sets(s1, s2, nodes_cost_dict, cost=0):
    max_heap = []
    s1_nodes_to_ixs = {node: ix for ix, node in enumerate(s1.permutation)}
    s2_nodes_to_ixs = {node: ix for ix, node in enumerate(s2.permutation)}

    for node in s1.permutation:
        s1_ix = s1_nodes_to_ixs[node]
        s2_ix = s2_nodes_to_ixs[node]
        node_score = (s1_ix + s2_ix) // 2
        heappush(max_heap, (-node_score, node))

    combined_set = []
    while max_heap:
        _, node = heappop(max_heap)
        combined_set.append(node)

    return seed_set_from_graph_permutation_given_cost(combined_set, nodes_cost_dict, cost)