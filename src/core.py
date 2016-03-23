import pickle

class DataBase:
    DB = None
    def __new__(self, *args, **kwargs):
        if self.DB is None:
            self.DB = object.__new__(self, *args, **kwargs)
        return self.DB

    def __init__(self):
        self.nodes = []

    def save(self, path='save'):
        with open(path, 'wb') as f:
            pickle.dump(self.nodes, f)

    def load(self, path='save'):
        with open(path, 'rb') as f:
            self.nodes = pickle.load(f)

class Node:
    def __init__(self, name, tags={}, links=[]):
        self.name = name
        self.tags = tags
        self.links = links
        DataBase().nodes.append(self)

    def link(self, the_link):
        if the_link not in self.links:
            self.links.append(the_link)

class Link:
    def __init__(self, relatives, tags={}):
        self.relatives = relatives
        self.tags = tags
        for relative in relatives:
            relative.link(self)

if __name__ == '__main__':
    db = DataBase()

