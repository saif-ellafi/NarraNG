import logging
from components import *

logging.getLogger().setLevel(logging.WARN)


class Generator:

    def __init__(self, project_name):
        self.root_node = None
        self.project_name = project_name
        self.path = './projects/'+project_name+'.json'

    @staticmethod
    def input_qrange(bound):
        if bound in ['a', 's']:
            qrange_minv = 1
        else:
            qrange_minv = None
        while not qrange_minv:
            a = input("LinkNode qrange min (1)\n>> ")
            if not a:
                qrange_minv = 1
            elif a == '#':
                qrange_minv = '#'
            else:
                try:
                    qrange_minv = int(a)
                except ValueError:
                    qrange_minv = None
                    continue
        if qrange_minv == '#':
            return None, None, None
        if bound in ['a', 's']:
            qrange_maxv = 1
        else:
            qrange_maxv = None
        while not qrange_maxv:
            a = input("LinkNode qrange max (1)\n>> ")
            if not a:
                qrange_maxv = 1
            elif a == '#':
                qrange_maxv = '#'
            else:
                try:
                    qrange_maxv = int(a)
                except ValueError:
                    qrange_maxv = None
                    continue
        if qrange_maxv == '#':
            return None, None, None
        if bound in ['a', 's']:
            qrange_mode = 1
        else:
            qrange_mode = None
        while not qrange_mode:
            input_mode = input('LinkNode qrange mode (%f)\n>> ' % ((qrange_minv+qrange_maxv)/2))
            if input_mode == '#':
                return None, None, None
            if not qrange_mode:
                qrange_mode = (qrange_minv+qrange_maxv)/2
            try:
                input_mode = float(input_mode)
                if qrange_minv <= qrange_mode <= qrange_maxv:
                    qrange_mode = input_mode
                else:
                    continue
            except ValueError:
                continue
        return qrange_minv, qrange_maxv, qrange_mode

    @staticmethod
    def input_weight(root_node):
        if root_node and root_node.bound == 'all':
            weight = 1.0
        else:
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
        return weight

    @staticmethod
    def create_link_node(given_name=None, root_node=None):
        name = given_name
        while not name:
            name = input('LinkNode name\n>> ')
        if name == '#':
            return
        bound = None
        while bound not in ['m', 's', 'a', '#']:
            bound = input('LinkNode bound (many).\ns. single\nm. many\na. all\n>> ')
            if not bound:
                bound = 'm'
        if bound == '#':
            return
        weight = Generator.input_weight(root_node)
        if weight == '#':
            return
        qrange_minv, qrange_maxv, qrange_mode = Generator.input_qrange(bound)
        if not qrange_minv or not qrange_maxv or not qrange_mode:
            return
        description = input('LinkNode description (none)\n>> ')
        if description == '#':
            return
        if not description:
            description = None
        node = LinkNode(root_node, name, description)
        node.set_bound(bound)
        node.set_weight(weight)
        node.set_qrange(QRange(qrange_minv, qrange_maxv, qrange_mode))
        return node

    @staticmethod
    def create_leaf_node(root_node):
        name = ''
        while not name:
            name = input('LeafNode name\n>> ')
        if name == '#':
            return
        weight = Generator.input_weight(root_node)
        if weight == '#':
            return
        description = input('LeafNode description (none)\n>> ')
        if description == '#':
            return
        if not description:
            description = None
        node = LeafNode(root_node, name, description)
        node.set_weight(weight)
        return node

    @staticmethod
    def create_value_node(root_node):
        name = ''
        while not name:
            name = input('ValueNode name\n>> ')
        if name == '#':
            return
        weight = Generator.input_weight(root_node)
        if weight == '#':
            return
        description = input('ValueNode description (none)\n>> ')
        if description == '#':
            return
        if not description:
            description = None
        qrange_minv, qrange_maxv, qrange_mode = Generator.input_qrange(root_node.bound)
        node = ValueNode(root_node, name, description)
        node.set_weight(weight)
        node.set_qrange(QRange(qrange_minv, qrange_maxv, qrange_mode))
        return node

    @staticmethod
    def create_external_node(root_node):
        name = ''
        while not name:
            name = input('ExternalNode name\n>> ')
        if name == '#':
            return
        weight = Generator.input_weight(root_node)
        if weight == '#':
            return
        description = input('ExternalNode description (none)\n>> ')
        if description == '#':
            return
        if not description:
            description = None
        link = None
        while not link:
            link = input('ExternalNode link\n>> ')
        node = ExternalNode(root_node, name, description, link)
        node.set_weight(weight)
        return node

    @staticmethod
    def status(node):
        return '\nCurrently in node < %s > with\nback-root< %s >\nlinks < %s >\nexternal < %s >\nleaves < %s >\nvalues < %s >' % \
               (
                   node.name,
                   node.root.name,
                   ' | '.join(
                       map(lambda n: str(n[0]+1) + ': ' + n[1].name,
                           enumerate(filter(lambda nn: type(nn) == LinkNode, node.links))
                           )
                   ),
                   ' | '.join(
                       map(lambda n: n.name,
                           filter(lambda nn: type(nn) == ExternalNode, node.links)
                           )
                   ),
                   ' | '.join(map(lambda n: n.name,
                                  filter(lambda nn: type(nn) == LeafNode, node.links)
                                  )
                              ),
                   ' | '.join(map(lambda n: n.name,
                                  filter(lambda nn: type(nn) == ValueNode, node.links)
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
            answer = input('\ne. exit \nb/0. back\nr. root\ns. save\n#. cancel\nl. LinkNode\nq. Quick LinkNode\nx. '
                           'External LinkNode\nf. LeafNode\nv. ValueNode\n\nenter $i to jump into a LinkNode\n\n>> ')

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
            link_node = self.create_link_node(root_node=node)
            if not link_node:
                return self.menu(node)
            links.append(link_node)
            return self.enter_or_not(node, link_node)
        elif answer == 'x':
            external_node = self.create_external_node(root_node=node)
            links.append(external_node)
            return self.menu(node)
        elif answer == 'q':
            name = input("Quick name input\n>> ")
            bound, weight, qrange, description = ('m', 1.0, QRange(minv=1, maxv=1, mode='u'), None)
            if name == '#' or bound == '#':
                return self.menu(node)
            link_node = LinkNode(node, name, description)
            link_node.set_bound(bound)
            link_node.set_weight(weight)
            link_node.set_qrange(qrange)
            links.append(link_node)
            return self.enter_or_not(node, link_node)
        elif answer == 'f':
            leaf_node = self.create_leaf_node(root_node=node)
            if not leaf_node:
                return self.menu(node)
            links.append(leaf_node)
            return self.menu(node)
        elif answer == 'v':
            value_node = self.create_value_node(root_node=node)
            if not value_node:
                return self.menu(node)
            links.append(value_node)
            return self.menu(node)
        elif link_answer and 1 <= link_answer <= len(node_links):
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
                r = input('file %s exists. continue? y/n (n)\n>> ' % self.path)
                if not r or r == 'n':
                    return
        self.root_node = self.create_link_node(given_name=self.project_name)
        self.root_node.root = self.root_node
        self.run()
