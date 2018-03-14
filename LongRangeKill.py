#---start of python imports
import sys
import time
import random
#---end of my python imports

from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions
from pysc2 import maps

from absl import app
from absl import flags
#---end of sc2 imports
#---start of my imports
import defs
#---end of my imports


#---END flags defines for simulation
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
class New_ScriptedAgent_MoveToBeacon(base_agent.BaseAgent):
  """An agent specifically for solving the MoveToBeacon map."""
  unit_selected =False
  def step(self, obs):
    super(New_ScriptedAgent_MoveToBeacon, self).step(obs)
    if defs._ATTACK_SCREEN in obs.observation["available_actions"]:

      # player_relative = obs.observation["screen"][defs._PLAYER_RELATIVE]
      # neutral_y, neutral_x = (player_relative == defs._PLAYER_NEUTRAL).nonzero()
      # if not neutral_y.any():
      #   return actions.FunctionCall(defs._NO_OP, [])
      target = [int(random.randrange(0,64)), int(random.randrange(0,64))]
      # target = [int(neutral_x.mean()), int(neutral_y.mean())]
      return actions.FunctionCall(defs._ATTACK_SCREEN, [defs._NOT_QUEUED, target])
    else:
      return actions.FunctionCall(defs._SELECT_ARMY, [defs._SELECT_ALL])

    if self.unit_selected == False:
        self.unit_selected = True
        return actions.FunctionCall(defs._SELECT_ARMY, [defs._SELECT_ALL])
    else:
        pass


def main_runner(unused_argv):
    with sc2_env.SC2Env(
            map_name = "LongRangeKill",
            step_mul=8,
            visualize=True) as env:

        maps.get(FLAGS.map)  # Assert the map exists.
        agent_000 = New_ScriptedAgent_MoveToBeacon()
        action_spec = env.action_spec()
        observation_spec = env.observation_spec()
        agent_000.setup(observation_spec, action_spec)
        agent_000.reset()
        try:
            obs = env.reset()
            #maybe have the first action to select all marines first
            for step_idx in range(1000):
                #could use packaged python agents
                print(obs[0].observation["available_actions"])
                rand_step = agent_000.step(obs[0])
                obs = env.step([rand_step])

                time.sleep(0.5)

        except KeyboardInterrupt:
            pass
        finally:
            print("simulation done")

if __name__ == "__main__":
    sys.argv = ["pysc2.bin.agent", "--map", "LongRangeKill"]
    app.run(main_runner)