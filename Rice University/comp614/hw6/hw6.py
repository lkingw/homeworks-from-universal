"""
COMP 614
Homework 6: DFS + PageRank
"""

import comp614_module6


def bfs_dfs(graph, start_node, rac_class):
    """
    Performs a breadth-first search on graph starting at the given node.
    Returns a two-element tuple containing a dictionary mapping each visited
    node to its distance from the start node and a dictionary mapping each
    visited node to its parent node.
    """
    if rac_class == comp614_module6.Queue:

        # Initialize all data structures
        queue = comp614_module6.Queue()
        distance = {}
        parent = {}

        # Initialize distance and parents; no nodes have been visited yet
        for node in graph.nodes():
            distance[node] = float("inf")
            parent[node] = None

        # Initialize start node's distanceance to 0
        distance[start_node] = 0
        queue.push(start_node)

        # Continue as long as there are new reachable nodes
        while queue:
            node = queue.pop()
            nbrs = graph.get_neighbors(node)

            for nbr in nbrs:
                # Only update neighbors that have not been seen before
                if distance[nbr] == float('inf'):
                    distance[nbr] = distance[node] + 1
                    parent[nbr] = node
                    queue.push(nbr)

    else:

        # Initialize all data structures
        stack = comp614_module6.Stack()
        distance = {}
        parent = {}

        # Initialize distance and parents; no nodes have been visited yet
        for node in graph.nodes():
            distance[node] = float("inf")
            parent[node] = None

        # Initialize start node's distance to 0
        distance[start_node] = 0
        stack.push(start_node)

        # Continue as long as there are new reachable nodes
        while stack:
            node = stack.pop()
            nbrs = graph.get_neighbors(node)

            for nbr in nbrs:
                # Only update neighbors that have not been visited before
                if distance[nbr] == float('inf'):
                    distance[nbr] = distance[node] + 1
                    parent[nbr] = node
                    stack.push(nbr)

    return parent


def recursive_dfs(graph, start_node, parent):
    """
    Given a graph, a start node from which to search, and a mapping of nodes to
    their parents, performs a recursive depth-first search on graph from the 
    given start node, populating the parents mapping as it goes.
    """
    parent_first = bfs_dfs(graph, start_node, rac_class=comp614_module6.Stack())
    for key, val in parent_first.items():
        parent[key] = val


def get_inbound_nbrs(graph):
    """
    Given a directed graph, returns a mapping of each node n in the graph to
    the set of nodes that have edges into n.
    """
    # Initialize all data structures
    neighbors = {}

    queue = comp614_module6.Queue()
    for node in graph.nodes():
        queue.push(node)
        neighbors[node] = set()

    # Initialize distances and parents; no nodes have been visited yet
    for node in graph.nodes():
        nbrs = graph.get_neighbors(node)
        for nbr in nbrs:
            if nbr in neighbors:
                neighbors[nbr] = {node}
            elif node not in neighbors[nbr] and nbr in neighbors:
                neighbors[nbr].add(node)

    # account for nodes with no inbound edges
    return neighbors


def remove_sink_nodes(graph):
    """
    Given a directed graph, returns a new copy of the graph where every node that
    was a sink node in the original graph now has an outbound edge linking it to 
    every other node in the graph (excluding itself).
    """
    graph_clone = graph.copy()
    all_nodes = set()

    for node in graph_clone.nodes():
        all_nodes.add(node)

    for node in graph_clone.nodes():
        if len(graph.get_neighbors(node)) == 0:
            for node_n in all_nodes:
                if node_n != node:
                    graph_clone.add_edge(node, node_n)

    return graph_clone


def page_rank(graph, damping):
    """
    Given a directed graph and a damping factor, implements the PageRank algorithm
    -- continuing until delta is less than 10^-8 -- and returns a dictionary that 
    maps each node in the graph to its page rank.
    """
    nodes_copy = remove_sink_nodes(graph)

    # output dictionary of page ranks
    epsilon = 10e-8
    nodes = {}
    node_list = nodes_copy.nodes()

    # initial rank
    for node_n in node_list:
        nodes[node_n] = 1 / len(node_list)

    # get all the inbound neighbors of each node
    # inbound_nbrs = get_inbound_nbrs(nodes_copy)

    # find the sets of outbound edges for each of the nodes
    outbound_nbrs = {}
    for n_b in nodes_copy.nodes():
        outbound_nbrs[n_b] = nodes_copy.get_neighbors(n_b)

    # delta = sum(nodes.values())
    delta = float("inf")
    while delta > epsilon:
        # create a new nodes dict to hold previous ranks
        copy_nodes = nodes.copy()

        for node, _ in nodes.items():
            num_ob_nodes = {}
            # set_ib_neighbors = inbound_nbrs[node]
            # set page rank to 0 if node has no inbound neighbors
            if len(get_inbound_nbrs(nodes_copy)[node]) == 0:
                nodes[node] = 0
            else:
                # find the number of outbound nodes for the current inbound node
                for ib_nbr in get_inbound_nbrs(nodes_copy)[node]:
                    num_ob_nodes[ib_nbr] = len(outbound_nbrs[ib_nbr])

                # sum pagerank/outdegree
                sum_ranks = 0
                for node_n, outb in num_ob_nodes.items():
                    sum_ranks += nodes[node_n]/outb

                # pagerank = (1-damping)/len(node_list) + (damping * sum_ranks)
                copy_nodes[node] = (1-damping)/len(node_list) + (damping * sum_ranks)

        # compute delta
        curr_delta = 0
        for (_, v_1), (_, v_2) in zip(nodes.items(), copy_nodes.items()):
            curr_delta += abs(v_1 - v_2)
        delta = curr_delta
        nodes = copy_nodes.copy()
    return nodes

if __name__ == '__main__':
    file1 = comp614_module6.file_to_graph("test1.txt")
    print(bfs_dfs(file1, "A", comp614_module6.Stack()))
    print(page_rank(file1, 0))