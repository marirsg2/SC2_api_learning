from pysc2.lib import actions
from pysc2.lib import features

# Features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_PLAYER_SELF = 1
_PLAYER_FRIENDLY = 1
_PLAYER_NEUTRAL = 3  # beacon/minerals
_PLAYER_HOSTILE = 4
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

# Functions
_NO_OP = actions.FUNCTIONS.no_op.id
_NOOP = actions.FUNCTIONS.no_op.id
_MOVE_SCREEN = actions.FUNCTIONS.Move_screen.id
_ATTACK_SCREEN = actions.FUNCTIONS.Attack_screen.id
#select actions
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_SELECT_UNIT = actions.FUNCTIONS.select_unit.id
_SELECT_IDLE_WORKER = actions.FUNCTIONS.select_idle_worker.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_SELECT_ALL = [0]
_SELECT_IDLE_WORKER_SET = [0]

#building specific actions
_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
_RALLY_UNITS_MINIMAP = actions.FUNCTIONS.Rally_Units_minimap.id



#build actions
_BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id


#building IDs
_TERRAN_COMMANDCENTER = 18
_TERRAN_BARRACKS = 21
#unit Ids
_TERRAN_SCV = 45

# Parameters
_NOT_QUEUED = [0]
_QUEUED = [1]
_SELECT_POINT_SELECT = [0] #COMES FROM ENUM BELOW
# select_point_act = ArgumentType.enum([
#     sc_spatial.ActionSpatialUnitSelectionPoint.Select,
#     sc_spatial.ActionSpatialUnitSelectionPoint.Toggle,
#     sc_spatial.ActionSpatialUnitSelectionPoint.AllType,
#     sc_spatial.ActionSpatialUnitSelectionPoint.AddAllType,
# ]),
_SUPPLY_USED = 3
_SUPPLY_MAX = 4

#-------------------------------------------------







