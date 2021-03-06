# -*- encoding:utf-8 -*-
# Dependencies
import os
print(os.getcwd())
from basicClasses.SkillTreeNode import SkillTreeNode
import pandas as pd
import math


class SkillTree():
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
    def __init__(self, root=None, name="#DEFAULT_NAME"):
        self.name = name
        if root is not None and isinstance(root, SkillTreeNode):
            self.root_node = root
        else:
            self.root_node = SkillTreeNode(fullName=self.name, shortName=self.name, ID="00000", is_abstract=True)
        self.node_set = set()
        self.node_set.add(self.root_node)

    def readSkillTreeFromFile(self, input_file):
        """
        read the input file to form a full skill tree
        :param input_file: the file to read
        :return: None
        """
        f = pd.read_csv(input_file)
        pool = set()
        for i in range(f.shape[0]):
            row = f.iloc[i]
            node = SkillTreeNode(
                row['course_crn'],
                row['full_name'],
                row['short_name'])
            prereq = row['prerequisites']
            if type(prereq) != str:
                self.root_node.add_child(node)
            else:
                prereq = prereq[1:-1]
                if len(prereq) == 0:
                    self.root_node.add_child(node)
                else:
                    prereq = prereq.split(', ')
                    prereq = list(map(lambda s: s.strip("'"), prereq))
                    for p in prereq:
                        for n in pool:
                            if n.shortName == p:
                                n.add_child(node)
                                node.add_parent(n)
                                break
            pool.add(node)

    def addSkill(self, skill:SkillTreeNode, parent=None, child=None):
        """
        Add the given skill to the skill tree (not only in the skill tree representation but also the skill itself)
        :param skill: skill to be added
        :param parent: parent of the skill (None as default)
        :param child: child of the skill (None as default)
        :return: None
        """
        if skill in self.node_set:
            print("Skill already added, returning without operation")
            return
        if parent is not None:
            if isinstance(parent,list):
                for par in parent:
                    par.add_child(skill)
                    skill.add_parent(par)
            elif isinstance(parent, SkillTreeNode):
                parent.add_child(skill)
                skill.add_parent(parent)
        if child is not None:
            if isinstance(child,list):
                for chi in child:
                    chi.add_parent(skill)
                    skill.add_child(chi)
            elif isinstance(child, SkillTreeNode):
                child.add_parent(skill)
                skill.add_child(child)
        self.node_set.add(skill)

    def remove_skill(self, skill:SkillTreeNode):
        """
        remove the given skill from the skill tree (not only in the skill tree representation but also the skill itself)
        :param skill: skill to be added
        :param parent: parent of the skill (None as default)
        :param child: child of the skill (None as default)
        :return: None
        """
        pass

    def get_node_by_ID(self, ID):
        """
        Get the node by ID
        :param ID: The ID of the Node
        :return: Node found by ID, None otherwise
        """
        pass

    def get_node_by_shortName(self, shortName):
        """
        Get the Node by shortName
        :param shortName: shortName of the node
        :return: Node found by shortName, None otherwise
        """
        pass

    def get_node_by_fullName(self, fullName):
        """
        Get the Node by fullName
        :param fullName: fullName of the Node
        :return: Node found by fullName, None otherwise
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
        for line in self.root_node.pretty_print_with_height():
            print(line)


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

if __name__ == '__main__':
    st = SkillTree(
        SkillTreeNode(
            ID=1,
            fullName='Computer Science Root', 
            shortName='CSCI',
            is_abstract=True),
        'Computer Science Tree')
    st.readSkillTreeFromFile('test_file.csv')
    st.print_tree()