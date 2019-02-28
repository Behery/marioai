
import py_trees
from py_trees import display
from py_trees.blackboard import Blackboard
from py_trees.common import Status as NodeStatus
from py_trees.trees import BehaviourTree, CONTINUOUS_TICK_TOCK
from py_trees.behaviour import *
from py_trees.behaviours import *
from py_trees.composites import *
from py_trees.decorators import *

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
