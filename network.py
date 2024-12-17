def threshold_influence_diffusion(graph, seed_set, nodes_influenced, nodes_threshold, with_print=False):
    influence_set = set(seed_set)
    t = 0

    while True:
        # calculate the next influenced set
        new_influence_set = set(influence_set)

        for node in graph.nodes:
            if node not in influence_set:
                neighbors = graph.neighbors(node)

                # count node's neighbors that are already in the influence set
                num_influenced_neighbors = sum(1 for neighbor in neighbors if neighbor in influence_set)
                if num_influenced_neighbors >= nodes_threshold[node]:
                    # mark nodes as influenced
                    nodes_influenced[node] = True
                    new_influence_set.add(node)

        # check for stabilization (no new influenced nodes in this iteration)
        if new_influence_set == influence_set:
            break

        # update influence set and increment time
        influence_set = new_influence_set
        t += 1

        if with_print:
            print(f"At step {t}, influence set is {influence_set}")

    return list(influence_set), t


def influence_nodes(seed_set, nodes_influenced):
    for node in seed_set:
        nodes_influenced[node] = True
    return nodes_influenced