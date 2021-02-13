# -*- encoding:utf-8 -*-
# Dependencies
from SkillTreeNode import SkillTreeNode
from SkillTree import SkillTree
import Request


class Person(object):
    """
    This class is to represent a player in our game
    """

    def __init__(self, name):
        """
        The initializing function of the class
        """
        self.name = name
        self.location = "TROY"
        self.gender = "UNKNOWN"
        self.tel = "UNKNOWN"
        self.mail = "UNKNOWN"
        self.skill_tree = SkillTree()


