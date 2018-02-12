


#---start of python imports
import sys
import numpy as np
import os
import time
#---end of my python imports
from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.agents import random_agent, base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions as sc2_actions
from pysc2.env import environment
from pysc2.lib import features
from pysc2.lib import actions
from pysc2 import maps

from absl import app
from absl import flags
#---end of sc2 imports
#---start of my imports
import defs
#---end of my imports

#----setup the flags for the simulation
FLAGS = flags.FLAGS
flags.DEFINE_bool("render", True, "Whether to render with pygame.")
flags.DEFINE_integer("screen_resolution", 84,
                     "Resolution for screen feature layers.")
flags.DEFINE_integer("minimap_resolution", 64,
                     "Resolution for minimap feature layers.")

flags.DEFINE_integer("max_agent_steps", 2500, "Total agent steps.")
flags.DEFINE_integer("game_steps_per_episode", 0, "Game steps per episode.")
flags.DEFINE_integer("step_mul", 8, "Game steps per agent step.")

flags.DEFINE_string("agent", "pysc2.agents.random_agent.RandomAgent",
                    "Which agent to run")
flags.DEFINE_enum("agent_race", None, sc2_env.races.keys(), "Agent's race.")
flags.DEFINE_enum("bot_race", None, sc2_env.races.keys(), "Bot's race.")
flags.DEFINE_enum("difficulty", None, sc2_env.difficulties.keys(),
                  "Bot's strength.")

flags.DEFINE_bool("profile", False, "Whether to turn on code profiling.")
flags.DEFINE_bool("trace", False, "Whether to trace the code execution.")
flags.DEFINE_integer("parallel", 1, "How many instances to run in parallel.")

flags.DEFINE_bool("save_replay", True, "Whether to save a replay at the end.")

flags.DEFINE_string("map", None, "Name of a map to use.")
flags.mark_flag_as_required("map")
#---END flags defines for simulation
FLAGS = flags.FLAGS
#---end flag settings

#this is ONLY for simple 64
'''
The mini map is 64 units across and 64 units tall, with 
(0, 0) being the top left coordinate. Values we receive are 0 
indexed, so we can assume that anything with an x or y 
coordinate between 0 and 31 is at the top left. Anything with 
an x or y coordinate between 32 and 63 is at the bottom right.
'''

class SimpleAgent(base_agent.BaseAgent):
    base_top_left = None
    supply_depot_built = False
    scv_selected = False
    barracks_built = False
    barracks_selected = False
    barracks_rallied = False
    def step(self,obs):
        super(SimpleAgent,self).step(obs)
        time.sleep(0.5)
        if self.base_top_left is None:
            #the minimap from observation has different types of minimap
            #we look at the player relative minimap. This gives positions in [64x64] that tell if
            # a position is friendly or hostile. Then .nonzero() removes those cases that are 0.
            player_y , player_x = (obs.observation["minimap"][defs._PLAYER_RELATIVE] == \
                                   defs._PLAYER_SELF).nonzero()
            #we get two arrays of indices that are position mapped to each other. i.e. x[0] and y[0] are a coordinate
            #now find if our base is top left or bottom right.
            self.base_top_left = player_y.mean() <= 31 #given the map index is 0->63

        if not self.supply_depot_built or not self.barracks_built:
            if not self.scv_selected:
                unit_type = obs.observation["screen"][defs._UNIT_TYPE]

                #IMPORTANT , the screen points are relative to the CURRENT SCREEN
                # if you move the camera, they become meaningless.
                #Note: The coordinates of units are returned in the order (y, x),
                # but you must pass in the values in the order (x, y)
                unit_y,unit_x = (unit_type == defs._TERRAN_SCV).nonzero()
                #get one of the scvs returned
                #this works when the screen has only our scvs.
                # in more complex situations, need it to be scv and our team (unit property)
                target = [unit_x[0],unit_y[0]]
                self.scv_selected = True
                return actions.FunctionCall(defs._SELECT_POINT, [defs._SELECT_POINT_SELECT, target])
            #---end if scv not selected
            #code to build supply depot, this will only be triggered when you have enuf resources
            elif defs._BUILD_SUPPLYDEPOT in obs.observation["available_actions"]:
                unit_type = obs.observation["screen"][defs._UNIT_TYPE]
                #in the line below, the terran command center has MANY x and y coordinates because it
                #spans an area
                unit_y, unit_x = (unit_type == defs._TERRAN_COMMANDCENTER).nonzero()
                #Now The screen is 84x84 units and a coordinate of (0, 0) is the top left corner.
                # In the code above we are placing the supply depot below the command centre by 20
                # units (or above if our base is at thebottom right).
                target = self.transformLocation(int(unit_x.mean()),0,int(unit_y.mean()),20)
                self.supply_depot_built = True
                return actions.FunctionCall(defs._BUILD_SUPPLYDEPOT,[defs._NOT_QUEUED,target])
            #code to build barracks
            elif defs._BUILD_BARRACKS in obs.observation["available_actions"]:
                unit_type = obs.observation["screen"][defs._UNIT_TYPE]
                #in the line below, the terran command center has MANY x and y coordinates because it
                #spans an area
                unit_y, unit_x = (unit_type == defs._TERRAN_COMMANDCENTER).nonzero()
                #Now The screen is 84x84 units and a coordinate of (0, 0) is the top left corner.
                # In the code above we are placing the supply depot below the command centre by 20
                # units (or above if our base is at thebottom right).
                target = self.transformLocation(int(unit_x.mean()),20,int(unit_y.mean()),0)
                self.supply_depot_built = True
                return actions.FunctionCall(defs._BUILD_BARRACKS,[defs._NOT_QUEUED,target])

        if self.supply_depot_built and self.barracks_built:
            


        return actions.FunctionCall(defs._NOOP,[])
    #---end step method

    def transformLocation(self, x, x_distance, y, y_distance):
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]

        return [x + x_distance, y + y_distance]
    #---end transform location



#======================================================================================
#
#======================================================================================
def main_runner(unused_argv):

    #TODO GET SYS ARGV and set the map accordingly
    with sc2_env.SC2Env(
            map_name = "Simple64",
            agent_race="T",
            step_mul=8,
            visualize=True) as env:

        maps.get(FLAGS.map)  # Assert the map exists.
        agent_000 = SimpleAgent()
        action_spec = env.action_spec()
        observation_spec = env.observation_spec()
        agent_000.setup(observation_spec, action_spec)
        agent_000.reset()
        try:
            obs = env.reset()
            #maybe have the first action to select all marines first
            for step_idx in range(1000):
                #could use packaged python agents
                #print(obs[0].observation["available_actions"])
                print(obs[0].observation["score_cumulative"])
                print(obs[0].reward)
                print(obs[0].discount)

                one_step = agent_000.step(obs[0])
                obs = env.step([one_step])
        except KeyboardInterrupt:
            pass
        finally:
            print("simulation done")

if __name__ == "__main__":
    # sys.argv = ["pysc2.bin.agent", "--map", "ResourceCollection"]
    #do a competitive map (simple 64) with your race as terran
    sys.argv = ["pysc2.bin.agent", "--map", "Simple64", "--agent_race" ,"T"]
    app.run(main_runner)
