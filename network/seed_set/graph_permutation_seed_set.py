from random import shuffle, uniform
from heapq import heappush, heappop
from utils import log


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


def seed_set_from_ordered_graph_given_cost(
    nodes,
    nodes_cost_dict,
    key_func,
    cost=0,
    exclude_ixs=None,
):
    nodes = list(nodes)
    nodes_cost = sum(nodes_cost_dict.values())
    if nodes_cost < cost:
        raise ValueError("The given cost is greater than the sum of the nodes\' costs")
    if nodes_cost == cost:
        return GraphPermutationSeedSet(nodes, nodes)

    nodes.sort(key=key_func, reverse=True)
    seed_set = set()
    seed_set_cost = 0

    ix = 0
    exclude_ixs = exclude_ixs if exclude_ixs else []
    excluded_ixs = []

    # while we have nodes to sample and the seed set cost is less than the given cost
    while seed_set_cost < cost and ix < len(nodes):
        log(text=f"Processing node at ix: {ix}, exclude_ixs: {exclude_ixs}", enabled=False)
        if ix in exclude_ixs:
            ix += 1
            continue

        sample_node = nodes[ix]
        sample_node_cost = nodes_cost_dict[sample_node]

        seed_set_with_sample_cost = seed_set_cost + sample_node_cost

        # we can add the node to the seed set only if it is not already in the seed set
        # and the seed set cost is less than the given cost (considering the new node)
        if sample_node not in seed_set and seed_set_with_sample_cost <= cost:
            seed_set.add(sample_node)
            seed_set_cost += nodes_cost_dict[sample_node]
            excluded_ixs.append(ix)

        ix += 1

    return GraphPermutationSeedSet(list(seed_set), nodes), excluded_ixs


def seed_set_from_degree_graph_given_cost(
    nodes,
    nodes_cost_dict,
    degrees,
    cost=0,
    a_range=None,
    with_print=False,
):
    a = uniform(a_range[0], a_range[1])
    log(text=f"Generating seed set from degree graph given a cost of {cost} and a={a}", enabled=with_print)

    graph_permutation_seed_set, _ = seed_set_from_ordered_graph_given_cost(
        nodes=nodes,
        nodes_cost_dict=nodes_cost_dict,
        key_func=lambda node: (degrees[node] * a),
        cost=cost,
    )

    return graph_permutation_seed_set


def seed_sets_from_degree_graph_given_cost(
    nodes,
    nodes_cost_dict,
    degrees,
    cost=0,
    n=1,
    a_range=None,
    with_print=False,
):
    seed_sets = set()

    tries = n * 5
    while len(seed_sets) < n:
        log(text=f"{tries} tries left to generate a seed set of cost {cost}", enabled=with_print)

        if tries < 1:
            log(text=f"No tries left to generate a seed set of cost {cost}, terminating the process", enabled=with_print)
            raise ValueError("Could not generate a seed set of the given cost")

        graph_permutation_seed_set = seed_set_from_degree_graph_given_cost(
            nodes=nodes,
            nodes_cost_dict=nodes_cost_dict,
            degrees=degrees,
            cost=cost,
            a_range=a_range,
            with_print=with_print,
        )

        seed_sets.add(graph_permutation_seed_set)
        log(text=f"lenght of seed sets: {len(seed_sets)}", enabled=with_print)

        tries -= 1

    return list(seed_sets)


