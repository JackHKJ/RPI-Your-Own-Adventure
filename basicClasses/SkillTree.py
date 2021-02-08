# -*- encoding:utf-8 -*-
# Dependencies
import SkillTreeNode


class SkillTree:
    """
    This is the FullSkillTree class that is designed for:
    1. Show one's achieved skill
    2. Show availability of selectable courses/skills
    other usage may be extended
    """

    # The entry to the tree
    root_node: SkillTreeNode = None


    def readSkillTreeFromFile(self, input_file):
        """
        read the input file to form a full skill tree
        :param input_file: the file to read
        :return: None
        """
        pass

    def addSkill(self, skill, parent, child):
        """
        Add the given skill to the skill tree (not only in the skill tree representation but also the skill itself)
        :param skill: skill to be added
        :param parent: parent of the skill
        :param child: child of the skill
        :return: None
        """
        pass

    def get_leaves(self, root_node: SkillTreeNode):
        """
        Use the BFS manner, find the leave Nodes of the given root node(available skill to choose)
        :param root_node: the root node to start the search
        :return: a collection of potential node(skill) to master
        """
        pass

    def print_tree(self, layer=3):
        """
        Output the structure of the tree in str manner with layer as the maximum level counting from the root.
        :param layer: maximum layer to print
        :return: a str representing this part of the tree
        """
        """
        My thought of str output:
        See sklearn.tree (decision tree)
        """
        pass

    def is_contained(self, nodes):
        """
        Judge whether the nodes are contained in this given tree
        :param nodes: a list of nodes to be judged
        :return: True if all the nodes are contained
        """
        pass

    def is_contained_and_mastered(self, nodes):
        """
       Judge whether the nodes are contained in this given tree and mastered
       :param nodes: a list of nodes to be judged
       :return: True if all the nodes are contained and mastered
       """
        pass

