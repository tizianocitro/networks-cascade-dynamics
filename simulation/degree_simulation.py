from typing import Any, Dict
from network import *
from utils import *

class DegreeSimulation:


    def __init__(
        self,
        name="Degree",
        cost=0,
        nodes_threshold: Dict[Any, int]=None,
        nodes_cost: Dict[Any, int]=None,
    ):
        self.name = name
        self.cost = cost
        self.nodes_threshold = nodes_threshold
        self.nodes_cost = nodes_cost


    def run(self, graph_name="karate_club_graph"):
        graph = graphs_by_name[graph_name]

        log(text=f"Generating seed sets from cost ordered graph given a cost of {self.cost}\n")
        seed_set, _ = seed_set_from_ordered_graph_given_cost(
            nodes=graph.nodes,
            nodes_cost_dict=self.nodes_cost,
            key_func=lambda node: graph.degree()[node],
            cost=self.cost,
        )

        epoch_sets, epoch_score = self.run_epoch(
            graph=graph,
            seed_sets=[seed_set], # only one seed set in this case
            nodes_cost=self.nodes_cost,
            nodes_threshold=self.nodes_threshold,
        )

        log(text=f"\n{GREEN}### Final degree seed set ###{RESET}\n")
        log(text=f"- {epoch_sets[0].seed_set}")

        # log(text=f"\n{GREEN}### Max score ###{RESET}\n")
        # log(text=f"Max score: {epoch_score}\n")

        return seed_set, epoch_score


    def run_epoch(
        self,
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


class DegreeCostSimulation:


    def __init__(
        self,
        name="Degree/Cost",
        cost=0,
        nodes_threshold: Dict[Any, int]=None,
        nodes_cost: Dict[Any, int]=None,
        starting_seed_set=None
    ):
        self.name = name
        self.cost = cost
        self.nodes_threshold = nodes_threshold
        self.nodes_cost = nodes_cost
        self.starting_seed_set = starting_seed_set


    def run(self, graph_name="karate_club_graph"):
        graph = graphs_by_name[graph_name]

        seed_set = self.starting_seed_set
        if seed_set:
            log(text=f"Starting seed set provided is {seed_set} with score {seed_set_score(seed_set.seed_set)}\n")
        if not self.starting_seed_set:
            log(text=f"No starting set provided: {self.starting_seed_set}")
            log(text=f"Then, generating seed set from (degree/cost) ordered graph given a cost of {self.cost}\n")
            seed_set, _ = seed_set_from_ordered_graph_given_cost(
                nodes=graph.nodes,
                nodes_cost_dict=self.nodes_cost,
                key_func=lambda node: (graph.degree()[node] // self.nodes_cost[node]),
                cost=self.cost,
            )

        epoch_sets, epoch_score = self.run_epoch(
            graph=graph,
            seed_sets=[seed_set], # only one seed set in this case
            nodes_cost=self.nodes_cost,
            nodes_threshold=self.nodes_threshold,
        )

        log(text=f"\n{GREEN}### Final degree seed set ###{RESET}\n")
        log(text=f"- {epoch_sets[0].seed_set}")

        # log(text=f"\n{GREEN}### Max score ###{RESET}\n")
        # log(text=f"Max score: {epoch_score}\n")

        return seed_set, epoch_score


    def run_epoch(
        self,
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