def seed_set_from_degreecost_graph_given_cost(
    nodes,
    nodes_cost_dict,
    degrees,
    cost=0,
    a_range=None,
    b_range=None,
    ab_total=False,
):
    a = uniform(a_range[0], a_range[1])
    b = uniform(b_range[0], b_range[1])

    # most of the times, including the the degree / cost
    # without influencing the result value, improves performance
    if ab_total:
        a = b = 1

    graph_permutation_seed_set, _ = seed_set_from_ordered_graph_given_cost(
        nodes=nodes,
        nodes_cost_dict=nodes_cost_dict,
        key_func=lambda node: ((degrees[node] * a) // (nodes_cost_dict[node] * b)),
        cost=cost,
    )

    return graph_permutation_seed_set


def seed_sets_from_degreecost_graph_given_cost(
    nodes,
    nodes_cost_dict,
    degrees,
    cost=0,
    n=1,
    a_range=None,
    b_range=None,
    with_first_total=True,
    with_print=False,
):
    seed_sets = set()

    ix = 0

    tries = n * 5
    while len(seed_sets) < n:
        a = uniform(a_range[0], a_range[1])
        b = uniform(b_range[0], b_range[1])

        log(text=f"{tries} tries left to generate a seed set of cost {cost} with a={a} and b={b}", enabled=with_print)

        if tries < 1:
            log(text=f"No tries left to generate a seed set of cost {cost}, terminating the process", enabled=with_print)
            raise ValueError(f"Could not generate a seed set of the given cost, max is {len(seed_sets)}")

        graph_permutation_seed_set = seed_set_from_degreecost_graph_given_cost(
            nodes=nodes,
            nodes_cost_dict=nodes_cost_dict,
            degrees=degrees,
            cost=cost,
            a_range=a_range,
            b_range=b_range,
            ab_total= with_first_total and ix == 0,
        )

        seed_sets.add(graph_permutation_seed_set)
        log(text=f"lenght of seed sets: {len(seed_sets)}", enabled=with_print)

        tries -= 1
        ix += 1

    return list(seed_sets)


def seed_sets_from_degree_ordered_graph_given_cost(
    nodes,
    degrees,
    nodes_cost_dict,
    cost=0,
    n=1,
    with_print=True,
):
    seed_sets = set()

    exclude_ixs = []
    tries = n * 5
    while len(seed_sets) < n:
        log(text=f"{tries} tries left to generate a seed set of cost {cost}", enabled=with_print)

        if tries < 1:
            log(text=f"No tries left to generate a seed set of cost {cost}, terminating the procees by excluding {excluded_ixs}", enabled=with_print)
            log(text=f"Generated {len(seed_sets)} seed sets", enabled=with_print)
            for seed_set in seed_sets:
                log(text=f"- Generated seed set: {seed_set.seed_set}", enabled=with_print)
            raise ValueError("Could not generate a seed set of the given cost")

        seed_set, excluded_ixs = seed_set_from_ordered_graph_given_cost(
            nodes=nodes,
            nodes_cost_dict=nodes_cost_dict,
            key_func=lambda node: degrees[node],
            cost=cost,
            exclude_ixs=exclude_ixs,
        )

        seed_sets.add(seed_set)
        exclude_ixs.extend(excluded_ixs)

        tries -= 1

    return list(seed_sets), exclude_ixs


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


def position_combine_seed_sets(s1, s2):
    max_heap = []
    s1_nodes_to_ixs = {node: ix for ix, node in enumerate(s1.seed_set)}
    s2_nodes_to_ixs = {node: ix for ix, node in enumerate(s2.seed_set)}

    for node in s1_nodes_to_ixs:
        s1_ix = s1_nodes_to_ixs[node]
        s2_ix = s2_nodes_to_ixs.get(node, -1)
        node_score = (s1_ix + s2_ix) // 2
        heappush(max_heap, (-node_score, node))

    for node in s2_nodes_to_ixs:
        if node in s1_nodes_to_ixs:
            continue
        s1_ix = s1_nodes_to_ixs.get(node, -1)
        s2_ix = s2_nodes_to_ixs[node]
        node_score = (s1_ix + s2_ix) // 2
        heappush(max_heap, (-node_score, node))

    combined_set = []
    while max_heap:
        _, node = heappop(max_heap)
        combined_set.append(node)

    return GraphPermutationSeedSet(combined_set, position_combine_permutation(s1, s2))


def permutation_position_combine_seed_sets(
    s1,
    s2,
    degrees=None,
    exclude_ixs=None,
    nodes_cost_dict=None,
    a_range=None,
    b_range=None,
    cost=0,
    generation_opt=1,
):
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

    if generation_opt == 1:
        return seed_set_from_graph_permutation_given_cost(combined_set, nodes_cost_dict, cost)
    elif generation_opt == 2:
        return seed_set_from_ordered_graph_given_cost(
            combined_set,
            nodes_cost_dict,
            key_func=lambda node: degrees[node],
            cost=cost,
            exclude_ixs=exclude_ixs,
        )
    elif generation_opt == 3:
        return seed_set_from_degreecost_graph_given_cost(
            combined_set,
            nodes_cost_dict,
            degrees=degrees,
            cost=cost,
            a_range=a_range,
            b_range=b_range,
        )


def position_combine_permutation(s1, s2):
    max_heap = []
    s1_nodes_to_ixs = {node: ix for ix, node in enumerate(s1.permutation)}
    s2_nodes_to_ixs = {node: ix for ix, node in enumerate(s2.permutation)}

    for node in s1.permutation:
        s1_ix = s1_nodes_to_ixs[node]
        s2_ix = s2_nodes_to_ixs[node]
        node_score = (s1_ix + s2_ix) // 2
        heappush(max_heap, (-node_score, node))

    combined_permutation = []
    while max_heap:
        _, node = heappop(max_heap)
        combined_permutation.append(node)

    return combined_permutation