#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn


# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')

    early_plan = Sequence(name='Early Strategy')
    check_neutral_planets = Check(if_neutral_planet_available)
    control_action = Action(claim_neutrals)
    early_plan.child_nodes = [check_neutral_planets, control_action]

    late_support_plan = Sequence(name='Late Support Strategy')
    check_no_neutral_planets = Check(if_no_neutral_planets)
    check_strongest_in_danger = Check(if_strongest_in_danger)
    support_action = Action(support_strongest_planet)
    late_support_plan.child_nodes = [check_no_neutral_planets, check_strongest_in_danger, support_action]

    late_attack_plan = Sequence(name='Late Attack Strategy')
    check_no_neutral_planets = Check(if_no_neutral_planets)
    check_strongest_safe = Check(if_strongest_safe)
    attack = Action(attack_weakest_enemy_planet)
    late_attack_plan.child_nodes = [check_no_neutral_planets, check_strongest_safe, attack]

    root.child_nodes = [early_plan, late_support_plan, late_attack_plan, attack.copy()]

    logging.info('\n' + root.tree_to_string())
    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

    behavior_tree = setup_behavior_tree()
    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
