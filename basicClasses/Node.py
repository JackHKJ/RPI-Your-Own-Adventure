# -*- encoding:utf-8 -*-
# Dependencies

class Node:
    """
    This is the class designed inheritance, a Node that can be presented in the SkillTree
    """

    def __init__(self, ID):
        """
        :param ID: the unique identification string of the Node
        """
        self.ID = ID
        # parent: a list representation of parents
        self.parent = []
        # child: a list representation of childs
        self.child = []

    def get_ID(self):
        """
        Getter of the name
        """
        return self.ID

    def get_parent(self):
        """
        Getter of the parent
        """
        return self.parent

    def get_child(self):
        """
        Getter of the child
        """
        return self.child
