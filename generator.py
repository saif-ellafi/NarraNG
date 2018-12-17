import os
from components import *


class Generator:

    def __init__(self, name, bound='m'):
        self.root_node = LinkNode(None, name, bound=bound)
        self.root_node.root = self.root_node
        self.name = name
        self.path = './projects/'+self.name+'.json'

    @staticmethod
    def create_link_node():
        name = None
        while not name:
            name = input('LinkNode name\n')
        bound = None
        while bound not in ['m', 's', 'a', '#']:
            bound = input('LinkNode bound (many).\ns. single\nm. many\na. all')
            if not bound:
                bound = 'm'
        return name, bound

    @staticmethod
    def create_leaf_node():
        name = ''
        while not name:
            name = input('LeafNode name\n')
        weight = None
        while not weight:
            try:
                w = input('LeafNode weight (1.0)\n')
                if not w:
                    weight = 1.0
                elif w == '#':
                    weight = '#'
                else:
                    weight = float(w)
            except ValueError:
                continue
        return name, weight

    @staticmethod
    def status(node):
        return 'Currently in node <%s> with back-root <%s>, links <%s> and leaves <%s>' % \
               (
                   node.name,
                   node.root.name,
                   ' | '.join(
                       map(lambda n: str(n[0]) + ': ' + n[1].name,
                           enumerate(filter(lambda nn: type(nn) == LinkNode, node.links))
                           )
                   ),
                   ' | '.join(map(lambda n: n.name,
                                  filter(lambda nn: type(nn) == LeafNode, node.links)
                                  )
                              )
               )

    def enter_or_not(self, current_node, new_node):
        a = None
        while a not in ['y', 'n']:
            a = input('enter node? y/n (y)')
            if a == '' or a == 'y':
                return self.menu(new_node)
            elif a == 'n':
                return self.menu(current_node)

    def menu(self, node):
        if type(node) != LinkNode:
            raise Exception("Something went wrong. Launched menu with a %s" % node)
        print(self.status(node))
        links = node.links
        node_links = list(filter(lambda n: type(n) == LinkNode, links))
        answer = None

        while not answer:
            answer = input('\ne. exit \nb. back\nr. root\ns. save\nl. LinkNode\nf. LeafNode\n\n'
                           'enter $i to jump into a LinkNode')

        try:
            link_answer = int(answer)
        except ValueError:
            link_answer = None

        if answer == 'e':
            return
        if answer == 'b':
            return self.menu(node.root)
        elif answer == 'r':
            return self.menu(self.root_node)
        elif answer == 's':
            self.save()
            return self.menu(self.root_node)
        elif answer == 'l':
            name, bound = self.create_link_node()
            if name == '#' or bound == '#':
                return self.menu(node)
            link_node = LinkNode(node, name, bound)
            links.append(link_node)
            return self.enter_or_not(node, link_node)
        elif answer == 'f':
            name, weight = self.create_leaf_node()
            if name == '#' or weight == '#':
                return self.menu(node)
            leaf_node = LeafNode(node, name, weight)
            links.append(leaf_node)
            return self.menu(node)
        elif 0 <= link_answer < len(node_links):
            print("here", link_answer)
            return self.menu(node_links[link_answer])
        else:
            return self.menu(node)

    def run(self):
        self.menu(self.root_node)
        self.save()

    def save(self):
        file = open(self.path, 'w')
        json.dump(self.root_node, file, indent=2, cls=NodeEncoder)
        file.close()

    def load(self):
        isfile = os.path.isfile(self.path)
        if not isfile:
            return "file does not exist"
        read_file = open(self.path, 'r')
        self.root_node = NodeDecoder.decode(read_file)
        read_file.close()
        self.run()

    def create(self):
        isfile = os.path.isfile(self.path)
        if isfile:
            r = None
            while r not in ['y', 'n']:
                r = input('file %s exists. continue? y/n (n)')
            if not r or r == 'n':
                return
        self.run()
