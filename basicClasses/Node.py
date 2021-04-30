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
        self.__ID = ID
        # parent: a list representation of parents
        self.__parent = []
        # child: a list representation of childs
        self.__child = []

    def get_ID(self):
        """
        Getter of the name
        """
        return self.__ID

    def get_parent(self):
        """
        Getter of the parent
        """
        return self.__parent

    def get_child(self):
        """
        Getter of the child
        """
        return self.__child
