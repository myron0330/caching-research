import random
import networkx as nx
from networkx.generators.classic import empty_graph
from collections import defaultdict


class Network(nx.Graph):

    def __init__(self, layout=None, *args, **kwargs):
        super(Network, self).__init__(*args, **kwargs)
        self.layout = layout

    @property
    def node_number(self):
        """
        Node number.
        """
        return self.number_of_nodes()

    @property
    def nodes_info(self):
        """
        Nodes info.
        """
        return self.nodes()

    @property
    def neighbors_info(self):
        """
        Neighbors info
        """
        info = dict()
        for node in self.nodes_info:
            info[node] = self.neighbors(node)
        return info

    @property
    def positions_info(self):
        """
        Positions info
        """
        return self.layout

    @classmethod
    def random_regular_graph(cls, degree, number, seed=None, layout='spring_layout', layout_parameters=None):
        """
        Generate a random regular graph.

        Args:
            degree(int): The degree of each node.
            number(int): The number of nodes. The value of ``number * degree`` must be even.
            seed(hashable object): The seed for random number generator.
            layout(string): layout functions.
            layout_parameters(dict): layout parameters
        """
        if (number * degree) % 2 != 0:
            raise nx.NetworkXError("n * d must be even")

        if not 0 <= degree < number:
            raise nx.NetworkXError("the 0 <= d < n inequality must be satisfied")

        if degree == 0:
            return empty_graph(number)

        if seed is not None:
            random.seed(seed)

        def _suitable(edges, potential_edges):
            # Helper subroutine to check if there are suitable edges remaining
            # If False, the generation of the graph has failed
            if not potential_edges:
                return True
            for s1 in potential_edges:
                for s2 in potential_edges:
                    if s1 == s2:
                        # Only need to consider s1-s2 pair one time
                        break
                    if s1 > s2:
                        s1, s2 = s2, s1
                    if (s1, s2) not in edges:
                        return True
            return False

        def _try_creation():
            # Attempt to create an edge set
            edges = set()
            stubs = list(range(number)) * degree

            while stubs:
                potential_edges = defaultdict(lambda: 0)
                random.shuffle(stubs)
                stubiter = iter(stubs)
                for s1, s2 in zip(stubiter, stubiter):
                    if s1 > s2:
                        s1, s2 = s2, s1
                    if s1 != s2 and ((s1, s2) not in edges):
                        edges.add((s1, s2))
                    else:
                        potential_edges[s1] += 1
                        potential_edges[s2] += 1

                if not _suitable(edges, potential_edges):
                    return None  # failed to find suitable edge set

                stubs = [node for node, potential in potential_edges.items()
                         for _ in range(potential)]
            return edges

        edges = _try_creation()
        while edges is None:
            edges = _try_creation()

        graph = cls()
        graph.name = "random_regular_graph(%s, %s)" % (degree, number)
        graph.add_edges_from(edges)
        layout_parameters = layout_parameters or dict()
        graph.layout = getattr(nx, layout)(graph, **layout_parameters)
        return graph
