import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

# --- IAN PSEUDOCODE ---
#
# closest_planet
#
# This is an additive measure for determining which planet we send an attack or
# reinforcements from. Essentially we should be able to respond faster to take neutral
# planets, defend planets being attacked, and ultimately make the final attack push faster
# I'm not exactly sure what order of priority would be optimal, but here's the gist:
#       a. compare closest planet first
#       b. then, if it has enough ships to attack
#       c. we attack from that planet (also accounting for "actual required ships"
#           based on distance and target planet growth rate)
#           [see bt_bot.py for reference]
#       d. else find next closest ship and compare its "actual required ships"
#       e. if all else fails, perhaps we start sending reinforcements to nearby ships
#
# production_bot.py Line 26 (for full reference): 
# Formula production_bot uses to send "actual required ships" considering 
# distance and growth rate:
#
#       required_ships = target_planet.num_ships + 
#               state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1
# ----------------------

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    # --- IAN PSEUDOCODE ---
    # * closest_planet
    # ----------------------
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    # --- IAN PSEUDOCODE ---
    # Note: We probably do just want to keep sending ships and defending
    #       when we can early game
    # ----------------------
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    # --- IAN PSEUDOCODE ---
    # * closest_planet
    # ----------------------
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def spread_to_nearest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    # --- IAN PSEUDOCODE ---
    # * closest_planet
    # ----------------------
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    nearest_planet = None
    for planet in state.neutral_planets():
        if nearest_planet == None or state.distance(strongest_planet, planet) < state.distance(strongest_planet, nearest_planet):
            nearest_planet = planet

    if not strongest_planet or not nearest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, nearest_planet.ID, strongest_planet.num_ships / 2)

def support_strongest_planet(state):
    # --- IAN PSEUDOCODE ---
    # * closest_planet
    # ----------------------
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    second_strongest_planet = None
    for planet in state.my_planets():
        if planet != strongest_planet and planet.num_ships > second_strongest_planet.num_ships:
            second_strongest_planet = planet
    if second_strongest_planet != None:
        return issue_order(state, second_strongest_planet.ID, strongest_planet.ID, second_strongest_planet.num_ships / 2)
    else: return False
