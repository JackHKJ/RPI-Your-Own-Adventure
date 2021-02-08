# -*- encoding:utf-8 -*-
# Dependencies

class SkillTreeNode(object):

    """
    This is the class designed for represent a single course in the full skill tree
    """

    # Representations

    # Name of the Skill
    name = ""
    # Other important information about this course
    additional_info = dict()
    # Parent Node representations
    parent = []
    # Children of this Node, potential selectable courses
    children = []
    # Some requirement to pass the course
    pass_requirement = []
    # Whether this skill is mastered
    mastered = False
    # Whether this node is abstract(used for classification purpose)
    is_abstract = False

    def __init__(self):
        """
        Initialize the representation
        """
        pass

    def __eq__(self, other):
        """
        Needed to implement the verification of prerequisite
        :param other: the object to compare
        :return: true if self === other
        """
        pass

    def __str__(self):
        """
        The representation to be shown in a printed graph
        :return: a string containing key identification part of this node
        """
        pass

    def add_parent(self, parent):
        """
        Add a parent to the representations
        :param parent: the SkillTreeNode to be added
        :return: None
        """
        pass

    def add_child(self, child):
        """
        Add a child to the representations
        :param child:
        :return:
        """
        pass

    def get_name(self):
        """
        The getter of the name
        :return: name
        """
        pass

    def is_mastered(self):
        """
        Getter of the mastered
        :return: mastered
        """
        pass

    def get_is_abstract(self):
        """
        Getter of the is_abstract
        :return: is_abstract
        """
        pass

    def try_to_pass(self, your_result):
        """
        Compare your result to the pass requirements, if passed then return True and modify the mastered status
        :param your_result: your result to be judged
        :return: True if this skill is considered mastered and False otherwise
        """
        pass
