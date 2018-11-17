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

    # Initializes project, path recognition and user input
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

    # Represents a narrative selection
    class Selection:
        def __init__(self, name, path, state):
            self.name = name
            self.path = path
            self.state = state

    # Represents project walk through and selection generation
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

    # Represents final file node walk through
    class LeafWizard(Wizard):
        def __init__(self):
            super(Narrator.LeafWizard, self).__init__()

        def build_selections(self, path, callback_name=None):
            with open(path) as file:
                for line in file:
                    name = (callback_name + ' ' + line if callback_name else line).strip()
                    self.selections.append(Narrator.Selection(name, path, state=2))

    # Clears current selections
    def clear(self):
        logging.debug("Clearing build")
        self.build = []

    # Deletes a specific selection
    def delete(self, index):
        del self.build[index-1]

    # Given a specific selection, handles next step
    def resolve(self, selection, auto=False):
        if selection.state == Narrator.ROOT:
            logging.debug("Go back to wizard, since selection is not final")
            self.gen(Narrator.Wizard, selection.path, selection.name, auto)
        elif selection.state == Narrator.LAST_NODE:  # Selection is last root. Call leaf wizard.
            logging.debug("selection identified as last root. Go to leaf wizard")
            self.gen(Narrator.LeafWizard, selection.path, selection.name, auto)
        elif selection.state == Narrator.LEAF:  # Selection is leaf. stop here
            logging.debug("selection identified as leaf. printing.")
            self.build.append(selection)
        else:
            logging.debug("result is set from standard input")
            self.build.append(selection)

    # Handles user's input and validations
    @staticmethod
    def input_callback(max_index):
        while True:
            choice = input().strip()
            if choice == '0':
                logging.debug("exit option selected")
                return 0
            elif choice.startswith('#'):
                try:
                    int(choice[1:])
                    return choice
                except ValueError:
                    pass
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

    # Creates a wizard and starts user interaction for selections
    def gen(self, wizard=Wizard, root_path=None, callback_name=None, auto=False):
        wiz = wizard()
        path = root_path if root_path else self.project_path
        logging.debug("Created wizard. Building from " + str(path) + ' ...')
        wiz.build_selections(path, callback_name)
        logging.debug("successfully built " + str(len(wiz.selections)) + ' selections')
        if auto:
            user_choice = random.randint(1, len(wiz.selections))
        else:
            print('\n'.join([str(index+1) + '. ' + selection.name +
                             ('*' if selection.state in [Narrator.ROOT, Narrator.LAST_NODE] else '')
                             for index, selection in enumerate(wiz.selections)])
                  )
            user_choice = Narrator.input_callback(len(wiz.selections))
        if user_choice == 0:
            return
        elif str(user_choice).startswith('#'):
            n = int(user_choice[1:])
            for i in range(0, len(wiz.selections)):
                for ii in range(0, n):
                    self.resolve(wiz.selections[i], auto=True)
        elif type(user_choice) == str:
            self.resolve(self.Selection(user_choice, '', self.LEAF), auto=auto)
        else:
            self.resolve(wiz.selections[user_choice-1], auto=auto)

    # Creates n wizards for multiple automated selections
    def mgen(self, n, wizard=Wizard, root_path=None, callback_name=None):
        i = 0
        while i < n:
            self.gen(wizard, root_path, callback_name, auto=True)
            i += 1
        self.print()

    # How is Narrative represented in console
    def __repr__(self):
        return '''--------------------\nProject {} has:\n--------------------\n{}'''. \
            format(self.name, '\n'.join([str(index+1) + '. ' + selection.name for index, selection in enumerate(self.build)]))

    def print(self):
        print(self.__repr__())
