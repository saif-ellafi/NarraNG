import os


class Project:
    def __init__(self, name, pid):
        self.name = name
        self.pid = pid


class Common:

    PROJECTS_FOLDER = 'projects'

    projects = []

    @staticmethod
    def load_projects():
        if Common.projects:
            return Common.projects
        path = os.path.join(Common.PROJECTS_FOLDER)
        prjs = [f[:-5] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.json')]
        for i, p in enumerate(prjs):
            Common.projects.append(Project(p, i))
        return Common.projects
