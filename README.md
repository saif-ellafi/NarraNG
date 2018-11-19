# NarraNG Project

The idea of this tiny project is to be able to generate randomly based contexts and narrative backgrounds

May be used for tabletop gaming or random creativity projects.

## Narrator
The narrator is a background generator
### Usage
Put json in `/project` and pass it's name (without `.json`) as project argument to narrator.

Import and start a narrator, indicating the name of the project you want to use (folder under project) and the target name (this is made up by user). Just as follows:

```python
from narrator.narrang import Narrator
narrator = Narrator("XCOM", "Robert Baratheon")
```

Such project structure will be utilized as a hierarchy generation tree.

Example `XCOM.json`

```json
{
  "Weapon": {
    "Rifles": {
      "Automatics": ["AK47", "Manning71"],
      "Snipers": ["AWP-4", "SNEAK1"]
    },
    "Heavy": ["Desert", "LOGGA"],
    "Pistols": ["Ares", "NogaPIP"]
  },
  "Class": ["Grenadier", "Medic"],
  "Spaceship": ["Destroyer", "Warship"]
}
```

then call `narrator.gen()` to get it kicked. At any time of the wizard you can either:

1. Leave empty for random selection
2. Enter the index choice
3. Enter #n to generate n of each of the possible selections
4. Enter a custom input you'd like to have
5. 0 to return and do nothing

or call `narrator.mgen(n=3)` to generate #n random choices

print the narrator any time to show selections content
        
# Example usage and results
```python
from narrator.narrang import Narrator
narrator = Narrator("XCOM", "Robert Baratheon")
'''
            Narrator initialized. On wizard, use the following inputs:
                - Number selection
                - Empty For random selection
                - #n to generate n of each possible selection
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