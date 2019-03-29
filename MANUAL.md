# Rogue 20177

## Introduction

\- "That _did_ hurt"

## Game mechanics

### Time

Time in the game flows in turns. The minimum amount of turns required for taking
an action is **one** turn. As a reference, let's say that 20 turns are roughly
equal to one second (so that quicker actions can be properly divided and require
a smaller amount of turns to be completed).

Any action requires a given amount of time, for instance on a medium/light load
moving one tile (while **walking** normally) takes 20 turns.

Non-combat action are usually interrupted (and items used in the process,
if any, are lost). So maybe find a nice quite spot to tend to that wound ;)

### Stats

 * **Strength** (**STR**): maximum **load**, melee bonus damage
 * **Dexterity** (**DEX**): melee and ranged toHit modifiers.
 * **Intelligence** (**INT**): determines maximum mana points and their recovery
   rate. Also bonus spell damage.
 * **Constitution** (**CON**): determines maximum health points (**HP**), Stamina points and their recovery rate.

### Classes

 * Technomancer: magic/tech
 * Specialist: tech
 * Arcanist: magic
 * Enforcer: strength
 * Shadow: agility
 * Cyborg: tech/strength
 * Spellslinger: magic/agility

### Skills

#### Weapons proficiencies

 * Guns
 * Rifles
 * Swords
 * Maces
 * Daggers
 * Unarmed

#### Combat

##### Melee

 * **Charge!**: quickly move towards a target, following it if it moves, and
   receiving a bonus on hit and damage on first melee attack. Cannot be
   performed while bleeding, poisoned, blinded or chilled.
 * **Heavy strike**: for a small negative modifier on roll to hit, deal 150%
   damage.

##### Ranged

 * **Headshot**: (requires _rifle_) take your time and receive a bonus to hit
   and damage. At higher levels grants a small chance to vanquish smaller
   creatures (like 5 levels below player's level) on hit (no need to roll
   for damage).
 * **Point blank**: use your gun(s) while in melee combat without suffering from
   negative modifiers due to being in melee.

##### Misc

 * **Dodge this!** (requires player level 5+) (_passive_):

#### Survival

 * Discover traps/secret doors
 * Stealth (*passive*): make less noise while moving, other entities do not see
   you if you're too far away.

### Spells

 * Light: creates a source of light attached to an entity. At higher levels has
   a chance to blind if cast directly on a creature.
 * Lightning: chance to stun the enemy for a given number of turns.
 * Fireball:
 * Ice blast: deal cold

## Combat system

An attack (either a melee or a ranged one) works in the following way:

 1. Roll to hit.
    1. Start from base roll to hit (based on weapon proficiency).
    1. Apply toHit modifiers (source, target, environment and effective ranged
      for ranged weapons).
    1. If target is hit, determine damage.
 2. Compute damage
    1. Start from base damage (based on weapon)
    2. Apply modifiers (from either player or weapon)

_Environment_ modifiers might be for instance being close to a wall (and the wall being between you and the target, or being hidden in a thick bush or in a cloud of smoke).

Damage is divided based on its type:

 * Physical: coming from most melee attacks and regular weapons
 * Elemental: one of several types
   - Fire: chance to **ignite** target.
   - Cold: chance to **chill** target.
   - Electricity: chance to **shock** target.
 * Arcane: caused by spells mostly

### Ailments

As a secondary effect, some attacks may inflict different types of ailments to
an entity (either the player or a monster).

Most of them cause the player to lose a certain amount of health every turn,
and must be treated by using the appropriate item/skill.

 * Burning: every turn the entity receives damage.
 * Bleeding:
 * Chilled:
 * Poisoned:
 * Blinded: reduced vision of the surroundings, plus can only shoot at a
   direction.
