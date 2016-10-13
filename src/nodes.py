import re
from datetime import datetime
from core import Link, Node, Graph, graph, db

COMMENT_REGEX = r'\B(@\w+)'

class Document(Node):
    def __init__(self, name, slug=None):
        super().__init__(name, slug)
        self.comment = ''

    def get_specific_connected_nodes(self):
        possible_nodes_slugs = self.parse_comment()
        existing_nodes = []
        for node_slug in possible_nodes_slugs:
            node = graph.get_node_by_slug(node_slug)
            if node is not None:
                existing_nodes.append(node)
        print('EXISTING nodes {}'.format(existing_nodes))
        return existing_nodes

    def parse_comment(self):
        nodes_slugs = re.findall(COMMENT_REGEX, self.comment)
        nodes_slugs = [slug[1:] for slug in nodes_slugs]
        nodes_slugs = list(set(nodes_slugs))
        print('FOUND nodes in comments {}'.format(nodes_slugs))
        return nodes_slugs


class TestNode(Node):
    def get_specific_connected_nodes(self):
        node_slug = input('> ')
        l = []
        print('Existing nodes: {}'.format(graph.nodes))
        while node_slug != '':
            node = graph.get_node_by_slug(node_slug)
            if node is not None:
                l.append(node)
            else:
                print('Node could not be found')
            node_slug = input('> ')
        return l

class Film(Document):
    pass

class Book(Document):
    pass

class Article(Document):
    pass

class Event(Node):
    def __init__(self, name, slug=None):
        super().__init__(name, slug)
        self.date = datetime.now()

class Person(Node):
    pass

class Tag(Node):
    pass
