# -*- encoding:utf-8 -*-
# Dependencies
from basicClasses.SkillTreeNode import SkillTreeNode
from basicClasses.SkillTree import SkillTree
import networkx as nx
import matplotlib.pyplot as plt


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
        self.skills = set()
        self.skillConnection = []

    def get_name(self):
        """
        Getter of the name
        :return: name
        """
        return self.name

    def get_skills(self):
        """
        Getter of the skills
        :return: skills
        """
        return self.skills

    def add_skill(self, main_tree: SkillTree, this_skill: SkillTreeNode):
        """
        Add skill to the person class
        :param main_tree: The main tree to look for connections
        :param this_skill: skill to be added
        :return: None
        """
        # If already contained, pass
        if this_skill in self.skills:
            return

        self.skills.add(this_skill)
        if this_skill.parent is not None:
            for this_parent in this_skill.parent:
                if this_parent in self.skills:
                    self.skillConnection.append([str(this_parent), str(this_skill)])
        if this_skill.children is not None:
            for this_child in this_skill.children:
                if this_child in self.skills:
                    self.skillConnection.append([str(this_child), str(this_skill)])

    def visualize_skills(self):
        g = nx.Graph()
        g.add_edges_from(self.skillConnection)
        nx.draw_networkx(g)
        plt.show()
