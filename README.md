# NarraNG Project

The idea of this tiny project is to be able to generate randomly based contexts and narrative backgrounds

May be used for tabletop gaming or random creativity projects.

## NarraNG
NarraNG is an inventor program. Users call the `Generator` to create narrative structure. Next, the `Narrator` generates interesting combination of these structures!

`Nodes` are created with particular properties in order maximize customization and randomness.

* The `Generator` is a step-by-step wizard and may only be used from a console.

* The `Narrator` has both a simple web interface to go through and a command line wizard for more customization.


### Requirements and quick-guide
Someday I'll make this easier for non technical people
1. Install [Python 3](https://www.python.org/downloads/release/python-372/)
2. Install [Git](https://git-scm.com/downloads)
3. Open Windows `Command Prompt` or any `terminal`
4. Clone this project `git clone https://github.com/revolucion09/NarraNG.git`
5. Enter the project folder `cd NarraNG`
6. Install Django to run the web service program `python -m pip install django`
7. Start the web server with `python manage.py runserver`
8. Open a browser and go to `http://localhost:8000`

### Usage
Use the Generator to build node structures (*Projects*).

The narrator will use these projects to create narrations.

You can skip the `Generator` and begin with provided examples on the `Narrator`

#### Generator

The following script will guide you through the process of creation. Follow instructions to use.

Run `python run_generator.py` from a `terminal` and follow instructions to generate a structure

You can create LinkNodes (which contain sub-nodes) or LeafNodes which are end-point contents.

It allows you to easily load and continue your work later as well, and focuses on ease-of-use and fast data-entry.

`LinkNodes` have:
* __name__: Main name for the node
* __bound__: either `all`, `single` or `many` depending on how many sub elements this node will have
* __weight__: (Only if parent __bound__ is `many` or `single`) How probable is this node to be chosen
* __qrange__: if __bound__ was `many`, how many? can be a range with an average provided point
* __vrange__: (Optional) element that gives this node a number within a range
* __description__: (Optional) element that describes the node

`LeafNodes` have:
* __name__: Main name for the node
* __weight__: (Only if parent __bound__ is `many` or `single`) How probable is this node to be chosen
* __vrange__: (Optional) element that gives this node a number within a range
* __description__: (Optional) element that describes the node


#### Narrator
It generates random narrations from generated structures. Can be used from a browser or console.

1. Start the web server with `python manage.py runserver`
2. Open a browser and go to `http://localhost:8000`
3. Follow the site. It's intuitive.

Run `python run_narrator.py` from a `terminal` and follow instructions to generate a narration

### Example output
The following example shows an XCOM like character.

*Class* is a `single` _LinkNode_. *Weapon* is a `many` _LinkNode_. *Appearance* is a `all` _LinkNode_.

On the other hand *Heavy* is a *Class* _LeafNode_ as *Mauzer 95* is a *Weapon* _LeafNode_
```
    Concealable Pistol (( Light Pistols ))
    	Taurus Omni-6  (( ACC5/SG6 6/7P AP0/-1 SA/SS ))
    		Concealable Holster  (( -1 conceal. Wireless -1 color camouflage conceal ))

```

Author: Saif Addin Ellafi