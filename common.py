import os
import logging
import json


class Project:
    def __init__(self, name, source, pid):
        self.name = name
        self.source = source
        self.pid = pid


class Common:

    PROJECTS_FOLDER = 'projects'
    OUTPUT_FOLDER = 'output'

    LOG_LEVEL = logging.WARN

    temp_entry = None

    @staticmethod
    def list_dir(path):
        logging.debug("received path", path)
        for f in os.listdir(path):
            t = os.path.join(path, f)
            if os.path.isfile(t) and f.endswith('.json'):
                logging.debug("is json", str(t))
                yield os.path.join(path, f)
            elif os.path.isdir(t):
                logging.debug("is dir", str(t))
                for ff in Common.list_dir(t):
                    yield ff

    @staticmethod
    def load_projects():
        projects = []
        path = os.path.join(Common.PROJECTS_FOLDER)
        prjs = sorted(Common.list_dir(path), key=lambda p: os.path.split(p)[-1])
        for i, p in enumerate(prjs):
            with open(p) as file:
                content = json.load(file)
                projects.append(Project(content['name'], p, i))
        return projects
