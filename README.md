# WoW-APL-Search
Searches through the space of Action Priority Lists to find the best one.

## APL Codegen (.simc --> .cpp)
APLs are typically written in human-readable form (TCI, aka
[TextualConfigurationInterface](github.com/simulationcraft/simc/wiki/TextualConfigurationInterface)
), usually in files with the `.simc` extension. For example,
[T29_Death_Knight_Unholy.simc](github.com/simulationcraft/simc/blob/84ea508e96575079df70d00c9a2ce61eca3bb7f1/profiles/Tier29/T29_Death_Knight_Unholy.simc):
```
deathknight="T29_Death_Knight_Unholy"
source=default
spec=unholy
level=70
race=troll
role=attack
position=back
talents=BwPAAAAAAAAAAAAAAAAAAAAAAAAIIJJBSAJJRIJSSSkAAAAAAAAAAKJJhIAAgEpkIRSSikA

# Default consumables
potion=elemental_potion_of_ultimate_power_3
# ...

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
# ...

# Executed every time the actor is available.
actions=auto_attack
# ...

# AoE Action List
actions.aoe=any_dnd,if=...
# ...

# Potion
actions.cooldowns=potion,if=...
# Cooldowns
actions.cooldowns+=/vile_contagion,target_if=...
# ...
# Generic
actions.generic=death_coil,if=...
# ...

# Opener
actions.opener=summon_gargoyle,use_off_gcd=1,if=buff.commander_of_the_dead_window.up
# ...

# Racials
actions.racials=arcane_torrent,if=...
# ...

# Trinkets
actions.trinkets=use_item,slot=trinket1,if=...
# ...

head=maw_of_the_haunted_frostbrood,id=200408,bonus_id=4800/4786/1498/6935,gem_id=192985
# ...

# Gear Summary
# gear_ilvl=422.20
# gear_strength=5445
# ...
```

`simc` is converted into `cpp` code via
[ConvertAPL.py](github.com/simulationcraft/simc/blob/dragonflight/engine/class_modules/apl/ConvertAPL.py)

For example,
[apl_death_knight.cpp](https://github.com/simulationcraft/simc/blob/dragonflight/engine/class_modules/apl/apl_death_knight.cpp):
```
#include "class_modules/apl/apl_death_knight.hpp"

#include "player/action_priority_list.hpp"
#include "player/player.hpp"
#include "dbc/dbc.hpp"

namespace death_knight_apl {

std::string potion( const player_t* p )
{
  // ...
}

//blood_apl_start
void blood( player_t* p )
{
  action_priority_list_t* default_ = p->get_action_priority_list( "default" );
  // ...

  precombat->add_action( "flask" );
  // ...

  default_->add_action( "auto_attack" );
  // ...

  drw_up->add_action( "blood_boil,if=!dot.blood_plague.ticking" );
  // ...

  racials->add_action( "blood_fury,if=...");
  // ...

  standard->add_action( "tombstone,if=...");
  // ...

  trinkets->add_action( "use_item,slot=trinket1,if=...");
  // ...
}
//blood_apl_end

//frost_apl_start

// ...

}  // namespace death_knight_apl
```

The C++ code is what's actually used by the simuation.

### SIMC Generation
The `.simc` file that's converted to C++ code is, itself, codegen'd.

There is one file per *class* in `profiles/generators/Tier29/`
that has one section like this per spec (basically just metadata and gear),
e.g. [T29_Generate_Death_Knight.simc](github.com/simulationcraft/simc/blob/84ea508e96575079df70d00c9a2ce61eca3bb7f1/profiles/generators/Tier29/T29_Generate_Death_Knight.simc):
```
deathknight="T29_Death_Knight_Blood"
level=70
race=goblin
spec=blood
role=tank
position=front
talents=BoPAAAAAAAAAAAAAAAAAAAAAAACJRgkEJiEBJikIkkkEBAAAAAQikEEJNJiEAAgIJJJAAAA

head=maw_of_the_haunted_frostbrood,id=200408,bonus_id=4800/4786/1498/1808,gem_id=192925
neck=elemental_lariat,id=193001,bonus_id=8836/8840/8902/8960/8783/8782/8801/8793,ilevel=418,gem_id=192991/192925/192925,crafted_stats=32/36
shoulders=jaws_of_the_haunted_frostbrood,id=200410,bonus_id=4800/4786/1498
back=cape_of_valarjar_courage,id=133765,bonus_id=1795/6808/4786/3156,drop_level=70
chest=breastplate_of_the_haunted_frostbrood,id=200405,bonus_id=1466/8767,ilevel=421,enchant=waking_stats_3
wrists=shackles_of_titanic_failure,id=195533,bonus_id=4800/4786/1498/1808,gem_id=192925
hands=grasps_of_the_haunted_frostbrood,id=200407,bonus_id=1466/8767,ilevel=421
waist=unstable_frostfire_belt,id=191623,bonus_id=8836/8840/8902/8960/8802/8793/1808,ilevel=418,gem_id=192925,crafted_stats=40/49
legs=greaves_of_the_godking,id=133630,bonus_id=1795/6808/4786/3156,enchant=frosted_armor_kit_3,drop_level=70
feet=stonestep_boots,id=143974,bonus_id=4177/6808/4786/3156,enchant=watchers_loam_3,drop_level=70
finger1=jeweled_signet_of_melandrus,id=134542,bonus_id=1795/6808/4786/3156/1808,gem_id=192925,enchant=devotion_of_haste_3,drop_level=70
finger2=seal_of_diurnas_chosen,id=195480,bonus_id=4800/4786/1498/1808,gem_id=192925,enchant=devotion_of_critical_strike_3
trinket1=manic_grieftorch,id=194308,bonus_id=4800/4786/1498
trinket2=windscar_whetstone,id=137486,bonus_id=6652/3300/8767
main_hand=incarnate_skysplitter,id=195528,bonus_id=4800/4786/1498,enchant=rune_of_the_fallen_crusader

save=T29_Death_Knight_Blood.simc
```

There is also a special `.simc` file
[T29_Generate.simc](github.com/simulationcraft/simc/blob/84ea508e96575079df70d00c9a2ce61eca3bb7f1/profiles/generators/Tier29/T29_Generate.simc)
that just includes every profile in the folder, e.g.
```
# ...

# Death Knight
T29_Generate_Death_Knight.simc

# ...
```

For each of those sections, there is a full `.simc` APL in the folder `profiles/Tier29/`,
e.g. `T29_Death_Knight_Unholy.simc` from above.

That "final" profiles are generated by
[generate_profiles.sh](github.com/simulationcraft/simc/blob/e411eeaf76a9322518d719da1c637b2153c2ea7f/generate_profiles.sh),
which boils down to
```
SIMC=${SIMC:-../../engine/simc}
# ...
for tier in 29
do
  PROFDIR="Tier$tier"
  echo "---$PROFDIR---"
  if [ ! -d $PROFDIR ]; then
    echo "Skipped $PROFDIR, directory not found."
    continue
  fi
  cd $PROFDIR/
  ${SIMC} '../generators/Tier'$tier'/T'$tier'_Generate.simc'
  cd ../
done
```

And that uses the

## Info
Python version `3.7.4`.
