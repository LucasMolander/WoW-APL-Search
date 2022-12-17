# WoW-APL-Search
Searches through the space of Action Priority Lists to find the best one.

# Code Structure
Main is in [sc_main.cpp](https://github.com/simulationcraft/simc/blob/dragonflight/engine/sc_main.cpp#L370)
as basically just
```
sim_t sim;
sim.main( io::utf8_args( argc, argv ) );
```

And `sim_t` is in [sim.hpp](https://github.com/simulationcraft/simc/blob/dragonflight/engine/sim/sim.hpp#L61)
(which is a child of `sc_thread_t`, basically just so it can `run()`).

`sim_t::main()` does some bookkeeping and reporting, then calls `simt_t::execute()`,
which is in [sim.cpp](https://github.com/simulationcraft/simc/blob/dragonflight/engine/sim/sim.cpp#L3187):
```
bool success = false;
{
  auto merge_final_action = gsl::finally([&](){ merge(); }); // Always merge, even in cases of unsuccessful simulation!
  partition();
  success = iterate();
}
return success;
```

`sim_t::partition()` allocates work iterations (`work_queue -> size()`) amongst threads
via `children.push_back( new sim_t( this, i + 1, child_control ) )`

`sim_t::execute()` calls [`sim_t::iterate()`](https://github.com/simulationcraft/simc/blob/dragonflight/engine/sim/sim.cpp#L2889),
which is basically
```
init();
activate_actors();

do
{
  ++current_iteration;
  ++work_done;
  combat();
  // Progress bar
  do_pause();
  if ( ! canceled )
  {
    current_index = work_queue -> pop();
    more_work = work_queue -> more_work();
    if ( more_work && current_index != old_active )
    {
      // Work indices, etc. for updating Progress Bar
      activate_actors();
    }
  }
} while ( more_work && ! canceled );
```

And here's `sim_t::init()`:
```
const auto start_time = chrono::wall_clock::now();

event_mgr.init();

// Seed RNG

// Set lag_stddev values

// Challenge mode or scaling item level

// set scaling metric

// Make the buffs (on `auras`) arcane_intellect, battle_shout, mark_of_the_wild, and power_word_fortitude

// Find Already defined target, otherwise create a new one.

// create additional enemies here

// Determine whether we have healers or tanks.

raid_event_t::init( this );

init_actors();

simulation_length.reserve( std::min( iterations, 10000 ) );

// For each actor in actor_list, call init_finished()

// If save= option is used, don't bother initializing profilesets
```

And here's `sim_t::activate_actors()`:
```
// Call reset_callbacks() on lots of lists

if ( ! single_actor_batch ) {
  range::for_each( player_list, []( player_t* p ) { p -> activate(); } );
}
// Single-actor batch mode activates the current active actor
else
{
  range::for_each( target_list, []( player_t* t ) { t -> actor_changed(); } );

  // Deactivate old actor
  if ( current_index > 0 )
  {
    player_no_pet_list[ current_index - 1 ] -> deactivate();
  }

  // Activate new actor
  player_no_pet_list[ current_index ] -> activate();
  if ( ! profileset_enabled )
  {
    progress_bar.set_phase( player_no_pet_list[ current_index ] -> name_str );
  }
}
```

## Events
`struct event_t` is in [event.hpp](https://github.com/simulationcraft/simc/blob/2ebb7a1fb07f34d5a4a15a5452960f85959fc664/engine/sim/event.hpp#L45).

## Combat
So the next interesting function is [`sim_t::combat()`](https://github.com/simulationcraft/simc/blob/dragonflight/engine/sim/sim.cpp#L1752)
which is just
```
combat_begin();
event_mgr.execute();
combat_end();
```

[`sim_t::combat_begin()`](https://github.com/simulationcraft/simc/blob/dragonflight/engine/sim/sim.cpp#L1814)
is like this:
```
// Debug stuff

reset();

iteration_dmg = priority_iteration_dmg = iteration_heal = 0;
datacollection_begin();
for ( auto& target : target_list ) target -> combat_begin();

// Override arcane_intellect, battle_shout, mark_of_the_wild, and power_word_fortitude

// Call combat_begin() on each module_t in module_t::get( i ) for i PLAYER_NONE to PLAYER_MAX

// Call combat_begin() on each player_t in player_list, player_no_pet_list, and their pets

// If required, call make_event() for regen_event_t, bloodlust_check_t, sim_end_event_t, and sim_safeguard_end_event_t

raid_event_t::combat_begin( this );
```

### Event Manager
The `event_manager_t` struct definition is in
[event_manager.hpp](https://github.com/simulationcraft/simc/blob/2ebb7a1fb07f34d5a4a15a5452960f85959fc664/engine/sim/event_manager.hpp#L20).
It has:
* `std::vector<event_t*> timing_wheel`

Moreover, [`event_manager_t::execute()`](https://github.com/simulationcraft/simc/blob/11753b3fd4fdad168be124a76d849ed427987071/engine/sim/event_manager.cpp#L203)
is like this:
```
unsigned n_events = 0U;

while ( event_t* e = next_event() )
{
  if ( e->time == current_time ) {
    if ( ++n_events == MAX_EVENTS ) {
      cancel_stuck();
    }
  } else {
    n_events = 0U;
  }

  current_time = e->time;

  if ( e->reschedule_time > e->time ) {
    reschedule_event( e ); continue;
  } else {
    // Optionally monitor CPU of the event
    e->execute();
  }

  recycle_event( e );
}

return true;
```

And here is [event_manager_t::next_event()](https://github.com/simulationcraft/simc/blob/11753b3fd4fdad168be124a76d849ed427987071/engine/sim/event_manager.cpp#L350):
```
  if ( events_remaining == 0 )
    return nullptr;

  while ( true )
  {
    event_t*& event_list = timing_wheel[ timing_slice ];
    if ( event_list )
    {
      event_t* e = event_list;
      event_list = e->next;
      events_remaining--;
      events_processed++;
      return e;
    }

    timing_slice++;
    if ( timing_slice == timing_wheel.size() )
    {
      timing_slice = 0;
      // Time Wheel turns around.
    }
  }

  return nullptr;
```

`sim_t::sim_t()` constructs `event_mgr( this )`, and  `sim_t::init()` calls `event_mgr.init()`.
`event_manager_t::event_manager_t()` is basic and non-interesting.
On the other hand,
[`event_manager_t::init`](https://github.com/simulationcraft/simc/blob/11753b3fd4fdad168be124a76d849ed427987071/engine/sim/event_manager.cpp#L319)
is slightly more interesting:
```
// Conditionally set wheel_seconds to 1024 and wheel_granularity to 32

wheel_time = timespan_t::from_seconds( wheel_seconds );

wheel_size = ( uint32_t )( wheel_time.total_millis() >> wheel_shift );

// Round up the wheel depth to the nearest power of 2 to enable a fast "mod"
// operation.
for ( wheel_mask = 2; wheel_mask < wheel_size; wheel_mask *= 2 )
{
  continue;
}
wheel_size = wheel_mask;
wheel_mask--;

// The timing wheel represents an array of event lists: Each time slice has an
// event list.
timing_wheel.resize( wheel_size );
```

# APL Codegen (.simc --> .cpp)
APLs are typically written in human-readable form (TCI, aka
[TextualConfigurationInterface](github.com/simulationcraft/simc/wiki/TextualConfigurationInterface)
), usually in files with the `.simc` extension. For example,
[T29_Death_Knight_Unholy.simc](github.com/simulationcraft/simc/blob/84ea508e96575079df70d00c9a2ce61eca3bb7f1/profiles/Tier29/T29_Death_Knight_Unholy.simc):
```
deathknight="T29_Death_Knight_Unholy"
source=default
spec=unholy
# ...

# Default consumables
potion=elemental_potion_of_ultimate_power_3
# ...

# Executed before combat begins. Accepts non-harmful actions only.
actions.precombat=flask
# ...

# Executed every time the actor is available.
actions=auto_attack

# Also do actions.aoe, actions.cooldowns, actions.generic, actions.opener, actions.racials, actions.trinkets

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
// Headers

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

  // Also add actions to default_, drw_up, racials, standard, trinkets
}
//blood_apl_end

//frost_apl_start

// ...

}  // namespace death_knight_apl
```

The C++ code is what's actually used by the simuation.

## SIMC Generation
The `.simc` file that's converted to C++ code is, itself, codegen'd.

There is one file per *class* in `profiles/generators/Tier29/`
that has one section like this per spec (basically just metadata and gear),
e.g. [T29_Generate_Death_Knight.simc](github.com/simulationcraft/simc/blob/84ea508e96575079df70d00c9a2ce61eca3bb7f1/profiles/generators/Tier29/T29_Generate_Death_Knight.simc):
```
deathknight="T29_Death_Knight_Blood"
level=70
# etc.

head=maw_of_the_haunted_frostbrood,id=200408,bonus_id=4800/4786/1498/1808,gem_id=192925
# etc.

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

# Project Info
Python version `3.7.4`.
