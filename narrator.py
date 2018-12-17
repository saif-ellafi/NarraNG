import os
import random
import logging
import json
import pprint
logging.getLogger().setLevel(logging.ERROR)


class Narrator:

    PROJECTS_FOLDER = 'projects'
    SUBSECTION_CHAR = '*'
    SELECTION_CHAR = '-'
    COMMENT_CHAR = '#'

    # Represents a narrative selection
    class Selection:
        def __init__(self, name, history):
            self.name = name
            self.history = history

    # Initializes project, path recognition and user input
    def __init__(self, project, name=None):
        self.name = name if name else project
        path = os.path.join(Narrator.PROJECTS_FOLDER, project+'.json')
        if type(project) == dict:
            self.selection_tree = project
        elif type(project) == str:
            with open(path) as file:
                self.selection_tree = json.load(file)
        else:
            raise Exception("Invalid project type")
        self.build = []
        print("""
            Narrator initialized. On wizard, use the following inputs:
                - Number selection
                - Empty For random selection
                - #n to generate n of each possible selection
                - Any text for customized entry
                - 0 to return and do nothing
                """)
        logging.debug("DEBUG MODE ON")

    # How is Narrative represented in console
    def __repr__(self):
        if self.build:
            content = '''--------------------\n{} has:\n--------------------\n{}'''. \
                format(self.name, '\n'.join([str(index+1) + '. ' + ' '.join(selection.history) + ' ' +
                                             selection.name for index, selection in enumerate(self.build)]))
        else:
            content = '''--------------------\n{} is empty\n--------------------'''. \
                format(self.name)
        return content

    @staticmethod
    def projects():
        path = os.path.join(Narrator.PROJECTS_FOLDER)
        prjs = [f[:-5] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.json')]
        return ', '.join(prjs)

        # Handles user's input and validations
    @staticmethod
    def input_callback(max_index):
        while True:
            choice = input().strip()
            if choice == '0':
                logging.debug("exit option selected")
                return 0
            elif choice.startswith('#'):
                logging.debug("# of each")
                try:
                    int(choice[1:])
                    return choice
                except ValueError:
                    pass
            elif not choice:
                logging.debug("single random shot")
                return random.randint(1, max_index)
            else:
                logging.debug("standard input chosen")
                try:
                    if 0 < int(choice) <= max_index:
                        return int(choice)
                except ValueError:
                    if choice:
                        return choice

    def show_tree(self):
        pprint.pprint(self.selection_tree)

    # Clears current selections
    def clear(self):
        logging.debug("Clearing build")
        self.build = []

    # Deletes a specific selection
    def delete(self, index):
        del self.build[index-1]

    # Internal recursive value choice generator
    def _gen(self, level=None, history=None, auto=False):
        level = level if level else self.selection_tree
        level_keys = list(level.keys()) if type(level) == dict else level
        history = history if history else []
        logging.debug("successfully built " + str(len(level_keys)) + ' selections')
        if auto:
            user_choice = random.randint(1, len(level_keys))
        else:
            print('\n'.join([str(i+1) + '. ' + k for (i, k) in enumerate(level_keys)]))
            user_choice = self.input_callback(len(level_keys))
        if user_choice == 0:
            return
        elif str(user_choice).startswith('#'):
            n = int(user_choice[1:])
            for i in range(0, len(level_keys)):
                for _ in range(0, n):
                    chosen_value = level_keys[i]
                    self.handle_choice(level, chosen_value, history, auto=True)
        elif type(user_choice) == str:
            self.build.append(self.Selection(user_choice, history))
            print(self)
        else:
            chosen_value = level_keys[user_choice - 1]
            self.handle_choice(level, chosen_value, history, auto)

    # Internal handled for choice roots
    def handle_choice(self, level, chosen_value, history, auto):
        if type(level) == dict:
            hc = history.copy()
            hc.append(chosen_value)
            self._gen(level[chosen_value], hc, auto=auto)
        else:
            self.build.append(self.Selection(chosen_value, history))

    # User level wizard generation
    def gen(self):
        self._gen()
        print(self)

    # Auto generate n selections
    def mgen(self, n, level=None):
        i = 0
        while i < n:
            self._gen(level, auto=True)
            i += 1
        print(self)
