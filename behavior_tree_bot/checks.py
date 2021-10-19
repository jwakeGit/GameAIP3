

def if_neutral_planet_available(state):
    return any(state.neutral_planets())

def if_no_neutral_planets(state):
    return not any(state.neutral_planets())

def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def if_strongest_in_danger(state):
  strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

  for fleet in state.enemy_fleets():
    if fleet.destination_planet == strongest_planet:
      return True
    else: return False

def if_strongest_safe(state):
  strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

  for fleet in state.enemy_fleets():
    if fleet.destination_planet == strongest_planet:
      return False
    else: return True

def if_incoming_attack(state):
  # I believe if_incoming_attack() can be used for early game rollout or 
  # mid game defense. Essentially we can use this to add a behavior 
  # that can signal when we need to defend (very generalized though)

  for my_planet in state.my_planets():
    for enemy_fleet in state.enemy_fleets():
      if my_planet == enemy_fleet.destination_planet:
        return True
      else: return False 

def if_attacking_same(state):
  # if_attacking_same() would be used to check when we are attacking a 
  # planet and it is also being attacked, we can send follow up ships 
  # compare fleets attacking same planets
  
  for my_fleet in state.my_fleets():
    for enemy_fleet in state.enemy_fleets(): 
      if my_fleet.destination_planet == enemy_fleet.destination_planet:
        return True
    else: return False
