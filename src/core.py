import pickle

class DataBase:
    def __init__(self):
        self.graph = Graph()

    def save(self, path='save'):
        with open(path, 'wb') as f:
            pickle.dump(self.graph, f)

    def load(self, path='save'):
        with open(path, 'rb') as f:
            self.graph = pickle.load(f)

class Graph:
    def __init__(self):
        self.nodes = []

    @property
    def links(self):
        return list(set(link for node in self.nodes for link in node.links))

    def save_node(self, node):
        # add to graph the node
        # check for duplication
        # offer to merge (?)
        # add the links, create them as lone node if necessary, or add the links if not lone_nodese

        if [n for n in self.nodes if n.name == node.name]:
            raise ValueError('Trying to duplicate a node! Name already taken.')
            # we check each time that the name is not taken because the name can be changed
        if node not in self.nodes:
            self.nodes.append(node)
            print('Node {} added to the graph'.format(node))

        connected_nodes = node.get_specific_connected_nodes()
        for connected_node in connected_nodes:
            if connected_node not in self.nodes:
                raise ValueError('Node {} is unknown!'.format(connected_node))
        old_connected_nodes = [link.to_node for link in node.links_to_others]
        for old_connected_node in old_connected_nodes:
            if old_connected_node not in connected_nodes:
                node.get_link_to(old_connected_node).delete()

        for connected_node in connected_nodes:
            if connected_node not in old_connected_nodes:
                node.link_to(connected_node)

    def get_node(self, name):
        l = [node for node in self.nodes if node.name == name]
        if len(l) == 1:
            return l[0]
        elif len(l) > 1:
            raise ValueError('Several nodes with the same name!')
        else:
            return None

class Node:
    def __init__(self, name):
        self.name = name
        self.links = []

    def __repr__(self):
        return '<Node \'{}\'>'.format(self.name)

    @property
    def links_to_others(self):
        return [link for link in self.links if link.from_node == self]

    @property
    def links_from_others(self):
        return [link for link in self.links if link.to_node == self]

    def node_is_relative_to(self, other_node):
        return other_node in [node for link in self.links_to_others for node in link.nodes]

    def node_is_relative_from(self, other_node):
        return other_node in [node for link in self.links_from_others for node in link.nodes]

    def link_to(self, other_node):
        if other_node == self:
            raise ValueError('A node cannot be linked to itself!')
        if not self.node_is_relative_to(other_node):
            if not other_node.node_is_relative_from(self):
                l = Link(self, other_node)
                l.register()
            else:
                raise ValueError('Asymetrie detected! A node knows another that doesn t know it.')

    def get_link_to(self, other_node):
        l = [link for link in self.links_to_others if link.to_node == other_node]
        if len(l) == 1:
            return l[0]
        else:
            raise ValueError('{} link from {} to {}'.format(len(l), self, other_node))


    def get_specific_connected_nodes(self):
        raise NotImplementedError()


class Link:
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node

    def __repr__(self):
        return 'Link from {} to {}'.format(self.from_node, self.to_node)

    @property
    def nodes(self):
        return [self.from_node, self.to_node]

    def register(self):
        for node in self.nodes:
            node.links.append(self)

    def delete(self):
        self.from_node.links.remove(self)
        self.to_node.links.remove(self)

class Document(Node):
    def __init__(self, name):
        super().__init__(name)
        self.comment = ''

    def get_specific_connected_nodes(self):
        possible_nodes_names = self.parse_comment()
        existing_nodes = []
        for node_name in possible_nodes_names:
            node = graph.get_node(node_name)
            if node is not None:
                existing_nodes.append(node)
        return existing_nodes

    def parse_comment(self):
        nodes_names = ['node 1', 'kaboom']
        print(nodes_names)
        return nodes_names


class TestNode(Node):
    def get_specific_connected_nodes(self):
        node_name = input('> ')
        l = []
        print('Existing nodes: {}'.format(DataBase().graph.nodes))
        while node_name != '':
            node = graph.get_node(node_name)
            if node is not None:
                l.append(node)
            else:
                print('Node could not be found')
            node_name = input('> ')
        return l

class Film(Document):
    pass

class Book(Document):
    pass

class Article(Document):
    pass

db = DataBase()
graph = Graph()



