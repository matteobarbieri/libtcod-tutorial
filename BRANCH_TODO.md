### Next

* Implement base stats (**STR**, **INT**, **DEX**) for _fighter_ component.

### Backlog

* Doors must be entities, and block LoS when closed.
* Corridors widths should be weighted, that is the average width should be more
  likely than extreme values.
* Also directions taken should be weighted, in order to sort of control the
  general geometry of the level.
* Add support for animated tiles.
* Refine entity details frame:
  - Add graphical representation of the focused entity.
  - Add relevant info lines for the entity.
* A junction should have a minimun size of 2+ the width of the corridor it
  originates from.

### Done

* Show current turn number somewhere on the UI
* An entity can be selected, and its frame be shown.
* Equipment slots must be dynamic
