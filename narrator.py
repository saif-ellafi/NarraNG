import os
import random
import logging
import json
import pprint

from components import NodeDecoder, NodeEncoder, Node, LinkNode, LeafNode
from common import Common

logging.getLogger().setLevel(logging.WARN)


class Narrator:

    OUTPUT_FOLDER = 'output'
    SUBSECTION_CHAR = '*'
    SELECTION_CHAR = '-'
    COMMENT_CHAR = '#'

    IGNORE_REPEAT = True

    # Represents a weighted selection node
    class WeightedChoice:
        def __init__(self, node, min_bound, max_bound):
            self.node = node
            self.min_bound = min_bound
            self.max_bound = max_bound

    # Initializes project, path recognition and user input
    def __init__(self, project, name=None):
        logging.debug("DEBUG MODE ENABLED")
        self.name = name if name else project
        self.project = project
        self.root_node = None
        self.output_node_root = None
        self.load_project(project)
        self.intro = """
            Narrator initialized. On wizard, use the following inputs:
                - --help for command list
                - --save to save current output
                - --clear to restart target
                - Number selection
                - Empty For random selection
                - @n to generate n random selections
                - #n to generate n random of each possible selection
                - Any text for customized entry
                - 0 to exit
                """
        print(self.intro)

    # How is Narrative represented in console
    def __repr__(self):
        if self.output_node_root.links:
            content = '''--------------------\n{} ({})\n--------------------\n\n{}\n--------------------'''. \
                format(self.name, self.project, '\n'.join([str(index+1) + '. ' +
                                                           str(selection) for index, selection in enumerate(self.output_node_root.links)]))
        else:
            content = '''--------------------\n{} is empty\n--------------------'''. \
                format(self.name)
        return content

    # Handles user's input and validations
    @staticmethod
    def user_input(nodes):
        max_index = len(nodes)
        while True:
            choice = input('>> ').strip()
            if choice == '#':
                logging.debug("# random go")
                return choice
            elif choice.startswith('#') or choice.startswith('@'):
                logging.debug("# of each")
                try:
                    int(choice[1:])
                    return choice
                except ValueError:
                    pass
            elif not choice:
                logging.debug("single random shot")
                return Narrator.weighted_random_node(nodes)
            else:
                logging.debug("standard input chosen")
                try:
                    if 0 < int(choice) <= max_index:
                        return int(choice)
                except ValueError:
                    if choice:
                        return choice

    @staticmethod
    def delete(node, index):
        del node.links[index - 1]

    # Returns a random selection considering weights
    @staticmethod
    def weighted_random_node(keys):
        i = 0.0
        choices = []
        for key in keys:
            new_max = i+(1*key.weight)
            choices.append(Narrator.WeightedChoice(key, i, new_max))
            logging.debug("Adding weighted choice: %s %s %s" % (key.name, str(i), str(new_max)))
            i = new_max
        rnd = random.uniform(0.0, i)
        logging.debug('generated randon number: %s' % str(rnd))
        for choice in choices:
            if choice.min_bound <= rnd < choice.max_bound:
                logging.debug('found uniform match at: %s against: %s' % (str(rnd), str(choice.node.name)))
                return choice.node

    def reset_output_node(self):
        self.output_node_root = LinkNode(
            None,
            self.root_node.name,
            self.root_node.bound,
            self.root_node.weight,
            self.root_node.qrange,
            self.root_node.description
        )
        self.output_node_root.root = self.output_node_root

    def show_tree(self):
        pprint.pprint(json.dumps(self.root_node, cls=NodeEncoder))

    # Clears current selections
    def clear(self):
        logging.debug("Clearing build")
        self.reset_output_node()

    def load_project(self, project):
        if type(project) == LinkNode:
            self.root_node = project
        elif type(project) == str:
            path = os.path.join(Common.PROJECTS_FOLDER, project+'.json')
            with open(path) as file:
                self.root_node = NodeDecoder.decode(file)
        else:
            raise Exception("Invalid project type. Must be either a LinkNode or a path to file.")
        self.reset_output_node()

    def simulate_choice(self, node, node_links):
        if node.bound == 'single':
            if not node.locked:
                node.locked = True
                user_choice = self.weighted_random_node(node_links)
            else:
                logging.info("Node %s locked. Ignored new value." % node.name)
                user_choice = None
        elif node.bound == 'all':
            user_choice = '#'+str(1)
        else:
            rndchoice = round(random.triangular(node.qrange.minv, node.qrange.maxv, node.qrange.mode))
            logging.debug("Decided to go for %s nodes in %s" % (rndchoice, node.name))
            result_nodes = []
            for _ in range(0, rndchoice):
                result_nodes.append(self.weighted_random_node(node_links))
            user_choice = result_nodes.copy()
        return user_choice

    # Internal recursive value choice generator
    def _gen(self, node=None, output_node=None, auto=False):
        node = node if node else self.root_node
        output_node = output_node if output_node else self.output_node_root
        node_links = node.links
        logging.debug("successfully built " + str(len(node_links)) + ' selections')
        if auto:
            user_choice = self.simulate_choice(node, node_links)
        else:
            print('\n'.join([str(i+1) + '. ' + k.name for (i, k) in enumerate(node_links)]))
            user_choice = self.user_input(node_links)
        if str(user_choice) == '--exit':
            return True
        elif str(user_choice) == '--help':
            print(self.intro)
        elif str(user_choice) == '--save':
            self.save()
        elif str(user_choice) == '--clear':
            self.load_project(self.project)
        elif isinstance(user_choice, list):
            logging.debug("Detected list choice")
            for qnode in user_choice:
                self.handle_choice(qnode, output_node, auto)
        elif isinstance(user_choice, Node):
            self.handle_choice(user_choice, output_node, auto)
        elif str(user_choice) == '#':
            logging.debug("User entered Random mode")
            for i in range(0, len(node_links)):
                chosen_node = node_links[i]
                logging.debug("entering link %s" % chosen_node.name)
                self.handle_choice(chosen_node, output_node, auto=True)
        elif str(user_choice).startswith('#'):
            n = int(user_choice[1:])
            for i in range(0, len(node_links)):
                for _ in range(0, n):
                    chosen_node = node_links[i]
                    logging.debug("entering link %s" % chosen_node.name)
                    self.handle_choice(chosen_node, output_node, auto=True)
        elif str(user_choice).startswith('@'):
            n = int(user_choice[1:])
            for _ in range(0, n):
                self._gen(node, auto=True)
        elif type(user_choice) == str:
            node.links.append(LeafNode(node, user_choice, 1.0, None))
            print(self)
        else:
            if not node.locked:
                if node.bound == 'single':
                    node.locked = True
                chosen_node = node_links[user_choice - 1]
                self.handle_choice(chosen_node, output_node, auto)
            else:
                logging.info("Node %s locked. Ignored new value." % node.name)

    # Internal handled for choice roots
    def handle_choice(self, new_node, output_node, auto):
        if type(new_node) == LinkNode:
            blank_node = LinkNode(
                output_node,
                new_node.name,
                new_node.bound,
                new_node.weight,
                new_node.qrange,
                new_node.description
            )
            output_node.links.append(blank_node)
            self._gen(new_node, blank_node, auto=auto)
        else:
            if not (Narrator.IGNORE_REPEAT and new_node in output_node.links):
                output_node.links.append(new_node)
            else:
                logging.info('IGNORE_REPEAT is True and selection already exists in target')

    # User level wizard generation
    def gen(self):
        ret = False
        while not ret:
            print('\nMake your choice\n')
            ret = self._gen()
            print(self)

    def save(self):
        with open(os.path.join(Narrator.OUTPUT_FOLDER, self.name+'.txt'), 'w') as file:
            file.write(str(self))
        with open(os.path.join(Narrator.OUTPUT_FOLDER, self.name+'.json'), 'w') as file:
            json.dump(self.output_node_root, file, cls=NodeEncoder, indent=2)

