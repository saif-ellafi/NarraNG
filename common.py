import os


class Project:
    def __init__(self, name, pid):
        self.name = name
        self.pid = pid


class Common:

    PROJECTS_FOLDER = 'projects'

    @staticmethod
    def load_projects():
        projects = []
        path = os.path.join(Common.PROJECTS_FOLDER)
        prjs = sorted([f[:-5] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.json')])
        for i, p in enumerate(prjs):
            projects.append(Project(p, i))
        return projects
