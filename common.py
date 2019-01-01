import os
import logging


class Project:
    def __init__(self, name, source, pid):
        self.name = name
        self.source = source
        self.pid = pid


class Common:

    PROJECTS_FOLDER = 'projects'
    OUTPUT_FOLDER = 'output'

    LOG_LEVEL = logging.DEBUG

    temp_entry = None

    @staticmethod
    def list_dir(path):
        print("received path", path)
        for f in os.listdir(path):
            t = os.path.join(path, f)
            if os.path.isfile(t) and f.endswith('.json'):
                print("is json", str(t))
                yield os.path.join(path, f)
            elif os.path.isdir(t):
                print("is dir", str(t))
                for ff in Common.list_dir(t):
                    yield ff

    @staticmethod
    def load_projects():
        projects = []
        path = os.path.join(Common.PROJECTS_FOLDER)
        prjs = sorted(Common.list_dir(path))
        for i, p in enumerate(prjs):
            logging.debug("Adding project path %s with name %s and id %i" % (p, os.path.split(p)[-1][:-5], i))
            projects.append(Project(os.path.split(p)[-1][:-5], p, i))
        return projects
