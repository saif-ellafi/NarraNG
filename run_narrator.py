from common import Common
from narrator import Narrator

# print projects
projects = Common.projects()

print("""
==================
NarraNG Narrator
==================
""")
print('\n-- Project list --')
print('\n'.join(projects))
print('\n')
project_name = None
while project_name not in projects:
    project_name = input('Pick a project to start with:\n>> ')

happy = 'n'
target_name = input('Enter a target name for this narrator:\n>> ')
if not target_name:
    target_name = None

narrator = Narrator(project_name, target_name)
narrator.gen()
