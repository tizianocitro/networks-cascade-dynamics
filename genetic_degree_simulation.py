from typing import Any, Dict
from network import *
from utils import *
from heapq import *


class GeneticDegreeSimulation:


    def __init__(
        self,
        name="Genetic Degree",
        cost=0,
        n=20,
        epochs=10,
        a_range=None,
        nodes_threshold: Dict[Any, int]=None,
        nodes_cost: Dict[Any, int]=None,
        with_first_total=True,
    ):
        self.name = name
        self.cost = cost
        self.n = n
        self.epochs = epochs
        self.a_range = a_range if a_range else [1, 1]
        self.nodes_threshold = nodes_threshold
        self.nodes_cost = nodes_cost
        self.with_first_total = with_first_total


    def run(self, graph_name="karate_club_graph"):
        graph = graphs_by_name[graph_name]

        log(text=f"Generating {self.n} seed sets from degree given a cost of {self.cost}\n")
        seed_sets = seed_sets_from_degree_graph_given_cost(
            nodes=graph.nodes,
            nodes_cost_dict=self.nodes_cost,
            degrees=graph.degree(),
            cost=self.cost,
            n=self.n,
            a_range=self.a_range,
            with_print=True,
        )

        max_score = 0
        epoch_scores = {0: 0}
        for epoch in range(self.epochs):
            log(text=f"\n{BLUE}### EPOCH {epoch} ###{RESET}\n")
            epoch_sets, epoch_score = self.run_epoch(graph=graph, seed_sets=seed_sets)
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
        log()

        return seed_sets, max_score, epoch_scores


    def run_epoch(self, graph, seed_sets):
        max_score = 0

        # the max heap will store the seed set cost and the seed set index
        # so, if we want the top 5 seed sets, we can pop 5 times from the heap
        max_heap = []
        for i, s in enumerate(seed_sets):
            log(text="\n---------------------------------------------\n")
            log(text=f"{RED}### START Seed set {i}: {s} START ###{RESET}\n")
            s_cost = seed_set_cost(s.seed_set, self.nodes_cost)
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
                nodes_threshold=self.nodes_threshold,
            )
            s.seed_set = s_influenced

            log(text=f"{YELLOW}Influenced seed set {i} in {t} steps:")
            print_seed_set(s_influenced)
            # log(text=f"{RESET}Nodes influenced {i} at the end: {nodes_influenced}\n")

            s_influenced_cost = seed_set_cost(s_influenced, self.nodes_cost) - s_cost
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
        random_len = (self.n - top_50_len) // 2
        random_sets = set()
        while len(random_sets) < random_len:
            random_set = seed_set_from_degree_graph_given_cost(
                nodes=graph.nodes,
                nodes_cost_dict=self.nodes_cost,
                degrees=graph.degree(),
                cost=self.cost,
                a_range=self.a_range,
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
            iterations = self.cost * 2
            while not found and iterations > 0:
                combined_set = permutation_position_combine_seed_sets(
                    s1=s1,
                    s2=s2,
                    nodes_cost_dict=self.nodes_cost,
                    degrees=graph.degree(),
                    a_range=self.a_range,
                    cost=self.cost,
                    generation_opt=4,
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


class GeneticDegreeCostSimulation:


    def __init__(
        self,
        name="Genetic Degree/Cost",
        cost=0,
        n=20,
        epochs=10,
        a_range=None,
        b_range=None,
        nodes_threshold: Dict[Any, int]=None,
        nodes_cost: Dict[Any, int]=None,
        with_first_total=True,
    ):
        self.name = name
        self.cost = cost
        self.n = n
        self.epochs = epochs
        self.a_range = a_range if a_range else [1, 1]
        self.b_range = b_range if b_range else [1, 1]
        self.nodes_threshold = nodes_threshold
        self.nodes_cost = nodes_cost
        self.with_first_total = with_first_total


    def run(self, graph_name="karate_club_graph"):
        graph = graphs_by_name[graph_name]

        log(text=f"Generating {self.n} seed sets from degree/cost given a cost of {self.cost}\n")
        seed_sets = seed_sets_from_degreecost_graph_given_cost(
            nodes=graph.nodes,
            nodes_cost_dict=self.nodes_cost,
            degrees=graph.degree(),
            cost=self.cost,
            n=self.n,
            a_range=self.a_range,
            b_range=self.b_range,
            with_first_total=self.with_first_total,
        )

        max_score = 0
        epoch_scores = {0: 0}
        for epoch in range(self.epochs):
            log(text=f"\n{BLUE}### EPOCH {epoch} ###{RESET}\n")
            epoch_sets, epoch_score = self.run_epoch(graph=graph, seed_sets=seed_sets)
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
        log()

        return seed_sets, max_score, epoch_scores


    def run_epoch(self, graph, seed_sets):
        max_score = 0

        # the max heap will store the seed set cost and the seed set index
        # so, if we want the top 5 seed sets, we can pop 5 times from the heap
        max_heap = []
        for i, s in enumerate(seed_sets):
            log(text="\n---------------------------------------------\n")
            log(text=f"{RED}### START Seed set {i}: {s} START ###{RESET}\n")
            s_cost = seed_set_cost(s.seed_set, self.nodes_cost)
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
                nodes_threshold=self.nodes_threshold,
            )
            s.seed_set = s_influenced

            log(text=f"{YELLOW}Influenced seed set {i} in {t} steps:")
            print_seed_set(s_influenced)
            # log(text=f"{RESET}Nodes influenced {i} at the end: {nodes_influenced}\n")

            s_influenced_cost = seed_set_cost(s_influenced, self.nodes_cost) - s_cost
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
        random_len = (self.n - top_50_len) // 2
        random_sets = set()
        while len(random_sets) < random_len:
            random_set = seed_set_from_degreecost_graph_given_cost(
                nodes=graph.nodes,
                nodes_cost_dict=self.nodes_cost,
                degrees=graph.degree(),
                cost=self.cost,
                a_range=self.a_range,
                b_range=self.b_range,
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
            iterations = self.cost * 2
            while not found and iterations > 0:
                combined_set = permutation_position_combine_seed_sets(
                    s1=s1,
                    s2=s2,
                    nodes_cost_dict=self.nodes_cost,
                    degrees=graph.degree(),
                    a_range=self.a_range,
                    b_range=self.b_range,
                    cost=self.cost,
                    generation_opt=3,
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