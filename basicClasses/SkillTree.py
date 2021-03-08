# -*- encoding:utf-8 -*-
# Dependencies
import os
from basicClasses.SkillTreeNode import SkillTreeNode
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


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
    # The default color sequence for printing the tree
    root_color = '#777777'
    colors = ['#ffff99', '#ffff00', '#ff9933', '#ff6600', '#ff3300', '#cc0000', '#990000', '#660000', '#705c5c']

    # The entry to the tree
    def __init__(self, root=None, name="#DEFAULT_NAME"):
        """
        Initialization function of the SkillTree
        :param root: optional root node
        :param name: name for this tree
        """
        self.name = name
        if root is not None and isinstance(root, SkillTreeNode):
            self.root_node = root
        else:
            self.root_node = SkillTreeNode(fullName=self.name, shortName=self.name, ID="00000", is_abstract=True)
        self.node_set = set()
        self.node_set.add(self.root_node)
        self.connection = []

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
                ID=row['course_crn'],
                fullName=row['full_name'],
                shortName=row['short_name'])
            pre_req = row['prerequisites']
            if type(pre_req) != str or len(pre_req[1:-1]) == 0:
                self.addSkill(node, parent=self.root_node)
            else:
                pre_req = pre_req[1:-1].split(', ')
                pre_req = list(map(lambda s: s.strip("'"), pre_req))
                for p in pre_req:
                    for n in pool:
                        if n.shortName == p:
                            self.addSkill(node, parent=n)
                            break
            pool.add(node)
            self.node_set.add(node)

    def addSkill(self, skill: SkillTreeNode, parent=None, child=None):
        """
        Add the given skill to the skill tree (not only in the skill tree representation but also the skill itself)
        :param skill: skill to be added
        :param parent: parent of the skill (None as default)
        :param child: child of the skill (None as default)
        :return: None
        """
        if skill in self.node_set:
            # print("Skill already added, returning without operation")
            return
        if parent is not None:
            if isinstance(parent, list):
                for par in parent:
                    par.add_child(skill)
                    skill.add_parent(par)
                    if [str(par), str(child)] not in self.connection:
                        self.connection.append([str(par), str(child)])
            elif isinstance(parent, SkillTreeNode):
                parent.add_child(skill)
                skill.add_parent(parent)
                if [str(skill), str(parent)] not in self.connection:
                    self.connection.append([str(skill), str(parent)])
        if child is not None:
            if isinstance(child, list):
                for chi in child:
                    chi.add_parent(skill)
                    skill.add_child(chi)
                    if [str(chi), str(child)] not in self.connection:
                        self.connection.append([str(chi), str(child)])
            elif isinstance(child, SkillTreeNode):
                child.add_parent(skill)
                skill.add_child(child)
                if [str(skill), str(child)] not in self.connection:
                    self.connection.append([str(skill), str(child)])
        self.node_set.add(skill)

    def remove_skill(self, skill: SkillTreeNode):
        """
        Remove the given skill from the skill tree (not only in the skill tree representation but also the skill itself)
        :param skill: skill to be added
        :return: None
        """
        if skill not in self.node_set:
            print("Skill not exist, returning without operation")
            return
        parLst = skill.get_parent()
        chiLst = skill.get_child()

        for par in parLst:
            if par in self.node_set:
                par.remove_child(skill)
        for chi in chiLst:
            if chi in self.node_set:
                chi.remove_parent(skill)
        self.node_set.remove(skill)

    def get_node_by_ID(self, ID):
        """
        Get the node by ID
        :param ID: The ID of the Node
        :return: Node found by ID, None otherwise
        """
        for node in self.node_set:
            if node.ID == ID:
                return node
        return None

    def get_node_by_shortName(self, shortName):
        """
        Get the Node by shortName
        :param shortName: shortName of the node
        :return: Node found by shortName, None otherwise
        """
        for node in self.node_set:
            if node.shortName == shortName:
                return node
        return None

    def get_node_by_fullName(self, fullName):
        """
        Get the Node by fullName
        :param fullName: fullName of the Node
        :return: Node found by fullName, None otherwise
        """
        for node in self.node_set:
            if node.fullName == fullName:
                return node
        return None

    def get_available_skills(self, person):
        """
        Use the BFS manner, find the leave Nodes of the given root node(available skill to choose)
        :param person: the person to find the skills on
        :return: a collection of potential node(skill) to master
        """
        pass

    def command_print_tree(self, layer=3):
        """
        Output the structure of the tree in str manner with layer as the maximum level counting from the root.
        :param layer: maximum layer to print
        :return: a str representing this part of the tree
        """
        for line in self.root_node.pretty_print_with_height():
            print(line)

    def _pretty_print_helper(self, connection_list):
        g = nx.Graph()
        g.add_edges_from(connection_list)
        pos_counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        pos = dict()
        color_map = []

        for node in g:
            node = str(node)
            if node == str(self.root_node):
                color_map.append(self.root_color)
                pos[node] = [-1, 0]
            elif node[node.rfind('-') + 1:node.rfind('-') + 2].isnumeric():
                hard_level = int(node[node.rfind('-') + 1:node.rfind('-') + 2]) - 1
                color_map.append(self.colors[hard_level])
                pos[node] = [hard_level, pos_counter[hard_level]]
                pos_counter[hard_level] += 1
            else:
                color_map.append('#777777')
        # pos = nx.kamada_kawai_layout(g)
        nx.draw_networkx(g, pos=pos, node_color=color_map, edge_color="#666666")
        plt.show()

    def pretty_print_tree(self):
        """
        This function uses the networkx package to print the whole tree
        :return:
        """
        self._pretty_print_helper(self.connection)

    def pretty_print_partial_tree(self, nodes):
        """
        Print partially of the tree structure, print only the nodes passed in
        :param nodes:
        :return:
        """
        node_str = [str(this_node) for this_node in nodes]
        this_connection = []
        for left, right in self.connection:
            if left in node_str and right in node_str:
                this_connection.append([left, right])

        self._pretty_print_helper(this_connection)

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
