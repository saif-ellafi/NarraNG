import os
from components import *


class Generator:

    def __init__(self, name, bound='m', weight=1.0):
        self.root_node = LinkNode(None, name, weight=weight, bound=bound)
        self.root_node.root = self.root_node
        self.name = name
        self.path = './projects/'+self.name+'.json'

    @staticmethod
    def create_link_node():
        name = None
        while not name:
            name = input('LinkNode name\n>> ')
        bound = None
        while bound not in ['m', 's', 'a', '#']:
            bound = input('LinkNode bound (many).\ns. single\nm. many\na. all\n>> ')
            if not bound:
                bound = 'm'
        weight = None
        while not weight:
            a = input("LinkNode weight (1.0)")
            if not a:
                weight = 1.0
            else:
                try:
                    weight = float(a)
                except ValueError:
                    weight = None
                    continue
        return name, bound, weight

    @staticmethod
    def create_leaf_node():
        name = ''
        while not name:
            name = input('LeafNode name\n>> ')
        weight = None
        while not weight:
            try:
                w = input('LeafNode weight (1.0)\n>> ')
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
        return 'Currently in node < %s > with back-root < %s >, links < %s > and leaves < %s >' % \
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
            a = input('enter node? y/n (y)\n>> ')
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
            answer = input('\ne. exit \nb. back\nr. root\ns. save\n#. cancel\nl. LinkNode\nf. LeafNode\n\n'
                           'enter $i to jump into a LinkNode\n\n>> ')

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
            name, bound, weight = self.create_link_node()
            if name == '#' or bound == '#':
                return self.menu(node)
            link_node = LinkNode(node, name, bound, weight)
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
        with open(self.path, 'w') as file:
            json.dump(self.root_node, file, indent=2, cls=NodeEncoder)

    def load(self):
        isfile = os.path.isfile(self.path)
        if not isfile:
            return "file does not exist"
        with open(self.path, 'r') as read_file:
            self.root_node = NodeDecoder.decode(read_file)
        self.run()

    def create(self):
        isfile = os.path.isfile(self.path)
        if isfile:
            r = None
            while r not in ['y', 'n']:
                r = input('file %s exists. continue? y/n (n)\n>> ')
            if not r or r == 'n':
                return
        self.run()
