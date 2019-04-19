
## General

There is the usual "dungeon" layer, that is the character diving through several
levels. However the game is imagined to be played over a series of _contracts_,
that is game sessions that will consist of an overall limited number of levels.

Each contract will have a primary goal and possibly several (a couple) secondary
goals.

Example missions:

 - Clear alien nests
 - Rescue VIP
 - Retrieve data disk
 - Recover tissue sample

The time passes after each mission, and the main story unrolls.

Q: How to make the story (slightly) different every time?
A: Procedurally generated story? How?

Q: Why should a player stop doing low-level contracts and hoarding credits? Is
there any kind of strategy layer-level _food clock_?
A: ...

- The goal is to have the player being able to play effectively using a regular
  XBOX-like controller (or at least the same amount of inputs).
- Boss fights?

## Game mechanics

How about NOT having stats at all, meaning that it is automatically assumed that
a character of a given class would have no reason to increase stats that are not
their main one?

Or maybe providing sort of templates but not a real class system?

### Combat

 * **Melee**: hitting is relatively easy (let's say base 75% chance), moderate
   amount of damage.
 * **Ranged**: hitting is less easy without a decent bonus in precision (given
   by weapon/stats/range). Firing rate depends on weapon.
 * **Ability/spell**: hitting is almost automatic, also damage dealt is usually
   high, however there is a limit to the frequency of attacks due to 
   _cooldown_/_energy cost_.
 * **Pets/turrets**: Sort of constant _DOT_, however the final blow most of the
   times will have to be inflicted by the player.

In case the enemy has multiple viable targets (i.e. the player and his/her
minions/pets/mercenaries), use a smart threat system to choose the target (and
possibly stick to it after that, it would not really make sense for a mob to
continuously switch target).



### Factions

There are several factions (not many). Accepting some contracts instead of
others may influence the _reputation_, which in turns may lock/unlock
purchasable upgrades.

## Classes

It might make sense to think of four base classes (each based on one of the main
stats (**STR**, **DEX**, **TCH**, **ARC**) and give the player the possibility
to choose a sort of a secondary class later in the game.

## Abilities/spells

Divided in three scopes:

 * Offense
 * Defense
 * Mobility
 * Support

## Strategy Layer

### Activities

 - Choose next contract
 - Level up/spend gained ability
 - Improve facility?
 - Recruit mercenaries

## Dungeon Layer

### Fighting styles

In general there should be a way for each class to face encounters so that they
of course survive, possibly taking a few hits which the very low health regen
system (if any at all) will let them recover before the next encounter.

#### Enforcer

Strength based class.

- Mainly a melee fighter.
- Has access to heavy armor and an overall larger health  pool, which means he'll
  be able to take more hits (and armor decreases damage taken).

Q: Could there be any reason for an Enforcer to prefer ranged play style?
A: ...

#### Arcanist

Arcane based class.

- Ability based fighter.
- Can only wear light armor.
- High risk-high reward class, deals a lot of damage but is more fragile.

#### Specialist

Tech based class.

- Can wear light and medium armor.
- Fighting style based on accessories.

## Misc

 - No max weight (tesseract inventory), however relatively limited amount of
   inventory space (possibly upgradable?)
 - No base health regen (or maybe very little?), it is however possible to
   regain health through (very rare) medkits and one-use health stations
   sometimes found throughout the level.
