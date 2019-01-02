from common import Common
from narrator import Narrator

# print projects
projects = Common.load_projects()

print("""
==================
NarraNG Narrator
==================
""")
print('\n-- Project list --')
for project in projects:
    print(str(project.pid+1) + '. ' + str(project.name))
print('\n')
project = None
while project not in projects:
    project_choice = input('Pick a project index to start with:\n>> ')
    try:
        project = projects[int(project_choice) - 1]
        break
    except ValueError:
        continue
    except IndexError:
        continue

target_name = input('Enter a target name for %s:\n>> ' % project.name)
if not target_name:
    target_name = None

narrator = Narrator(project.source, target_name)
narrator.gen()
