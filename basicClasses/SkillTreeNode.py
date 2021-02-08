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

    def try_to_pass(self, your_result):
        """
        Compare your result to the pass requirements, if passed then return True and modify the mastered status
        :param your_result: your result to be judged
        :return: True if this skill is considered mastered and False otherwise
        """
        pass


