import os

from components import *


class Generator:

    def __init__(self, name, bound='m', weight=1.0, qrange=QRange(1, 1, 'u')):
        self.root_node = LinkNode(None, name, weight=weight, bound=bound, qrange=qrange)
        self.root_node.root = self.root_node
        self.name = name
        self.path = './projects/'+self.name+'.json'

    @staticmethod
    def create_link_node():
        name = None
        while not name:
            name = input('LinkNode name\n>> ')
        if name == '#' :
            return ('#', '#', '#', '#' )
        bound = None
        while bound not in ['m', 's', 'a', '#']:
            bound = input('LinkNode bound (many).\ns. single\nm. many\na. all\n>> ')
            if not bound:
                bound = 'm'
        if bound == '#' :
            return ('#', '#', '#', '#' )
        weight = None
        while not weight:
            a = input("LinkNode weight (1.0)\n>> ")
            if not a:
                weight = 1.0
            elif a == '#':
                weight = '#'
            else:
                try:
                    weight = float(a)
                except ValueError:
                    weight = None
                    continue
        if weight == '#' :
            return ('#', '#', '#', '#' )
        qrange_dist = None
        while qrange_dist not in ['u', 'n', 't', '#']:
            qrange_dist = input('LinkNode0 qrange dist (u).\nu. uniform\nn. normal\nt. t-dist\n>> ')
            if not qrange_dist:
                qrange_dist = 'u'
        if qrange_dist == '#' :
            return ('#', '#', '#', '#' )
        qrange_minv = None
        while not qrange_minv:
            a = input("LinkNode qrange min (1)\n>> ")
            if not a:
                qrange_minv = 1
            elif a == '#' :
                qrange_minv = '#'
            else:
                try:
                    qrange_minv = int(a)
                except ValueError:
                    qrange_minv = None
                    continue
        if qrange_minv  == '#' :
            return ('#', '#', '#', '#' )
        qrange_maxv = None
        while not qrange_maxv:
            a = input("LinkNode qrange max (1)\n>> ")
            if not a:
                qrange_maxv = 1
            elif a == '#' :
                qrange_maxv = '#'
            else:
                try:
                    qrange_maxv = int(a)
                except ValueError:
                    qrange_maxv = None
                    continue
        if qrange_maxv  == '#' :
            return ('#', '#', '#', '#' )
        return name, bound, weight, QRange(qrange_minv, qrange_maxv, qrange_dist)

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
                       map(lambda n: str(n[0]+1) + ': ' + n[1].name,
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
            answer = input('\ne. exit \nb/0. back\nr. root\ns. save\n#. cancel\nl. LinkNode\nql. Quick LinkNode\nf. LeafNode\n\n'
                           'enter $i to jump into a LinkNode\n\n>> ')

        try:
            link_answer = int(answer)
        except ValueError:
            link_answer = None

        if answer == 'e':
            return
        if answer == 'b' or link_answer == 0:
            return self.menu(node.root)
        elif answer == 'r':
            return self.menu(self.root_node)
        elif answer == 's':
            self.save()
            return self.menu(self.root_node)
        elif answer == 'l':
            name, bound, weight, qrange = self.create_link_node()
            if name == '#' or bound == '#' or weight == '#' or qrange == '#':
                return self.menu(node)
            link_node = LinkNode(node, name, bound, weight, qrange)
            links.append(link_node)
            return self.enter_or_not(node, link_node)
        elif answer == 'ql':
            name = input("Quick name input: \n>> ")
            bound, weight, qrange =( 'm', 1.0, QRange(minv=1, maxv=1, dist='u'))
            if name == '#' or bound == '#':
                return self.menu(node)
            link_node = LinkNode(node, name, bound, weight, qrange)
            links.append(link_node)
            return self.enter_or_not(node, link_node)
        elif answer == 'f':
            name, weight = self.create_leaf_node()
            if name == '#' or weight == '#':
                return self.menu(node)
            leaf_node = LeafNode(node, name, weight)
            links.append(leaf_node)
            return self.menu(node)
        elif 1 <= link_answer <= len(node_links):
            return self.menu(node_links[link_answer - 1])
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
