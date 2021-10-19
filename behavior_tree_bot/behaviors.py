from os import close, stat
import logging, sys
sys.path.insert(0, '../')
from planet_wars import issue_order

def claim_neutrals(state):
    # Implimentation of other bots' early game rollouts

    # load a planet we don't own
    for neutral_planet in state.not_my_planets():

        # check if we already have a fleet being sent to questioned planet
        isTargeted = False
        for fleet in state.my_fleets():
            if fleet.destination_planet == neutral_planet.ID:
                        isTargeted = True

        # if we are not sending a fleet to said planet
        if not isTargeted:
            # load a planet we own
            for my_planet in state.my_planets():
                # check if we own the planet or if the enemy does
                # set required ships accordingly
                if neutral_planet.owner == 0:
                    required_ships = neutral_planet.num_ships + 1
                elif neutral_planet.owner == 2:
                    required_ships = neutral_planet.num_ships + state.distance(my_planet.ID, neutral_planet.ID) * neutral_planet.growth_rate + 1

                # if we have the required number of ships, execute the order
                if my_planet.num_ships > required_ships:
                    issue_order(state, my_planet.ID, neutral_planet.ID, required_ships)

    return False


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    #strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (2) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not weakest_planet: return False
    
    logging.info(weakest_planet.owner)

    # (3) Find the best planet to use for the attack on the weakest enemy planet
    closest_planet = None
    for planet in state.my_planets():
        potential_required_ships = weakest_planet.num_ships + state.distance(planet.ID, weakest_planet.ID) * weakest_planet.growth_rate + 1
        if closest_planet == None or \
        state.distance(planet.ID, weakest_planet.ID) < state.distance(closest_planet.ID, weakest_planet.ID) \
        and planet.num_ships >= potential_required_ships:
            closest_planet = planet

    if not closest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my closest planet to the weakest enemy planet.
        required_ships = weakest_planet.num_ships + state.distance(closest_planet.ID, weakest_planet.ID) * weakest_planet.growth_rate + 1
        if required_ships > (closest_planet.num_ships): return False
        return issue_order(state, closest_planet.ID, weakest_planet.ID, required_ships)


def spread_to_weakest_neutral_planet(state):
    # (1) Find the weakest neutral planet.
    #weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)
    weakest_planet = None
    for target in state.neutral_planets():
        isTargeted = False
        for fleet in state.my_fleets():
            if fleet.destination_planet == target.ID:
                isTargeted = True
        if (not isTargeted) and (weakest_planet == None or target.num_ships < weakest_planet.num_ships):
            weakest_planet = target

    if not weakest_planet: return False

    logging.info(weakest_planet.owner)

    # (2) Find the best planet to use for the attack on the weakest neutral planet
    closest_planet = None
    for planet in state.my_planets():
        potential_required_ships = weakest_planet.num_ships + state.distance(planet.ID, weakest_planet.ID) * weakest_planet.growth_rate + 1
        if closest_planet == None or \
        state.distance(planet.ID, weakest_planet.ID) < state.distance(closest_planet.ID, weakest_planet.ID) \
        and planet.num_ships >= potential_required_ships:
            closest_planet = planet

    if not closest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (3) Send half the ships from my closest planet to the weakest neutral planet.
        required_ships = weakest_planet.num_ships + state.distance(closest_planet.ID, weakest_planet.ID) * weakest_planet.growth_rate + 1
        if required_ships > (closest_planet.num_ships): return False
        return issue_order(state, closest_planet.ID, weakest_planet.ID, required_ships)

def spread_to_nearest_neutral_planet(state):
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (2) Find the weakest neutral planet.
    # (2.1) Start with the nearest_planet being null.
    nearest_planet = None
    # (2.2) Loop through each neutral planet on the board.
    for planet in state.neutral_planets():
        # (2.3) Start the isTargeted variable as False.
        isTargeted = False
        # (2.4) Loop through each of my fleets
        for fleet in state.my_fleets():
            # (2.5) If the current fleet is headed to the current neutral planet...
            if fleet.destination_planet == planet.ID:
                # (2.6) ...then we set isTargeted to True.
                isTargeted = True
        #(2.7) If the current planet is not targeted, then we pass condition 1.
        #(2.7.1) If nearest_planet is None, we immediately set it equal to the current planet.
        #(2.7.2) Otherwise, if this planet is closer to our strongest planet than the current nearest_planet...
        if (not isTargeted) and (nearest_planet == None or state.distance(strongest_planet.ID, planet.ID) < state.distance(strongest_planet.ID, nearest_planet.ID)):
            #(2.8) ...then we set nearest_planet to be equal to the current planet.
            nearest_planet = planet

    if not nearest_planet: return False

    logging.info(nearest_planet.owner)

    # (3) Find the best planet to use for the attack on the weakest neutral planet
    closest_planet = None
    for planet in state.my_planets():
        potential_required_ships = nearest_planet.num_ships + state.distance(planet.ID, nearest_planet.ID) * nearest_planet.growth_rate + 1
        if closest_planet == None or \
        state.distance(planet.ID, nearest_planet.ID) < state.distance(closest_planet.ID, nearest_planet.ID) \
        and planet.num_ships >= potential_required_ships:
            closest_planet = planet

    if not strongest_planet or not closest_planet or not nearest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        required_ships = nearest_planet.num_ships + state.distance(closest_planet.ID, nearest_planet.ID) * nearest_planet.growth_rate + 1
        if required_ships > (closest_planet.num_ships): return False
        return issue_order(state, closest_planet.ID, nearest_planet.ID, required_ships)

def support_strongest_planet(state):
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    for fleet in state.my_fleets():
        if fleet.destination_planet == strongest_planet:
            return False

    for fleet in state.enemy_fleets():
        if fleet.destination_planet == strongest_planet:
            fleet_size = fleet.num_ships

    closest_planet = None
    for planet in state.my_planets():
        potential_required_ships = fleet_size + state.distance(planet.ID, strongest_planet.ID) * strongest_planet.growth_rate + 1
        if closest_planet == None or \
        state.distance(planet.ID, strongest_planet.ID) < state.distance(closest_planet.ID, strongest_planet.ID) \
        and planet.num_ships >= potential_required_ships:
            closest_planet = planet

    if closest_planet != None:
        required_ships = fleet_size + state.distance(closest_planet.ID, strongest_planet.ID) * strongest_planet.growth_rate + 1
        if required_ships > (closest_planet.num_ships): return False
        return issue_order(state, closest_planet.ID, strongest_planet.ID, required_ships)
    else: return False
