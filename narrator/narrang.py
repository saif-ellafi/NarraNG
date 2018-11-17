import os
import random
import logging


logging.getLogger().setLevel(logging.INFO)


class Narrator:

    PROJECTS_FOLDER = 'projects'
    SUBSECTION_CHAR = '*'
    SELECTION_CHAR = '-'
    COMMENT_CHAR = '#'

    ROOT = 0
    LAST_NODE = 1
    LEAF = 2

    def __init__(self, project, name=None):
        self.name = name if name else project
        self.project = project
        self.project_path = os.path.join(Narrator.PROJECTS_FOLDER, project)
        self.sections = [
            section for section in os.listdir(self.project_path)
            if os.path.isfile(os.path.join(self.project_path, section))
        ]
        self.build = []
        print("""
            Narrator initialized. On wizard, use the following inputs:
                - Number selection
                - Empty For random selection
                - Any text for customized entry
                - 0 to return and do nothing
                """)
        logging.debug("DEBUG MODE ON")

    class Selection:
        def __init__(self, name, path, state):
            self.name = name
            self.path = path
            self.state = state

    class Wizard:
        def __init__(self):
            self.selections = []

        def build_selections(self, target, callback_name=None):

            logging.debug("Loading and printing sections from '" + str(target) + "'")

            for section in os.listdir(target):
                path = os.path.join(target, section)
                is_leaf = os.path.isfile(path)
                name = (callback_name + ' ' + section if callback_name else section).strip()
                logging.debug("Generated entry with name: " + str(name) + " at path: " + str(path))
                self.selections.append(Narrator.Selection(name, path, state=1 if is_leaf else 0))
                print(str(len(self.selections)) + '. ' + name + '*')

    class LeafWizard(Wizard):
        def __init__(self):
            super(Narrator.LeafWizard, self).__init__()

        def build_selections(self, path, callback_name=None):
            with open(path) as file:
                for line in file:
                    name = (callback_name + ' ' + line if callback_name else line).strip()
                    self.selections.append(Narrator.Selection(name, path, state=2))
                    print(str(len(self.selections)) + '. ' + name)

    @staticmethod
    def input_callback(max_index):
        while True:
            choice = input().strip()
            if choice == '0':
                logging.debug("exit option selected")
                return 0
            elif not choice:
                logging.debug("single random shot. Setting randomized choices to 1")
                return random.randint(1, max_index)
            else:
                logging.debug("standard input chosen")
                try:
                    if 0 < int(choice) <= max_index:
                        return int(choice)
                except ValueError:
                    if choice:
                        return choice

    def clear(self):
        logging.debug("Clearing build")
        self.build = []

    def delete(self, index):
        del self.build[index-1]

    def resolve(self, selection):
        if selection.state == Narrator.ROOT:
            logging.debug("Go back to wizard, since selection is not final")
            self.gen(Narrator.Wizard, selection.path, selection.name)
        elif selection.state == Narrator.LAST_NODE:  # Selection is last root. Call leaf wizard.
            logging.debug("selection identified as last root. Go to leaf wizard")
            self.gen(Narrator.LeafWizard, selection.path, selection.name)
        elif selection.state == Narrator.LEAF:  # Selection is leaf. stop here
            logging.debug("selection identified as leaf. printing.")
            self.build.append(selection)
        else:
            logging.debug("result is set from standard input")
            self.build.append(selection)

    def gen(self, wizard=Wizard, root_path=None, callback_name=None):
        print('\n')
        wiz = wizard()
        path = root_path if root_path else self.project_path
        logging.debug("Created wizard. Building from " + str(path) + ' ...')
        wiz.build_selections(path, callback_name)
        logging.debug("successfully built " + str(len(wiz.selections)) + ' selections')
        user_choice = Narrator.input_callback(len(wiz.selections))
        if user_choice == 0:
            return
        elif type(user_choice) == str:
            self.resolve(self.Selection(user_choice, '', self.LEAF))
        else:
            self.resolve(wiz.selections[user_choice-1])

    def __repr__(self):
        return '''--------------------\nProject {} has:\n--------------------\n{}'''. \
            format(self.name, '\n'.join([str(index+1) + '. ' + selection.name for index, selection in enumerate(self.build)]))

    def print(self):
        print(self.__repr__())
