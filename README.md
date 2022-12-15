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
flask=phial_of_static_empowerment_3
food=fated_fortune_cookie
augmentation=draconic
temporary_enchant=main_hand:howling_rune_3

# This default action priority list is automatically created based on your character.
# It is a attempt to provide you with a action list that is both simple and practicable,
# while resulting in a meaningful and good simulation. It may not result in the absolutely highest possible dps.
# Feel free to edit, adapt and improve it to your own needs.
# SimulationCraft is always looking for updates and improvements to the default action lists.

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
# ...

# Executed every time the actor is available.
actions=auto_attack
# ...

# AoE Action List
actions.aoe=any_dnd,if=!death_and_decay.ticking&variable.adds_remain&(talent.festermight&buff.festermight.remains<3|!talent.festermight)&(death_knight.fwounded_targets=active_enemies|death_knight.fwounded_targets=8|!talent.bursting_sores&!talent.vile_contagion|raid_event.adds.exists&raid_event.adds.remains<=11&raid_event.adds.remains>5|(cooldown.vile_contagion.remains|!talent.vile_contagion)&buff.dark_transformation.up&talent.infected_claws&(buff.empower_rune_weapon.up|buff.unholy_assault.up))|fight_remains<10
# ...

# Potion
actions.cooldowns=potion,if=(30>=pet.gargoyle.remains&pet.gargoyle.active)|(!talent.summon_gargoyle|cooldown.summon_gargoyle.remains>60)&(buff.dark_transformation.up&30>=buff.dark_transformation.remains|pet.army_ghoul.active&pet.army_ghoul.remains<=30|pet.apoc_ghoul.active&pet.apoc_ghoul.remains<=30)|fight_remains<=30
# Cooldowns
actions.cooldowns+=/vile_contagion,target_if=max:debuff.festering_wound.stack,if=active_enemies>=2&debuff.festering_wound.stack>=4&cooldown.any_dnd.remains<3
# ...
# Generic
actions.generic=death_coil,if=!variable.pooling_runic_power&(rune<3|pet.gargoyle.active|buff.sudden_doom.react)
actions.generic+=/any_dnd,if=!death_and_decay.ticking&active_enemies>=2&death_knight.fwounded_targets=active_enemies
actions.generic+=/wound_spender,target_if=max:debuff.festering_wound.stack,if=variable.pop_wounds|active_enemies>=2&death_and_decay.ticking
actions.generic+=/festering_strike,target_if=min:debuff.festering_wound.stack,if=!variable.pop_wounds
actions.generic+=/death_coil

# Opener
actions.opener=summon_gargoyle,use_off_gcd=1,if=buff.commander_of_the_dead_window.up
actions.opener+=/potion,if=pet.gargoyle.active|!talent.summon_gargoyle&pet.army_ghoul.active|!talent.summon_gargoyle&!talent.army_of_the_dead&buff.dark_transformation.up
actions.opener+=/death_coil,if=pet.gargoyle.active&!prev_gcd.1.death_coil
actions.opener+=/apocalypse,if=buff.commander_of_the_dead_window.up
actions.opener+=/dark_transformation,if=debuff.festering_wound.stack>=4
actions.opener+=/festering_strike,target_if=min:debuff.festering_wound.stack,if=!variable.pop_wounds
actions.opener+=/variable,name=opener_done,op=setif,value=1,value_else=0,condition=cooldown.apocalypse.remains|!talent.apocalypse&(cooldown.dark_transformation.remains|cooldown.summon_gargoyle.remains)

# Racials
actions.racials=arcane_torrent,if=runic_power.deficit>20&(cooldown.summon_gargoyle.remains<gcd|!talent.summon_gargoyle.enabled|pet.gargoyle.active&rune<2&debuff.festering_wound.stack<1)
actions.racials+=/blood_fury,if=(buff.blood_fury.duration>=pet.gargoyle.remains&pet.gargoyle.active)|(!talent.summon_gargoyle|cooldown.summon_gargoyle.remains>60)&(buff.dark_transformation.up&buff.blood_fury.duration>=buff.dark_transformation.remains|pet.army_ghoul.active&pet.army_ghoul.remains<=buff.blood_fury.duration|pet.apoc_ghoul.active&pet.apoc_ghoul.remains<=buff.blood_fury.duration|active_enemies>=2&death_and_decay.ticking)|fight_remains<=buff.blood_fury.duration
actions.racials+=/berserking,if=(buff.berserking.duration>=pet.gargoyle.remains&pet.gargoyle.active)|(!talent.summon_gargoyle|cooldown.summon_gargoyle.remains>60)&(buff.dark_transformation.up&buff.berserking.duration>=buff.dark_transformation.remains|pet.army_ghoul.active&pet.army_ghoul.remains<=buff.berserking.duration|pet.apoc_ghoul.active&pet.apoc_ghoul.remains<=buff.berserking.duration|active_enemies>=2&death_and_decay.ticking)|fight_remains<=buff.berserking.duration
actions.racials+=/lights_judgment,if=buff.unholy_strength.up&(!talent.festermight|buff.festermight.remains<target.time_to_die|buff.unholy_strength.remains<target.time_to_die)
actions.racials+=/ancestral_call,if=(15>=pet.gargoyle.remains&pet.gargoyle.active)|(!talent.summon_gargoyle|cooldown.summon_gargoyle.remains>60)&(buff.dark_transformation.up&15>=buff.dark_transformation.remains|pet.army_ghoul.active&pet.army_ghoul.remains<=15|pet.apoc_ghoul.active&pet.apoc_ghoul.remains<=15|active_enemies>=2&death_and_decay.ticking)|fight_remains<=15
actions.racials+=/arcane_pulse,if=active_enemies>=2|(rune.deficit>=5&runic_power.deficit>=60)
actions.racials+=/fireblood,if=(buff.fireblood.duration>=pet.gargoyle.remains&pet.gargoyle.active)|(!talent.summon_gargoyle|cooldown.summon_gargoyle.remains>60)&(buff.dark_transformation.up&buff.fireblood.duration>=buff.dark_transformation.remains|pet.army_ghoul.active&pet.army_ghoul.remains<=buff.fireblood.duration|pet.apoc_ghoul.active&pet.apoc_ghoul.remains<=buff.fireblood.duration|active_enemies>=2&death_and_decay.ticking)|fight_remains<=buff.fireblood.duration
actions.racials+=/bag_of_tricks,if=active_enemies=1&(buff.unholy_strength.up|fight_remains<5)

