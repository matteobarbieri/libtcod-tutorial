# Entities and components

## Example of entities in the game

For each entity type, its component is described.

Each component has a pointer _owner_ to the entity it belongs to.

### Player

Components:

 * _Fighter_
 * _Inventory_
 * _Level_
 * _Equipment_

### Monster

 * _Fighter_
 * _Inventory_
 * _Equipment_
 * _Ai_

### Weapon

 * _Item_
 * _Equippable_

## Components

### Fighter

An entity which has stats such as HP, **STR** etc.; used to represent actual
mobs in the world, including the player itself and various NPCs (monsters
included).

### Item

The properties of the item as a material object, plus its function when _used_
(this is done by associating a function to it).

### Equippable

Represents an item as it is being equipped. Examples are weapons, pieces of
armor, trinkets/gadgets/rings whatever.

### Equipment

### AI

Contains a list of behaviours that instruct the monster on how to respond to
different events (such as seeing the player).
