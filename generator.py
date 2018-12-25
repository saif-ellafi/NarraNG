import logging
from components import *

logging.getLogger().setLevel(logging.WARN)


class Generator:

    def __init__(self, project_name):
        self.root_node = None
        self.project_name = project_name
        self.path = './projects/'+project_name+'.json'

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
        if weight == '#':
            return
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
            return
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
            return
        if bound in ['a', 's']:
            qrange_mode = 1
        else:
            qrange_mode = None
        while not qrange_mode:
            input_mode = input('LinkNode qrange mode (%i)\n>> ' % round((qrange_minv+qrange_maxv)/2))
            if input_mode == '#':
                return
            if not qrange_mode:
                qrange_mode = round((qrange_minv+qrange_maxv)/2)
            try:
                input_mode = int(input_mode)
                if qrange_minv <= qrange_mode <= qrange_maxv:
                    qrange_mode = input_mode
                else:
                    continue
            except ValueError:
                continue
        description = input('LinkNode description (none)\n>> ')
        if description == '#':
            return
        if not description:
            description = None
        return LinkNode(root_node, name, bound, weight, QRange(qrange_minv, qrange_maxv, qrange_mode), description)

    @staticmethod
    def create_leaf_node(root_node):
        name = ''
        while not name:
            name = input('LeafNode name\n>> ')
        if name == '#':
            return
        if root_node.bound in ['a', 's']:
            weight = 1.0
        else:
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
        if weight == '#':
            return
        description = input('LeafNode description (none)\n>> ')
        if description == '#':
            return
        if not description:
            description = None
        return LeafNode(root_node, name, weight, description)

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
                   ) if not node.external else (node.external + '(external)'),
                   ' | '.join(map(lambda n: n.name,
                                  filter(lambda nn: type(nn) == LeafNode, node.links)
                                  )
                              ) if not node.external else '(external)'
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
            answer = input('\ne. exit \nb/0. back\nr. root\ns. save\n#. cancel\nl. LinkNode\nql. Quick LinkNode\nxl. '
                           'External LinkNode\nf. LeafNode\n\nenter $i to jump into a LinkNode\n\n>> ')

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
            if node.external:
                logging.warning('Cannot add LinkNode. Node links are external')
                return self.menu(node)
            link_node = self.create_link_node(root_node=node)
            if not link_node:
                return self.menu(node)
            links.append(link_node)
            return self.enter_or_not(node, link_node)
        elif answer == 'xl':
            if len(links) != 0:
                logging.warning("external links require current node links to be empty")
                return self.menu(node)
            node.external = input("external link name\n>> ")
            return self.menu(node)
        elif answer == 'ql':
            if node.external:
                logging.warning('Cannot add LinkNode. Node links are external')
                return self.menu(node)
            name = input("Quick name input\n>> ")
            bound, weight, qrange, description = ('m', 1.0, QRange(minv=1, maxv=1, mode='u'), None)
            if name == '#' or bound == '#':
                return self.menu(node)
            link_node = LinkNode(node, name, bound, weight, qrange, description)
            links.append(link_node)
            return self.enter_or_not(node, link_node)
        elif answer == 'f':
            if node.external:
                logging.warning('Cannot add LinkNode. Node links are external')
                return self.menu(node)
            leaf_node = self.create_leaf_node(root_node=node)
            if not leaf_node:
                return self.menu(node)
            links.append(leaf_node)
            return self.menu(node)
        elif link_answer and 1 <= link_answer <= len(node_links):
            if node.external:
                logging.warning('Cannot enter an external LinkNode')
                return self.menu(node)
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
