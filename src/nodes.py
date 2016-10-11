import re
from core import Link, Node, Graph, graph, db

COMMENT_REGEX = r'\B(@\w+)'

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
        print('EXISTING nodes {}'.format(existing_nodes))
        return existing_nodes

    def parse_comment(self):
        nodes_names = re.findall(COMMENT_REGEX, self.comment)
        nodes_names = [name[1:] for name in nodes_names]
        nodes_names = list(set(nodes_names))
        print('FOUND nodes in comments {}'.format(nodes_names))
        return nodes_names


class TestNode(Node):
    def get_specific_connected_nodes(self):
        node_name = input('> ')
        l = []
        print('Existing nodes: {}'.format(graph.nodes))
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


