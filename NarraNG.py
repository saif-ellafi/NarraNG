import os
import random


class Narrator:

    PROJECTS_FOLDER = 'projects'
    SUBSECTION_CHAR = '*'
    SELECTION_CHAR = '-'
    COMMENT_CHAR = '#'

    def __init__(self, project, name=None):
        self.name = name if name else project
        self.project = project
        self.project_path = os.path.join(Narrator.PROJECTS_FOLDER, project)
        self.sections = [
            section for section in os.listdir(self.project_path)
            if os.path.isfile(os.path.join(self.project_path, section))
        ]
        self.build = []

    class Selection:
        def __init__(self, name, path, is_final):
            self.name = name
            self.path = path
            self.is_final = is_final

    def clear(self):
        self.build = []

    def wizard(self, subsection=None):
        index = 0
        selection = {}
        target = self.project_path if not subsection else os.path.join(self.project_path, subsection)
        print('\n')

        for section in os.listdir(target):
            path = os.path.join(target, section)
            is_final = os.path.isfile(path)
            if is_final:
                with open(path) as file:
                    for line in file:
                        index += 1
                        selection_name = (('' if not subsection else subsection.replace('/', ' '))
                                          + ' ' + section + ' ' + line).strip()
                        selection_path = section if not subsection else os.path.join(subsection, section)
                        selection[index] = Narrator.Selection(selection_name, selection_path, is_final)
                        print(str(index) + '. ' + selection_name)
            else:
                index += 1
                selection_name = (('' if not subsection else subsection.replace('/', ' ')) + ' ' + section).strip()
                selection_path = section if not subsection else os.path.join(subsection, section)
                selection[index] = Narrator.Selection(selection_name, selection_path, is_final)
                print(str(index) + '. ' + selection_name + '*')

        while True:
            print('\n')
            choice = input("Choose your destiny (empty for random): ")
            if not choice:
                result = random.randint(1, index)
                break
            else:
                try:
                    result = int(choice)
                    if 0 < result <= index:
                        break
                except ValueError:
                    pass

        if selection[result].is_final:
            self.build.append(selection[result].name)
            self.print()
        else:
            self.wizard(selection[result].path)

    def print(self):
        print('\n')
        print('--------------------')
        print('Project ' + self.name)
        print('--------------------')
        for element in self.build:
            print(self.name + ' has ' + element)
