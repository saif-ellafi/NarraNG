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
    print(str(project.id+1) + '. ' + str(project.name))
print('\n')
project_name = None
while project_name not in projects:
    project_choice = input('Pick a project index to start with:\n>> ')
    try:
        project_name = projects[int(project_choice)-1].name
    except ValueError:
        continue
    except IndexError:
        continue

target_name = input('Enter a target name for %s:\n>> ' % project_name)
if not target_name:
    target_name = None

narrator = Narrator(project_name, target_name)
narrator.gen()
