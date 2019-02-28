
import random
import marioai
import _thread

import numpy as np

import py_trees
from py_trees import display
from py_trees.blackboard import Blackboard
from py_trees.common import Status as NodeStatus
from py_trees.trees import BehaviourTree, CONTINUOUS_TICK_TOCK
from py_trees.behaviour import *
from py_trees.behaviours import *
from py_trees.composites import *
from py_trees.decorators import *

__all__ = ['BTAgent']

BLACKBOARD = None

class BTAgent(marioai.BTAgent):
    def __init__(self):
        super(BTAgent, self)

        global BLACKBOARD

        py_trees.logging.level = py_trees.logging.Level.DEBUG

        BLACKBOARD = Blackboard()
        self.tree = BehaviourTree(self.create_tree())
        _thread.start_new_thread(self.tree.tick_tock, (
                        50, CONTINUOUS_TICK_TOCK, None, None))

    def act(self):
        action = BLACKBOARD.get("next_action") or [0, 0, 0, 0, 0]
        BLACKBOARD.set("next_action", None)
        return action

    def sense(self, obs):

        global BLACKBOARD
        super(RLAgent, self).sense(obs)
        # (mayMarioJump, isMarioOnGround, marioFloats, enemiesFloats, levelScene, dummy)

        get_situation(focus=BLACKBOARD.get("focus"),
                      can_shoot=obs[0],
                      on_ground=obs[1],
                      mario_floats=obs[2],
                      enemy_floats=obs[3],
                      can_shoot=focus=BLACKBOARD.get("focus"))


class Learn(Behaviour):
    """
        This action is meant to trigger the learning algorithm and 
        grow the tree
    """
    def update(self):
        self.logger.debug("  %s [Foo::update()]" % self.name)
        # return NodeStatus.SUCCESS
        while self.cum_reward < 1:
            perform_action(sequence(T_safe, T))
            if is_executed("action learn"):
                T_cond = get_situation()
                T_acts = learn_single_action(T)
                if T_acts.children == 0:
                    T_acts = get_actions_gp(T)
                if is_present(T_acts):
                    T_cond_exist = get_conditions(T_acts)
                    T_cond_exist = simplify(fallback(T_cond_exist, T_cond))
                else:
                    T = fallback(sequence(T_cond, T_acts), T)
            self.get_rewards(sequence(T_safe, T))
        return T


def get_situation(focus, **kwargs):
    """
        Gets a snap shot of the world, and transforms 
        it into a sequence composition of condition nodes

        Equation 6 from the paper
    """
    def inv(cond):
        return Inverter(name="Inverter", child=Check(name=name, cond=cond))

    root = Sequence("T_cond")
    inv_root = Sequence("inv")
    norm_root = Sequence("norm")
    for k, v in kwargs:
        val = eval(v)
        if val:
            node = Check(name=k, cond=v)
            norm_root.add_child(node)
        else:
            node = inv(name=k, cond=v)
            inv_root.add_child(node)
    root.add_children([norm_root, inv_root])
    return root
