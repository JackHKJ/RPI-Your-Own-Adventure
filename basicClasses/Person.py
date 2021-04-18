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

    def __init__(self, name, location="TROY", gender="UNKNOWN", tel="UNKNOWN", mail="UNKNOWN"):
        """
        The initializing function of the class
        """
        self.name = name
        self.location = location
        self.gender = gender
        self.tel = tel
        self.mail = mail
        self.skills = set()
        self.skillConnection = []

    def __str__(self):
        return "User [{}]".format(self.name)

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
        if this_skill.child is not None:
            for this_child in this_skill.child:
                if this_child in self.skills:
                    self.skillConnection.append([str(this_child), str(this_skill)])

    def add_skills_by_shortName(self, skill_tree: SkillTree, skills):
        """
        This function tries to add a list of skills by finding them in the main tree using shortNames
        :param skill_tree: the skill tree where the skills came from
        :param skills: a list of shortName of the skill to be added
        :return: None
        """
        for skill in skills:
            this_node = skill_tree.get_node_by_shortName(skill)
            if this_node is not None:
                self.add_skill(skill_tree, this_node)

    def get_selectable_courses(self, skillTree: SkillTree):
        """
        Get the selectable courses of a person
        :param skillTree: the skillTree to be utilized
        :return: list of SkillTreeNode that is selectable for the person
        """
        selectable_course = []
        for course in skillTree.node_set:
            if len(course.parent) == 0 or (len(course.parent) == 1 and course.parent[0] == skillTree.root_node):
                selectable_course.append(course)
                continue
            selectable = True
            for req in course.parent:
                if req not in self.skills:
                    selectable = False
                    break
            if selectable and course not in self.skills:
                selectable_course.append(course)
                continue
        return selectable_course

    def get_selectable_courses_filtered(self, skillTree: SkillTree, filter_str: str):
        """
        Get the selectable course with filter applied
        :param skillTree:the skillTree to be utilized
        :param filter_str:the filter to be applied
        :return:list of SkillTreeNode that is selectable for the person with filter applied
        """
        selectable_courses = self.get_selectable_courses(skillTree)
        filtered = []
        for course in selectable_courses:
            if filter_str in course.fullName or filter_str in course.shortName or filter_str in course.ID:
                filtered.append(course)
        return filtered
