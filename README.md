# NarraNG Project

The idea of this tiny project is to be able to generate randomly based contexts and narrative backgrounds

May be used for tabletop gaming or random creativity projects.

## Narrator
The narrator is a background generator
### Usage
Standing in the project's directory, inside `project` folder, create any one folder with a given name, with any amount of subfolders or text files (without any extension).

Such file structure will be utilized as a hierarchy generation tree.

```
* Xcom (Root folder, project name)
  * Class (File called 'Class')
    * -> Medic (File content)
    * -> Grenadier (File content)
  * Spaceship (Another File)
    * -> Abductor
    * -> Overseer
  * Weapon (A subfolder)
    * Pistols (File inside subfolder)
      * -> Ares3 (content)
      * -> Viper
    * Heavy
      * -> Bazooka
      * -> Pak81
    * Rifles
      * Automatics
        * -> AK97
        * -> Nendra11
      * Snipers
        * -> AWP-4
        * -> Dorsa
```

Import and start a narrator, indicating the name of the project you want to use (folder under project) and the target name (this is made up by user). Just as follows:

```python
from narrator.narrang import Narrator
narrator = Narrator("Xcom", "Robert Baratheon")
```

then call `gen()` to get it kicked. At any time of the wizard you can either:

1. Leave empty for random selection
2. Enter the index choice you decide
3. Enter a custom input you'd like to have

or call `mgen(n=3)` to generate #n random choices

print the narrator any time to show selections content
        
# Example usage and results
```python
from narrator.narrang import Narrator
narrator = Narrator("Xcom", "Robert Baratheon")
'''
            Narrator initialized. On wizard, use the following inputs:
                - Number selection
                - Empty For random selection
                - Any text for customized entry
                - 0 to return and do nothing
'''
                
narrator.gen()
'''
1. Spaceship*
2. Class*
3. Weapon*
>> 2

1. Class MEC Trooper
2. Class Psionic
3. Class Assault
4. Class XCOM Hero
5. Class Heavy
6. Class Sniper
7. Class Support
>>3
'''

narrator.gen()
'''
1. Spaceship*
2. Class*
3. Weapon*
>> 3

1. Weapon Pistols*
2. Weapon Heavy*
3. Weapon Rifles*
>> 3

1. Weapon Rifles Snipers*
2. Weapon Rifles Automatics*
>> 1

1. Weapon Rifles Snipers AWP-4
2. Weapon Rifles Snipers Dorsa
>> 1
'''
print(narrator)
'''
--------------------
Project Robert Baratheon has:
--------------------
1. Class Assault
2. Weapon Rifles Snipers AWP-4
'''
```

## To Do
1. Export result to file with format
2. Add weights or strategies for random choices
3. Improve story-telling

Author: Saif Ellafi