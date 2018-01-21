import battlecode as bc
import random
import sys
import traceback

import os
print(os.getcwd())

print("pystarting")

# A GameController is the main type that you talk to the game with.
# Its constructor will connect to a running game.
gc = bc.GameController()
directions = list(bc.Direction)

print("pystarted")

# It's a good idea to try to keep your bots deterministic, to make debugging easier.
# determinism isn't required, but it means that the same things will happen in every thing you run,
# aside from turns taking slightly different amounts of time due to noise.
random.seed(6137)

# let's start off with some research!
# we can queue as much as we want.
gc.queue_research(bc.UnitType.Rocket)
gc.queue_research(bc.UnitType.Worker)
gc.queue_research(bc.UnitType.Knight)

my_team = gc.team()

while True:
    # We only support Python 3, which means brackets around print()
    print('pyround:', gc.round())

    # frequent try/catches are a good idea
    try:


        units = gc.my_units()
        count = {}

        count["healer"] = 0
        count["knight"] = 0
        count["factory"] = 0
        #initaite counts of units
        fac_completed = True
        fac_not_complete = []
        #boolean to determine if all of our factories are fully built

        for unit in units:

            if unit.unit_type == bc.UnitType.Healer:

                count["healer"]+=1

            if unit.unit_type == bc.UnitType.Knight:
                count["knight"] += 1

            if unit.unit_type == bc.UnitType.Factory:
                count["factory"] += 1

                if unit.health < unit.max_health:
                    fac_not_complete.append(unit)
                    fac_completed = False
                    #if factory health is less than max, it is not done
        # walk through our units:
        for unit in gc.my_units():

            x = random.randrange(0, 4, 1)

            #random variables for different classes





            # first, factory logic
            if unit.unit_type == bc.UnitType.Factory:
                garrison = unit.structure_garrison()
                if len(garrison) > 0:
                    d = random.choice(directions)
                    if gc.can_unload(unit.id, d):
                        print('unloaded something')
                        gc.unload(unit.id, d)
                        continue
                #if factory can unload something unload it,




                if x == 0:

                    if count["knight"] < count["healer"] and gc.can_produce_robot(unit.id, bc.UnitType.Knight):
                        gc.produce_robot(unit.id, bc.UnitType.Knight)
                        print('produced a knight!')
                        continue
                    else:

                        if gc.can_produce_robot(unit.id, bc.UnitType.Healer):
                            gc.produce_robot(unit.id, bc.UnitType.Healer)
                            print('produced a healer!')
                            continue



                elif x == 1:

                    if gc.can_produce_robot(unit.id, bc.UnitType.Worker):
                        gc.produce_robot(unit.id, bc.UnitType.Worker)
                        print('produced a worker!')
                        continue




                elif x == 2:

                    if  count["healer"] < count["knight"]  and gc.can_produce_robot(unit.id, bc.UnitType.Healer):
                        gc.produce_robot(unit.id, bc.UnitType.Healer)
                        print('produced a healer!')
                        continue

                    elif gc.can_produce_robot(unit.id, bc.UnitType.Knight):
                        gc.produce_robot(unit.id, bc.UnitType.Knight)
                        print('produced a knight!')
                        continue

                elif x == 3:


                    if gc.can_produce_robot(unit.id, bc.UnitType.Ranger):
                        gc.produce_robot(unit.id, bc.UnitType.Ranger)
                        print('produced a knight!')
                        continue

            # first, let's look for nearby blueprints to work on
            location = unit.location
            if location.is_on_map():
                nearby = gc.sense_nearby_units(location.map_location(), 20)
                for other in nearby:
                    if unit.unit_type == bc.UnitType.Worker and other.unit_type == bc.UnitType.Factory:

                        #workers try to build factories nearby

                        if  gc.can_build(unit.id, other.id):
                            gc.build(unit.id, other.id)
                            print('built a factory!!')
                            # move onto the next unit
                            continue
                        elif other in fac_not_complete:

                            #if a factory is not completed, move towards factories
                            #moves to factories that aren't completed only

                            maploc = unit.location.map_location()
                            factory_loc = other.location.map_location()
                            direction = maploc.direction_to(factory_loc)
                           # print("direction",direction)
                            if gc.is_move_ready(unit.id):
                                #print("I am move ready")

                                if gc.can_move(unit.id, direction):
                                   # print("I can move in that direction")
                                    gc.move_robot(unit.id, direction)
                                    #print("Moving towards factory")
                                    continue
                                else:
                                    pass



                    if unit.unit_type == bc.UnitType.Knight and  other.team != my_team and gc.is_attack_ready(unit.id) and gc.can_attack(unit.id, other.id):
                        print('attacked a thing!')
                        gc.attack(unit.id, other.id)
                        continue
                    if unit.unit_type == bc.UnitType.Healer and  other.team == my_team and gc.is_heal_ready(unit.id) and gc.can_heal(unit.id,other.id) and other.health <other.max_health:

                        print('healed a thing')
                        gc.heal(unit.id,other.id)

            # okay, there weren't any dudes around
            # pick a random direction:
            d = random.choice(directions)

            # or, try to build a factory:
            if gc.karbonite() > bc.UnitType.Factory.blueprint_cost() and gc.can_blueprint(unit.id, bc.UnitType.Factory, d) and count["factory"] < 10:
                gc.blueprint(unit.id, bc.UnitType.Factory, d)
                print("BLUEPRINT")
            # and if that fails, try to move
            elif gc.is_move_ready(unit.id) and gc.can_move(unit.id, d):
                gc.move_robot(unit.id, d)



    except Exception as e:
        print('Error:', e)
        # use this to show where the error was
        traceback.print_exc()

    # send the actions we've performed, and wait for our next turn.
    gc.next_turn()

    # these lines are not strictly necessary, but it helps make the logs make more sense.
    # it forces everything we've written this turn to be written to the manager.
    sys.stdout.flush()
    sys.stderr.flush()
