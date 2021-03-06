import pickle, re

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

        if [n for n in self.nodes if node != n and (n.name == node.name or n.slug == node.slug)]:
            raise ValueError('Trying to duplicate a node! Name or slug already taken.')
            # we check each time that the name and slug are not taken because the name and slug can be changed
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

    def get_node_by_slug(self, slug):
        l = [node for node in self.nodes if node.slug == slug]
        if len(l) == 1:
            return l[0]
        elif len(l) > 1:
            raise ValueError('Several nodes with the same slug!')
        else:
            return None

class Node:
    def __init__(self, name, slug=None):
        self.name = name
        self.links = []
        self.slug = self.slugify(slug or name)

    @staticmethod
    def slugify(name):
        slug = name.strip()
        slug = slug.lower()
        slug = re.sub(r'[\W_]', '-', slug)  # replace all non alphanumeric and _ with -
        slug = re.sub(r'-+', '-', slug)  # remplace ----- to -
        slug = slug.strip('-')
        return slug

    def __repr__(self):
        return '<Node \'{}\'>'.format(self.slug)

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


db = DataBase()
graph = Graph()



