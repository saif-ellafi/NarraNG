import random
import copy

from components import *
from common import Common

logging.getLogger().setLevel(Common.LOG_LEVEL)


class Narrator:

    IGNORE_REPEAT = True

    # Represents a weighted selection node
    class WeightedChoice:
        def __init__(self, node, min_bound, max_bound):
            self.node = node
            self.min_bound = min_bound
            self.max_bound = max_bound

    class Entry:
        def __init__(self, eid, node):
            self.eid = eid
            self.node = node

    # Initializes project, path recognition and user input
    def __init__(self, project, name=None):
        logging.debug("DEBUG MODE ENABLED")
        self.name = name if name else project
        self.project_source = project
        self.root_node = None
        self.output_node_root = None
        self.load_project(project)
        self.intro = """
            Narrator initialized for %s - %s. On wizard, use the following inputs:
                - --help for command list
                - --save to save current output
                - --clear to restart target
                - --exit to quit
                - Number selection
                - Empty For random selection
                - @n to generate n random selections
                - #n to generate n random of each possible selection
                - # for full random strategy (Recommended)
                - Any text for customized entry
                - 0 to exit
                """ % (project, name)
        print(self.intro)

    # How is Narrative represented in console
    def __repr__(self):
        if self.output_node_root.links:
            content = '''--------------------\n{} ({})\n--------------------\n\n{}\n--------------------'''. \
                format(self.name, self.project_source, '\n'.join([str(index + 1) + '. ' +
                                                                  str(selection) for index, selection in
                                                                  enumerate(self.output_node_root.links)]))
        else:
            content = '''--------------------\n{} is empty\n--------------------'''. \
                format(self.name)
        return content

    @staticmethod
    def load_output_entries(project_id):
        entries = []
        target_project = Common.load_projects()[project_id]
        path = os.path.join(Common.OUTPUT_FOLDER, target_project.name)
        if not os.path.exists(path):
            return entries
        entry_files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.json')]
        i = 0
        for entry_path in entry_files:
            with open(entry_path, 'r') as entry_file:
                decoded_entry = OutputNodeDecoder.decode(entry_file)
                if decoded_entry.project == target_project.name:
                    entries.append(Narrator.Entry(i, decoded_entry))
                    i += 1
        return entries

    @staticmethod
    def load_external_node(external_node):
        path = os.path.join(external_node.link)
        with open(path) as file:
            node = NodeDecoder.decode(file)
        # Give priority to current root attributes
        if external_node.weight:
            node.set_weight(external_node.weight)
        if external_node.qrange:
            node.set_qrange(external_node.qrange)
        if external_node.bound:
            node.set_bound(external_node.bound)
        return node

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
        clean_node = LinkNode(
            None,
            self.root_node.name,
            self.root_node.description
        )
        clean_node.root = self.output_node_root
        clean_node.project = self.root_node.project
        self.output_node_root = clean_node

    # Clears current selections
    def clear(self):
        logging.debug("Clearing build")
        self.reset_output_node()

    def load_project(self, project):
        if isinstance(project, LinkNode):
            self.root_node = project
            self.name = project.name
        elif isinstance(project, str):
            path = os.path.join(project)
            with open(path) as file:
                self.root_node = NodeDecoder.decode(file)
                self.root_node.project = self.root_node.name
                self.root_node.name = self.name
        else:
            raise Exception("Invalid project type. Must be either a LinkNode or a path to file.")
        self.reset_output_node()

    def simulate_choice(self, node, node_links):
        if node.bound == 'single':
            if not node.locked:
                node.locked = True
                user_choice = [self.weighted_random_node(node_links)]
                for link in node_links:
                    if link.must and link not in user_choice:
                        user_choice.insert(0, link)
            else:
                logging.info("Node %s locked. Ignored new value." % node.name)
                user_choice = None
        elif node.bound == 'all':
            user_choice = '#'+str(1)
        else:
            rndchoice = round(random.triangular(node.qrange.minv, node.qrange.maxv, node.qrange.mode))
            logging.debug("Decided to go for %s nodes in %s" % (rndchoice, node.name))
            result_nodes = []
            if rndchoice > 0:
                for _ in range(0, rndchoice):
                    result_nodes.append(self.weighted_random_node(node_links))
                for link in node_links:
                    if link.must and link not in result_nodes:
                        result_nodes.insert(0, link)
            user_choice = result_nodes
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
        logging.debug("parsing choice for node %s" % node.name)
        if str(user_choice) == '--exit':
            return True
        elif str(user_choice) == '--help':
            print(self.intro)
        elif str(user_choice) == '--save':
            self.output_node_root.save()
        elif str(user_choice) == '--clear':
            self.load_project(self.project_source)
        elif isinstance(user_choice, list):
            logging.debug("Detected list choice")
            if user_choice:
                for qnode in user_choice:
                    self.handle_choice(qnode, output_node, auto)
            else:
                logging.info("node with empty selections. deleting root %s" % output_node.root.name)
                del output_node.root.links[output_node.root.links.index(output_node)]
        elif isinstance(user_choice, Node):
            self.handle_choice(user_choice, output_node, auto)
        elif str(user_choice) == '#':
            logging.debug("User entered Random mode")
            self._gen(node, auto=True)
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
        elif isinstance(user_choice, str):
            node.links.append(LeafNode(node, user_choice, None))
            print(self)
        else:
            if not node.locked:
                if node.bound == 'single':
                    node.locked = True
                chosen_node = node_links[user_choice - 1]
                self.handle_choice(chosen_node, output_node, auto)
            else:
                logging.info("Node %s locked. Ignored new value." % node.name)

    @staticmethod
    def get_set_value(node, auto):
        if node.vrange and auto:
            return round(random.triangular(
                node.vrange.minv,
                node.vrange.maxv,
                node.vrange.mode))
        elif node.vrange:
            value = None
            while not isinstance(value, int):
                try:
                    v = int(input('Enter %s value:\n>> ' % node.name))
                    if node.vrange.minv <= v <= node.vrange.maxv:
                        value = v
                        break
                    else:
                        continue
                except ValueError:
                    continue
            return value
        else:
            return None

    # Internal handled for choice roots
    def handle_choice(self, new_node, output_node, auto):
        if isinstance(new_node, ExternalNode):
            logging.debug("Processing external node %s" % new_node.name)
            if new_node in output_node.links:
                self._gen(self.load_external_node(new_node), output_node.links[output_node.links.index(new_node)], auto=auto)
            else:
                blank_node = LinkNode(
                    output_node,
                    new_node.name,
                    new_node.description
                )
                output_node.links.append(blank_node)
                self._gen(self.load_external_node(new_node), blank_node, auto=auto)
        elif isinstance(new_node, LinkNode):
            if new_node in output_node.links:
                self._gen(new_node, output_node.links[output_node.links.index(new_node)], auto=auto)
            else:
                blank_node = LinkNode(
                    output_node,
                    new_node.name,
                    new_node.description
                )
                set_value = Narrator.get_set_value(new_node, auto)
                if isinstance(set_value, int):
                    blank_node.set_value(set_value)
                output_node.links.append(blank_node)
                self._gen(new_node, blank_node, auto=auto)
        else:
            if not (Narrator.IGNORE_REPEAT and new_node in output_node.links):
                blank_node = copy.copy(new_node)
                set_value = Narrator.get_set_value(blank_node, auto)
                if isinstance(set_value, int):
                    blank_node.set_value(set_value)
                    blank_node.clear_vrange()
                output_node.links.append(blank_node)
            else:
                logging.info('IGNORE_REPEAT is True and selection already exists in target')

    # User level wizard generation
    def gen(self):
        ret = False
        while not ret:
            print('\nMake your choice\n')
            ret = self._gen()
            print(self)
