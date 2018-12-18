import os


class Common:

    PROJECTS_FOLDER = 'projects'

    @staticmethod
    def projects():
        path = os.path.join(Common.PROJECTS_FOLDER)
        prjs = [f[:-5] for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.endswith('.json')]
        return prjs
