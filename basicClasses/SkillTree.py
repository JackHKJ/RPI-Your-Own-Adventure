# -*- encoding:utf-8 -*-
# Dependencies
import os
from basicClasses.SkillTreeNode import SkillTreeNode
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json


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

    def readSkillTreeFromFileDefaultPath(self):
        """
        read the input file to form a full skill tree
        :return: None
        """
        try:
            home_dir = os.listdir('./data')
        except FileNotFoundError:
            home_dir = os.listdir('../data')

        for term in home_dir:
            try:
                courses = pd.read_csv('./data/{}/courses.csv'.format(term))
            except FileNotFoundError:
                courses = pd.read_csv('../data/{}/courses.csv'.format(term))
            try:
                prereqs = open('./data/{}/prerequisites.json'.format(term), 'r')
            except FileNotFoundError:
                prereqs = open('../data/{}/prerequisites.json'.format(term), 'r')
            prereqs = json.load(prereqs)
            pool = set()
            for i in range(courses.shape[0]):
                row = courses.iloc[i]
                crn = str(row['course_crn'])
                node = SkillTreeNode(
                    ID=crn,
                    fullName=row['full_name'],
                    shortName=row['short_name'])
                if crn not in prereqs or not 'prerequisites' in prereqs[crn]:
                    self.addSkill(node, parent=self.root_node)
                else:
                    p = self.__parse(prereqs[crn]['prerequisites'])
                    flatten = self.__flatten(p)
                    parents = []
                    for p in flatten:
                        for n in pool:
                            if n.shortName == p:
                                parents.append(n)
                    self.addSkill(node, parent=parents)
                pool.add(node)
                self.node_set.add(node)

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

    def _pretty_print_helper(self, connection_list, method, save_fig=False):
        g = nx.Graph()
        g.add_edges_from(connection_list)
        pos_counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        pos = dict()
        color_map = []

        if method == "Stack":
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

        elif method == "Spring":
            for node in g:
                node = str(node)
                if node == str(self.root_node):
                    color_map.append(self.root_color)
                elif node[node.rfind('-') + 1:node.rfind('-') + 2].isnumeric():
                    hard_level = int(node[node.rfind('-') + 1:node.rfind('-') + 2]) - 1
                    color_map.append(self.colors[hard_level])
                    pos_counter[hard_level] += 1
                else:
                    color_map.append('#777777')
            pos = nx.spring_layout(g)
            nx.draw_networkx(g, pos=pos, node_color=color_map, edge_color="#666666")

        if not save_fig:
            plt.show()
        else:
            try:
                plt.savefig(fname="../pic_save/temp_fig.png")
            except FileNotFoundError:
                plt.savefig(fname="./pic_save/temp_fig.png")

    def pretty_print_tree(self, method="Stack", save_fig=False):
        """
        This function uses the networkx package to print the whole tree
        :param method: The method statement is defaulted to 'Stack'
        :param save_fig: The indicator whether to show the fig or to save it in the file
        Method can be ['Stack','Spring']
        :return:
        """
        self._pretty_print_helper(self.connection, method, save_fig=save_fig)

    def pretty_print_partial_tree(self, nodes, method="Stack", save_fig=False):
        """
        Print partially of the tree structure, print only the nodes passed in
        :param nodes: the list of SkillTreeNode to be printed
        :param method: The method statement is defaulted to 'Stack'. Method can be ['Stack','Spring']
        :param save_fig: The indicator whether to show the fig or to save it in the file
        :return:
        """
        node_str = [str(this_node) for this_node in nodes]
        this_connection = []
        for left, right in self.connection:
            if left in node_str and right in node_str:
                this_connection.append([left, right])

        self._pretty_print_helper(this_connection, method, save_fig=save_fig)

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

    def __parse(self, prereq_dict):
        """
        Private method to parse the prerequisites into a list from a dict
        :param prereq_dict: dict that holds the prerequisites of a course
        """
        prereqs = []
        t = prereq_dict['type']
        if t == 'course':
            return prereq_dict['course']
        if t == 'and':
            return [self.__parse(x) for x in prereq_dict['nested']]
        if t == 'or':
            return [[self.__parse(x) for x in prereq_dict['nested']]]
        return t

    def __flatten(self, l):
        """
        Flatten a logical prereq list
        : param l: the list to be flattened
        """
        if type(l) != list:
            return [l]
        ret = []
        for x in l:
            ret += self.__flatten(x)
        return ret
