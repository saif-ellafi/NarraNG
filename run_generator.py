from common import Common
from generator import Generator

# print projects
projects = Common.projects()

print("""
==================
NarraNG Generator
==================
""")
print('\n-- Project list --')
print('\n'.join(projects))
print('\n')
project_name = input('Pick a project to start with:\n>> ')
print('\nProject name chosen: %s\n' % project_name)

generator = Generator(project_name)

action = None
while action not in ['create', 'load']:
    action = input('create or load?\n>> ')

if action == 'create':
    generator.create()
else:
    generator.load()
