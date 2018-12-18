import os
import random
import logging
import json
import pprint

from components import NodeDecoder, NodeEncoder, Node, LinkNode
from common import Common

logging.getLogger().setLevel(logging.INFO)


class Narrator:

    OUTPUT_FOLDER = 'output'
    SUBSECTION_CHAR = '*'
    SELECTION_CHAR = '-'
    COMMENT_CHAR = '#'

    IGNORE_REPEAT = True

    # Represents a narrative selection
    class Selection:
        def __init__(self, name, history):
            self.name = name
            self.history = history

        def __eq__(self, other):
            if isinstance(other, Narrator.Selection):
                return self.name == other.name and self.history == other.history
            else:
                return False

    # Represents a weighted selection node
    class WeightedChoice:
        def __init__(self, node, min_bound, max_bound):
            self.node = node
            self.min_bound = min_bound
            self.max_bound = max_bound

    # Initializes project, path recognition and user input
    def __init__(self, project, name=None):
        self.name = name if name else project
        self.project = project
        self.root_node = None
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
                - 0 to return and do nothing
                """
        self.load_project(project)
        self.build = []
        print(self.intro)
        logging.debug("DEBUG MODE ENABLED")

    # How is Narrative represented in console
    def __repr__(self):
        if self.build:
            content = '''--------------------\n{} ({}) has:\n--------------------\n{}'''. \
                format(self.name, self.project, '\n'.join([str(index+1) + '. ' + ' '.join(selection.history) + ' ' +
                                                           selection.name for index, selection in enumerate(self.build)]))
        else:
            content = '''--------------------\n{} is empty\n--------------------'''. \
                format(self.name)
        return content

    # Handles user's input and validations
    @staticmethod
    def input_callback(nodes):
        max_index = len(nodes)
        while True:
            choice = input('>> ').strip()
            if choice == '0':
                logging.debug("exit option selected")
                return 0
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

    def show_tree(self):
        pprint.pprint(json.dumps(self.root_node, cls=NodeEncoder))

    # Clears current selections
    def clear(self):
        logging.debug("Clearing build")
        self.build = []

    # Deletes a specific selection
    def delete(self, index):
        del self.build[index-1]

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

    def load_project(self, project):
        path = os.path.join(Common.PROJECTS_FOLDER, project+'.json')
        if type(project) == LinkNode:
            self.root_node = project
        elif type(project) == str:
            with open(path) as file:
                self.root_node = NodeDecoder.decode(file)
        else:
            raise Exception("Invalid project type. Must be either a LinkNode or a path to file.")

    # Internal recursive value choice generator
    def _gen(self, node=None, history=None, auto=False):
        node = node if node else self.root_node
        node_links = node.links
        history = history if history else []
        logging.debug("successfully built " + str(len(node_links)) + ' selections')
        if auto:
            if node.bound == 'single':
                if not node.locked:
                    node.locked = True
                    user_choice = self.weighted_random_node(node_links)
                else:
                    logging.info("Node %s locked. Ignored new value." % node.name)
                    return False
            elif node.bound == 'all':
                user_choice = '#'+str(len(node.links))
            else:
                user_choice = self.weighted_random_node(node_links)
        else:
            print('\n'.join([str(i+1) + '. ' + k.name for (i, k) in enumerate(node_links)]))
            user_choice = self.input_callback(node_links)
        if user_choice == 0:
            return True
        elif str(user_choice) == '--help':
            print(self.intro)
        elif str(user_choice) == '--save':
            self.save()
        elif str(user_choice) == '--clear':
            self.build.clear()
            self.load_project(self.project)
        elif isinstance(user_choice, Node):
            self.handle_choice(user_choice, history, auto)
        elif str(user_choice).startswith('#'):
            n = int(user_choice[1:])
            for i in range(0, len(node_links)):
                for _ in range(0, n):
                    chosen_value = node_links[i]
                    self.handle_choice(chosen_value, history, auto=True)
        elif str(user_choice).startswith('@'):
            n = int(user_choice[1:])
            for _ in range(0, n):
                self._gen(node, history, auto=True)
        elif type(user_choice) == str:
            self.build.append(self.Selection(user_choice, history))
            print(self)
        else:
            if not node.locked:
                if node.bound == 'single':
                    node.locked = True
                chosen_value = node_links[user_choice - 1]
                self.handle_choice(chosen_value, history, auto)
            else:
                logging.info("Node %s locked. Ignored new value." % node.name)

    # Internal handled for choice roots
    def handle_choice(self, chosen_value, history, auto):
        if type(chosen_value) == LinkNode:
            hc = history.copy()
            hc.append(chosen_value.name)
            self._gen(chosen_value, hc, auto=auto)
        else:
            selection = self.Selection(chosen_value.name, history)
            if not (Narrator.IGNORE_REPEAT and selection in self.build):
                self.build.append(selection)
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

