
import py_trees
from py_trees import display
from py_trees.blackboard import Blackboard
from py_trees.common import Status as NodeStatus
from py_trees.trees import BehaviourTree, CONTINUOUS_TICK_TOCK
from py_trees.behaviour import *
from py_trees.behaviours import *
from py_trees.composites import *
from py_trees.decorators import *

from bt_actions import *


ACTIONS = {'10000': "Left"
           '01000': "Right"
           '00100': "Crouch"
           '01010': "Jump"
           '00001' "Shoot"}


def get_random_subtree(root):
    children = root.get_children()
    if not children:
        return None
    for child in children:
        if random.nextchoice([True, False]):
            break
    return child


def cross_bt(a, b):
    a_child = get_random_child(a)
    b_child = get_random_child(b)
    if a_child and b_child:
        if random.nextchoice([True, False]):
            a.replace_child(a_child, b_child)
            b.replace_child(b_child, a_child)
            return a, b
        return cross_bt(a_child, b_child)
    return None, None


def mutate_bt(root):
    children = root.get_children()
    available_actions = reduce(set.union, ACTIONS.values())
    flow_nodes = {Sequence, Parallel, Chooser, Selector}
    for child_ind in range(len(children)):
        child = children[child_ind]
        if random.nextchoice([True, False]):
            ## Conditions aren't mutated, for now
            child_type = type(child)
            if child_type in available_actions:
                root.replace_child(child, random.nextchoice(available_actions - {child_type})(child.name))
            else:
                if child_type is Composite:
                    grand_children = child.get_children()
                    replacement = random.nextchoice(flow_nodes - {child_type})(child.name)
                    replacement.add_children(grand_children)
                    root.replace_child(child, replacement)


def create_fallback_selector(actions, eps):
    """
        Equation 7
    """

    fallback = Chooser("fallbacks")
    for act in actions:
        if self.reward_map[act] > eps:
            fallback.add_child(eval(ACTIONS[act])(ACTIONS[act]))
    return fallback