# Trinkets
actions.trinkets=use_item,slot=trinket1,if=((!talent.summon_gargoyle|talent.summon_gargoyle&pet.gargoyle.active|cooldown.summon_gargoyle.remains>90|variable.trinket_priority=2&cooldown.summon_gargoyle.remains>20)&(pet.apoc_ghoul.active|buff.dark_transformation.up)&(variable.trinket_priority=1|trinket.2.cooldown.remains))|trinket.1.proc.any_dps.duration>=fight_remains
actions.trinkets+=/use_item,slot=trinket2,if=((!talent.summon_gargoyle|talent.summon_gargoyle&pet.gargoyle.active|cooldown.summon_gargoyle.remains>90|variable.trinket_priority=1&cooldown.summon_gargoyle.remains>20)&(pet.apoc_ghoul.active|buff.dark_transformation.up)&(variable.trinket_priority=2|trinket.1.cooldown.remains))|trinket.2.proc.any_dps.duration>=fight_remains
actions.trinkets+=/use_item,slot=trinket1,if=!variable.trinket_1_buffs&(trinket.2.cooldown.remains|!variable.trinket_2_buffs|!talent.summon_gargoyle|cooldown.summon_gargoyle.remains>20&!pet.gargoyle.active)|fight_remains<15
actions.trinkets+=/use_item,slot=trinket2,if=!variable.trinket_2_buffs&(trinket.1.cooldown.remains|!variable.trinket_1_buffs|!talent.summon_gargoyle|cooldown.summon_gargoyle.remains>20&!pet.gargoyle.active)|fight_remains<15

head=maw_of_the_haunted_frostbrood,id=200408,bonus_id=4800/4786/1498/6935,gem_id=192985
neck=elemental_lariat,id=193001,bonus_id=6652/7936/7979/1540/8767/8782,gem_id=192961/192948/192948,crafted_stats=36/49
shoulders=jaws_of_the_haunted_frostbrood,id=200410,bonus_id=4800/4786/1498
back=fireproof_drape,id=193763,bonus_id=6808/4786/1643
chest=cuirass_of_irreparable_madness,id=193644,bonus_id=6652/8783/8784/7936/7937/6808/4786/1643,enchant=waking_stats_3
wrists=vambraces_of_the_haunted_frostbrood,id=200412,bonus_id=1507/6935,gem_id=192948
hands=grasps_of_the_haunted_frostbrood,id=200407,bonus_id=4800/4786/1498
waist=primal_molten_greatbelt,id=190501,bonus_id=8836/8840/8902/8802/8793/8932/8960/1498,gem_id=192948
legs=greaves_of_the_haunted_frostbrood,id=200409,bonus_id=4800/4786/1504,enchant=fierce_armor_kit_3
feet=stonestep_boots,id=143974,bonus_id=4177/6808/4786/3311
finger1=seal_of_filial_duty,id=195526,bonus_id=4800/4786/1497/6935,gem_id=192948,enchant=devotion_of_critical_strike_3
finger2=jeweled_signet_of_melandrus,id=134542,bonus_id=1795/6808/4786/3300/6935,gem_id=192948,enchant=devotion_of_critical_strike_3
trinket1=algethar_puzzle_box,id=193701,bonus_id=6808/4786/1643
trinket2=manic_grieftorch,id=194308,bonus_id=4800/4786/1498
main_hand=incarnate_skysplitter,id=195528,bonus_id=4800/4786/1498,enchant=rune_of_the_fallen_crusader

# Gear Summary
# gear_ilvl=422.20
# gear_strength=5445
# gear_stamina=13377
# gear_crit_rating=2134
# gear_haste_rating=4824
# gear_mastery_rating=3814
# gear_versatility_rating=575
# gear_armor=7154
# set_bonus=tier29_2pc=1
# set_bonus=tier29_4pc=1
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

  racials->add_action( "blood_fury,if=cooldown.dancing_rune_weapon.ready&(!cooldown.blooddrinker.ready|!talent.blooddrinker.enabled)" );
  // ...

  standard->add_action( "tombstone,if=buff.bone_shield.stack>5&rune>=2&runic_power.deficit>=30&!(talent.shattering_bones.enabled&death_and_decay.ticking)&cooldown.dancing_rune_weapon.remains>=25" );
  // ...

  trinkets->add_action( "use_item,slot=trinket1,if=!variable.trinket_1_buffs", "Prioritize damange dealing on use trinkets over trinkets that give buffs" );
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
