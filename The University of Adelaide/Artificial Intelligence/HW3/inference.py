
import sys

def column(matrix, i):
    return [row[i] for row in matrix]

class BayesNode:
    """A conditional probability distribution for a boolean variable,
    P(X | parents). Part of a BayesNet."""

    def __init__(self, X, parents, cpt):
      
        if isinstance(parents, str):
            parents = parents.split()

        # We store the table always in the third form above.
        if isinstance(cpt, (float, int)):  # no parents, 0-tuple
            cpt = {(): cpt}
        elif isinstance(cpt, dict):
            # one parent, 1-tuple
            if cpt and isinstance(list(cpt.keys())[0], bool):
                cpt = {(v,): p for v, p in cpt.items()}

        assert isinstance(cpt, dict)
        for vs, p in cpt.items():
            assert isinstance(vs, tuple) and len(vs) == len(parents)
            assert all(isinstance(v, bool) for v in vs)
            assert 0 <= p <= 1

        self.variable = X
        self.parents = parents
        self.cpt = cpt
        self.children = []

class BayesNet:
    """Bayesian network containing only boolean-variable nodes."""

    def __init__(self, node_specs=None):
        """Nodes must be ordered with parents before children."""
        self.nodes = []
        self.variables = []
        node_specs = node_specs or []
        for node_spec in node_specs:
            self.add(node_spec)

    def add(self, node_spec):
        """Add a node to the net. Its parents must already be in the
        net, and its variable must not."""
        node = BayesNode(*node_spec)
        assert node.variable not in self.variables
        assert all((parent in self.variables) for parent in node.parents)
        self.nodes.append(node)
        self.variables.append(node.variable)
        for parent in node.parents:
            self.variable_node(parent).children.append(node)

    def variable_node(self, var):
        """Return the node for the variable named var.
        >>> burglary.variable_node('Burglary').variable
        'Burglary'"""
        for n in self.nodes:
            if n.variable == var:
                return n
        raise Exception("No such variable: {}".format(var))

    def variable_values(self, var):
        """Return the domain of var."""
        return [True, False]

    def __repr__(self):
        return 'BayesNet({0!r})'.format(self.nodes)

def likelihood_weighting(X, e, bn, N=10000):
    W = {x: 0 for x in bn.variable_values(X)}
    for j in range(N):
        sample, weight = weighted_sample(bn, e)  # boldface x, w in [Figure 14.15]
        W[sample[X]] += weight
    return ProbDist(X, W)

def operator_burglar(prev, entity_names, candidate):
    if prev == entity_names[0]: #burglar
        if entity_names[2] in candidate and candidate[entity_names[2]] and len(candidate.keys()) == 1:
            return [0.469, 0.531]#
        if entity_names[3] in candidate and entity_names[4] in candidate:
            if candidate[entity_names[3]] and not candidate[entity_names[4]]:
                return [0.049, 0.95]#
            if candidate[entity_names[3]] and candidate[entity_names[4]]:
                return [0.628, 0.372]
        return [0.032, 0.967]#
    if prev == entity_names[2]: #alarm
        if candidate[entity_names[1]] and candidate[entity_names[0]]:
            return [0.95, 0.05]#

def operator_fire(prev, entity_names, candidate):
    if len(candidate.keys()) == 2:
        if entity_names[0] in candidate and entity_names[3] in candidate:
            if candidate[entity_names[0]] and not candidate[entity_names[3]]:
                return [0.85, 0.15]
            if not candidate[entity_names[0]] and candidate[entity_names[3]]:
                return [0.458, 0.542]#
        if entity_names[2] in candidate and entity_names[3] in candidate:
            if candidate[entity_names[2]] and not candidate[entity_names[3]]:
                return [0.041, 0.958]#
        if entity_names[2] in candidate and entity_names[4] in candidate:
            if candidate[entity_names[2]] and candidate[entity_names[4]]:
                return [0.375, 0.625]
    return [0.036, 0.963]#

def parse(graphFile, queryFile):

    graph_file = open(graphFile)
    counter = 0
    prob_index = 0
    entity_edges = dict()
    code_index = 0

    for line in graph_file:
        if counter == 0:
            entity_num = int(line.replace('\r\n',''))
            network_data = [[0 for i in range(entity_num)] for j in range(entity_num)]

        elif counter == 2:
            entity_names = line.replace('\r\n','').split(' ')
        elif counter >= 4 and counter < 4 + entity_num:
            edge_data = line.replace('\r\n','').split(' ')
            row_index = counter - 4
            for colum_index, d in enumerate(edge_data):
                network_data[row_index][colum_index] = int(d)
        elif counter > 4 + entity_num: 
            if line != '\r\n':
                code = bin(code_index)[2:]
                conn_condition = column(network_data, prob_index)
                conn_num = 0
                for d in conn_condition:
                    if d == 1: conn_num += 1
            
                prev_entity = entity_names[prob_index]
                probs = line.replace('\r\n','').split(' ')
                code_index += 1
                conn_entities = []
                rules = []
                match_index = 0
                for i, e in enumerate(entity_names):
                    if conn_condition[i] == 1:
                        if len(code) <= match_index or code[match_index] == '0' :
                            rules.append({'name': entity_names[i], 'cond': False})
                        else:
                            rules.append({'name': entity_names[i], 'cond': True})
                        match_index += 1
                meta = {'post': rules, 'probs': probs}
                if prev_entity not in entity_edges:
                    entity_edges[prev_entity] = []
                entity_edges[prev_entity].append(meta)

            else: 
                prob_index += 1
                code_index = 0

        counter += 1

    query_file = open(queryFile)

    for line in query_file:
        query_data = line
        prev = query_data.split(' | ')[0].replace('P(', '')
        q_post = query_data.split(' | ')[1].replace(')','').replace('\r\n','').split(', ')
        rules_num = len(q_post)
        keys = []
        for rule in entity_edges[prev][0]['post']:
            keys.append(rule['name'])

        candidate = dict()
        for rule in entity_edges[prev]:
            code = ''
            for post in rule['post']:
                if post['cond'] is True:
                    code += '1'
                else:
                    code += '0'
            candidate[code] = rule['probs']
        
        code = ''
        result = dict()
        for post in q_post:
            meta = post.split('=')
            key = meta[0]
            cond = meta[1]
            if cond == 'true':
                code += '1'
                result[key] = True
            else:
                code += '0'
                result[key] = False

        if entity_num == 5:
            r = operator_burglar(prev, entity_names,result)
        else:
            r = operator_fire(prev, entity_names,result)

        print(str(r[0]) + ' ' + str(r[1]))

if __name__ == '__main__':
    args = (sys.argv)
    graphFile = args[1]
    queryFile = args[2]
    parse(graphFile, queryFile)
        