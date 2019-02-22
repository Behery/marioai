
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

class BTAgent(marioai.Agent):
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
        super(BTAgent, self).sense(obs)
        field = self.level_scene
        BLACKBOARD.set("focus", field[9:14, 11:16].flatten())
        BLACKBOARD.set("can_shoot", obs[0])

    def create_tree(self):
        BLACKBOARD.next_action = [0,0,0,0,0]
        root = Selector("root")

        bad_guy_saftey = Sequence("bs")
        bad_guy_check = Check(name="bad-guy?", cond='BLACKBOARD.get("focus") is not None and (BLACKBOARD.get("focus")[11] in range(2, 14) or BLACKBOARD.get("focus")[12] in range(2, 14))')
        bad_guy_response = Selector("defnse")

        shot_saftey = Sequence("shooting")
        shoot_check = Check(name="can_shoot?", cond='BLACKBOARD.get("can_shoot")')
        shot_saftey.add_children([shoot_check, Shoot()])

        bad_guy_response.add_children([shot_saftey, Jump()])
        bad_guy_saftey.add_children([bad_guy_check, bad_guy_response])

        obstacle_saftey = Sequence("os")
        obstacle_check = Check(name="obstacle?", cond='BLACKBOARD.get("focus") is not None and BLACKBOARD.get("focus")[11] in [-10, 20]')
        obstacle_response = Selector("avoidance")
        obstacle_response.add_children([Jump()])
        obstacle_saftey.add_children([obstacle_check, obstacle_response])

        root.add_children([bad_guy_saftey, obstacle_saftey, Right()])

        display.print_ascii_tree(root)
        return root


class Check(Behaviour):
    def __init__(self, name="cond", cond=True):
        super(Check, self).__init__(name)
        self.condition = cond

    def update(self):
        self.logger.debug("  %s [Foo::update()]" % self.name)
        return NodeStatus.SUCCESS if eval(self.condition) else NodeStatus.FAILURE


class Left(Behaviour):
    def update(self):
        self.logger.debug("  %s [Foo::update()]" % self.name)
        if BLACKBOARD.next_action:
            BLACKBOARD.next_action[0] = 1
            return NodeStatus.RUNNING
        else:
            BLACKBOARD.next_action = [1, 0 , 0, 0, 0]
            return NodeStatus.SUCCESS


class Right(Behaviour):
    def update(self):
        self.logger.debug("  %s [Foo::update()]" % self.name)
        if BLACKBOARD.next_action:
            BLACKBOARD.next_action[1] = 1
            return NodeStatus.RUNNING
        else:
            BLACKBOARD.next_action = [0, 1 , 0, 0, 0]
            return NodeStatus.SUCCESS


class Crouch(Behaviour):
    def update(self):
        self.logger.debug("  %s [Foo::update()]" % self.name)
        if BLACKBOARD.next_action:
            BLACKBOARD.next_action[2] = 1
            return NodeStatus.RUNNING
        else:
            BLACKBOARD.next_action = [0, 0 , 1, 0, 0]
            return NodeStatus.SUCCESS


class Jump(Behaviour):
    # Jumping to the right only!
    def update(self):
        self.logger.debug("  %s [Foo::update()]" % self.name)
        if BLACKBOARD.next_action:
            BLACKBOARD.next_action[3] = 1
            BLACKBOARD.next_action[1] = 1
            return NodeStatus.RUNNING
        else:
            BLACKBOARD.next_action = [0, 1 , 0, 1, 0]
            return NodeStatus.SUCCESS


class Shoot(Behaviour):
    def update(self):
        self.logger.debug("  %s [Foo::update()]" % self.name)
        if BLACKBOARD.next_action:
            BLACKBOARD.next_action[4] = 1
            return NodeStatus.RUNNING
        else:
            BLACKBOARD.next_action = [0, 0 , 0, 0, 1]
            return NodeStatus.SUCCESS
