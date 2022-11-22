"""
COMP 614
Provided code for homework 6. Includes the Stack, Queue, and DiGraph classes.
"""


class Stack:
    """
    A representation of a LIFO stack.
    """

    def __init__(self):
        """
        Constructs a new empty stack.
        """
        self._items = []

    def __len__(self):
        """
        Returns an integer representing the number of items in the stack.
        """
        return len(self._items)

    def __str__(self):
        """
        Returns a string representation of the stack.
        """
        return str(self._items)

    def push(self, item):
        """
        Adds the given item to the stack.
        """
        self._items.append(item)

    def pop(self):
        """
        Removes and returns the most recently added item from the stack. 
        Assumes that there is at least one element in the stack.
        """
        return self._items.pop()

    def clear(self):
        """
        Removes all items from the queue.
        """
        self._items = []


class Queue:
    """
    A representation of a FIFO queue.
    """

    def __init__(self):
        """
        Constructs a new empty queue.
        """
        self._items = []

    def __len__(self):
        """
        Returns an integer representing the number of items in the queue.
        """
        return len(self._items)

    def __str__(self):
        """
        Returns a string representation of the queue.
        """
        return str(self._items)

    def push(self, item):
        """
        Adds the given item to the queue.
        """
        self._items.append(item)

    def pop(self):
        """
        Removes and returns the least recently added item from the queue. 
        Assumes that there is at least one element in the queue.
        """
        return self._items.pop(0)

    def clear(self):
        """
        Removes all items from the queue.
        """
        self._items = []


class DiGraph:
    """
    A representation of a directed graph.
    """

    def __init__(self):
        """
        Constructs a new empty graph.
        """
        self._graph = {}

    def nodes(self):
        """
        Returns a set containing all of the nodes in the graph.
        """
        return set(self._graph.keys())

    def get_neighbors(self, node):
        """
        Given a particular node, returns a set containing all neighbors of that
        node in the graph. This will only include neighbors that are connected
        to one of node's *outbound* edges.
        """
        return self._graph[node]

    def add_node(self, node):
        """
        Adds the given node to the graph.
        """
        if node not in self._graph:
            self._graph[node] = set([])

    def add_edge(self, node1, node2):
        """
        Adds an edge from node1 to node2.
        """
        self.add_node(node1)
        self.add_node(node2)
        self._graph[node1].add(node2)

    def copy(self):
        """
        Returns a deep copy of this graph.
        """
        new_graph = DiGraph()

        # Copy all edges, which will also copy the nodes
        for node, nbrs in self._graph.items():
            for nbr in nbrs:
                new_graph.add_edge(node, nbr)

        return new_graph

    def __eq__(self, other):
        """
        Returns True if self and other are equivalent DiGraph objects; returns 
        False otherwise.
        """
        # Check that other has the correct type
        if type(other) != DiGraph:
            return False

        # Check that other has the same nodes as self
        elif other.nodes() != self.nodes():
            return False

        # Check that other has the same edges as self
        for node, nbrs in self._graph.items():
            if other.get_neighbors(node) != nbrs:
                return False

        # Passed all equivalence checks
        return True


def file_to_graph(filename):
    """
    Given the name of a file, reads the contents of that file and uses it to
    build a graph. Assumes that each line will contain the name of a single node. 
    If the line does not start with a tab, it contains the name of a new node to
    be added to the graph. If the line starts with a tab, it contains the name of
    a node that is a neighbor of the most recently added node. 

    For example, imagine that the file is structured as follows:
    node1
        node2
        node3
    node2
        node1
    node3

    In this case, the graph has three nodes: node1, node2, and node3. node1 has 
    outbound edges to node2 and node3. node2 has an outbound edge to node1. node3
    has no outbound edges.
    """
    # Read the lines out of the specified file
    graph_file = open(filename, "r")
    lines = graph_file.readlines()

    # Create a new graph
    graph = DiGraph()

    # Populate the graph based on the data in the file
    node = None
    for line in lines:
        if not line.strip():
            continue

        if line.startswith("\t"):
            nbr = line.strip()
            graph.add_edge(node, nbr)
        else:
            node = line.strip()
            graph.add_node(node)

    return graph