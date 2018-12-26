from common import Common
from generator import Generator

# print projects
projects = Common.load_projects()

print("""
==================
NarraNG Generator
==================
""")
print('\n-- Project list --')
for project in projects:
    print(str(project.id+1) + '. ' + str(project.name))
print('\n')
project_name = None
while project_name not in map(lambda p: p.name, projects):
    project_choice = input('Pick a project index to start with or a new project name:\n>> ')
    try:
        project_name = projects[int(project_choice)-1].name
    except ValueError:
        project_name = project_choice
        break
    except IndexError:
        continue

generator = Generator(project_name)

action = None
while action not in ['create', 'load']:
    action = input('%s: create or load?\n>> ' % project_name)

if action == 'create':
    generator.create()
else:
    generator.load()
