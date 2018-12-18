# NarraNG Project

The idea of this tiny project is to be able to generate randomly based contexts and narrative backgrounds

May be used for tabletop gaming or random creativity projects.

## NarraNG
The narrator is a background inventor. The generator creates a structure for the narrator to use.
The structure is made of Nodes with particular properties in order to make sense for a given narration.

These tools work under command-line only. No plans for a GUI yet.

### Usage
Use the Generator to build node structures (*Projects*). Then, the narrator will use these projects to create narrations.

The following scripts are wizards that will guide you through the process.

Run `python run_generator.py` and follow instructions to generate a `.json` structure

Run `python run_narrator.py` and follow instructions to generate content

### Generator
The generator allows you to create and edit `.json` structures in a very easy way to use it on the Narrator later.
You can create LinkNodes (which contain sub-nodes) or LeafNodes which are end-point contents.
It allows you to easily load and continue your work later as well, and focuses on ease-of-use and fast data-entry.

### Narrator
The narrator will use a generated `.json` project and will allow the user to manually or automatically generate a target narration.
The wizard allows you to test and generate multiple aspect combinations of your target narration.
It focuses on customization and ease of use.

### Details
### Node
Node represents a data structure similar to a graph
* root: it points to the upper level node (for root, it is itself)
* name: text representation
* weight: random probability weight. Defaults to 1.0
### LinkNode (Node)
LinkNode is a structure that contains multiple nodes within
* links: points to all sub-nodes
* bound: a property that applies only when generating randomly
  * `single` when the LinkNode allows only one sub-node
  * `many` when the LinkNode may have more than one sub-node
  * `all` when the LinkNode must have all sub-nodes
### LeafNode (Node)
LeafNode represents the endpoint of a node structure. Also called a Selection.

### Example output
The following example shows an XCOM like character.

*Class* is a `single` _LinkNode_. *Weapon* is a `many` _LinkNode_. *Appearance* is a `all` _LinkNode_.

On the other hand *Heavy* is a *Class* _LeafNode_ as *Mauzer 95* is a *Weapon* _LeafNode_
```
    --------------------
    Baum Robertson (XCOM) has:
    --------------------
    1. Class Heavy
    2. Weapon Colt 2071
    3. Weapon Mauzer 95
    4. Appearance Hair Color Black
    5. Appearance Eye Color Blue
```

### To do
* agregar delete en generator
* mejorar textos y tabulacion
* decoder poner leaves al final
* si es single o all, no pedir qrange
* si es many, tomar el qrange. generar entre min-max
* many choices, combinarlas por el history
* anidar node arboles 
* poder cancelar

Author: Saif Addin Ellafi