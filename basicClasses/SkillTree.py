# -*- encoding:utf-8 -*-
# Dependencies
from basicClasses.SkillTreeNode import SkillTreeNode


class SkillTree:
    """
    This is the FullSkillTree class that is designed for:
    1. Show one's achieved skill
    2. Show availability of selectable courses/skills
    other usage may be extended
    """
    """
    Use a set to manage all the learned skills, each is a node pointing to its parent
    1. prerequisite check: inclusive check using in
    2. adding child: manage the parent pointer
    """

    # The entry to the tree
    def __init__(self, root=None):
        if root is None:
            self.root_node = None
            return
        self.root_node = SkillTreeNode(fullName="$ROOTNODE$", shortName="$ROOTNODE$", ID="00000", is_abstract=True)

    def readSkillTreeFromFile(self, input_file):
        """
        read the input file to form a full skill tree
        :param input_file: the file to read
        :return: None
        """
        pass

    def addSkill(self, skill, parent=None, child=None):
        """
        Add the given skill to the skill tree (not only in the skill tree representation but also the skill itself)
        :param skill: skill to be added
        :param parent: parent of the skill (None as default)
        :param child: child of the skill (None as default)
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

    def print_whole_tree(self):
        for line in self.root_node.pretty_print_with_height():
            print(line)




