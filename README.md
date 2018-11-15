# NarraNG Project

The idea of this tiny project is to be able to generate randomly based contexts and narrative backgrounds

May be used for tabletop gaming or random creativity projects.

## Narrator
The narrator is a background generator
### Usage
Standing in the project's directory, inside `project` folder, create any one folder with a given name, with any amount of subfolders or text files (without any extension).

Such file structure will be utilized as a hierarchy generation tree.

Once `wizard()` is called, user can manually select, or leave empty for a `random` selection

The following example is included within projects (-> denote text file content, or `final_selection`):

```
* Xcom
  * Class
    * -> Sniper
    * -> Assault
  * Spaceship
    * -> Abductor
    * -> Overseer
  * Weapon
    * Pistols
      * -> Ares3
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
# Example usage and results
```python
from NarraNG import Narrator

narrator = Narrator('Xcom')
narrator.wizard()

'''
1. Spaceship Battleship
2. Spaceship Overseer
3. Spaceship Abductor
4. Spaceship Temple Ship
5. Spaceship Supply Barge
6. Spaceship Small Scout
7. Spaceship Large Scout
8. Class MEC Trooper
9. Class Psionic
10. Class Assault
11. Class XCOM Hero
12. Class Heavy
13. Class Sniper
14. Class Support
15. Weapon*

Choose your destiny (empty for random): 
> 3

--------------------
Project Xcom
--------------------
Xcom has Spaceship Abductor
'''

narrator.wizard()

'''
1. Spaceship Battleship
2. Spaceship Overseer
3. Spaceship Abductor
4. Spaceship Temple Ship
5. Spaceship Supply Barge
6. Spaceship Small Scout
7. Spaceship Large Scout
8. Class MEC Trooper
9. Class Psionic
10. Class Assault
11. Class XCOM Hero
12. Class Heavy
13. Class Sniper
14. Class Support
15. Weapon*

Choose your destiny (empty for random):
>

--------------------
Project Xcom
--------------------
Xcom has Spaceship Abductor
Xcom has Class Sniper
'''

narrator.wizard()
'''
1. Spaceship Battleship
2. Spaceship Overseer
3. Spaceship Abductor
4. Spaceship Temple Ship
5. Spaceship Supply Barge
6. Spaceship Small Scout
7. Spaceship Large Scout
8. Class MEC Trooper
9. Class Psionic
10. Class Assault
11. Class XCOM Hero
12. Class Heavy
13. Class Sniper
14. Class Support
15. Weapon*
Choose your destiny (empty for random): >? 15
1. Weapon Pistols Ares3
2. Weapon Pistols Piper
3. Weapon Heavy Bazooka
4. Weapon Heavy Pak81
5. Weapon Rifles*
Choose your destiny (empty for random): >? 5
1. Weapon Rifles Snipers AWP-4
2. Weapon Rifles Snipers Dorsa
3. Weapon Rifles Automatics AK97
4. Weapon Rifles Automatics Nendra11
Choose your destiny (empty for random): >? 3
--------------------
Project Xcom
--------------------
Xcom has Spaceship Abductor
Xcom has Class Sniper
Xcom has Weapon Rifles Automatics AK97
'''
```

## To Do
1. Make wizard capable of going through each of all sections instead of manual selection
2. Export result to file
3. Improve print modularity and story-telling

Author: Saif Ellafi