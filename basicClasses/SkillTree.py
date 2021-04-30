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
    __root_color = '#777777'
    __colors = ['#ffff99', '#ffff00', '#ff9933', '#ff6600', '#ff3300', '#cc0000', '#990000', '#660000', '#705c5c']
    __custom_counter = 0

    # The entry to the tree
    def __init__(self, root=None, name="#DEFAULT_NAME"):
        """
        Initialization function of the SkillTree
        :param root: optional root node
        :param name: name for this tree
        """
        self.__name = name
        if root is not None and isinstance(root, SkillTreeNode):
            self.__root_node = root
        else:
            self.__root_node = SkillTreeNode(fullName=self.__name, shortName=self.__name, ID="00000", is_abstract=True)
        self.__node_set = set()
        self.__node_set.add(self.__root_node)
        self.__connection = []

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
                prerequisites = open('./data/{}/prerequisites.json'.format(term), 'r')
            except FileNotFoundError:
                prerequisites = open('../data/{}/prerequisites.json'.format(term), 'r')
            prerequisites = json.load(prerequisites)
            pool = set()
            for i in range(courses.shape[0]):
                row = courses.iloc[i]
                crn = str(row['course_crn'])
                node = SkillTreeNode(
                    ID=crn,
                    fullName=row['full_name'],
                    shortName=row['short_name'])
                if crn not in prerequisites or 'prerequisites' not in prerequisites[crn]:
                    self.addSkill(node, parent=self.__root_node)
                else:
                    p = self.__parse(prerequisites[crn]['prerequisites'])
                    flatten = self.__flatten(p)
                    parents = []
                    for p in flatten:
                        for n in pool:
                            if n.shortName == p:
                                parents.append(n)
                    self.addSkill(node, parent=parents)
                pool.add(node)
                self.__node_set.add(node)

    def readSkillTreeFromFile(self, input_file):
        """
        read the input file to form a full skill tree
        :param input_file: the file to read
        :return: None
        """
        f = pd.read_csv(input_file)
        find_parents = {}

        dic_by_shortName = {}

        for i in range(f.shape[0]):
            row = f.iloc[i]
            node = SkillTreeNode(
                ID=row['course_crn'],
                fullName=row['full_name'],
                shortName=row['short_name'])
            pre_req = row['prerequisites']
            if type(pre_req) != str or len(pre_req[1:-1]) == 0:
                self.addSkill(node, parent=self.__root_node)
            else:
                find_parents[node] = pre_req
            dic_by_shortName[node.get_shortName()] = node

        # pool = set(find_parents.keys()) | self.node_set
        for node in find_parents:
            parents = []
            pre_req = find_parents[node]
            pre_req = pre_req[1:-1].split(', ')
            pre_req = list(map(lambda s: s.strip("'"), pre_req))
            for p in pre_req:
                if p in dic_by_shortName.keys():
                    parents.append(dic_by_shortName[p])
            self.addSkill(node, parent=parents)

    def get_node_set(self):
        """
        Getter of nodeset
        :return: nodeset
        """
        return self.__node_set
    
    def get_root_node(self):
        """
        Getter of root_node
        :return: root_node
        """
        return self.__root_node

    def addSkill(self, skill: SkillTreeNode, parent=None, child=None):
        """
        Add the given skill to the skill tree (not only in the skill tree representation but also the skill itself)
        :param skill: skill to be added
        :param parent: parent of the skill (None as default)
        :param child: child of the skill (None as default)
        :return: None
        """
        if skill in self.__node_set:
            # print("Skill already added, returning without operation")
            return
        if parent is not None:
            if isinstance(parent, list):
                for par in parent:
                    par.add_child(skill)
                    skill.add_parent(par)
                    if [str(skill), str(par)] not in self.__connection:
                        self.__connection.append([str(skill), str(par)])
            elif isinstance(parent, SkillTreeNode):
                parent.add_child(skill)
                skill.add_parent(parent)
                if [str(skill), str(parent)] not in self.__connection:
                    self.__connection.append([str(skill), str(parent)])

        if child is not None:
            if isinstance(child, list):
                for chi in child:
                    chi.add_parent(skill)
                    skill.add_child(chi)
                    if [str(chi), str(skill)] not in self.__connection:
                        self.__connection.append([str(chi), str(skill)])
            elif isinstance(child, SkillTreeNode):
                child.add_parent(skill)
                skill.add_child(child)
                if [str(child), str(skill)] not in self.__connection:
                    self.__connection.append([str(child), str(skill)])
        self.__node_set.add(skill)

    def add_custom_skill(self, skill_name, parent=None, child=None):
        """
        :param skill_name: str, the name of the custom skill to be added
        :param parent: a list of skillTreeNode to be added as the parent
        :param child: a list of skillTreeNode to be added as the child
        :return: the created skillTreeNode
        """
        this_skill_node = SkillTreeNode(ID="Cus-$" + str(self.__custom_counter), fullName=skill_name,
                                        shortName=skill_name)
        self.__custom_counter += 1
        self.addSkill(skill=this_skill_node, parent=parent, child=child)
        return this_skill_node

    def remove_skill(self, skill: SkillTreeNode):
        """
        Remove the given skill from the skill tree (not only in the skill tree representation but also the skill itself)
        :param skill: skill to be added
        :return: None
        """
        if skill not in self.__node_set:
            print("Skill not exist, returning without operation")
            return
        parLst = skill.get_parent()
        chiLst = skill.get_child()

        for par in parLst:
            if par in self.__node_set:
                par.remove_child(skill)
        for chi in chiLst:
            if chi in self.__node_set:
                chi.remove_parent(skill)
        self.__node_set.remove(skill)

    def get_node_by_ID(self, ID):
        """
        Get the node by ID
        :param ID: The ID of the Node
        :return: Node found by ID, None otherwise
        """
        for node in self.__node_set:
            if node.get_ID() == ID:
                return node
        return None

    def get_node_by_shortName(self, shortName):
        """
        Get the Node by shortName
        :param shortName: shortName of the node
        :return: Node found by shortName, None otherwise
        """
        for node in self.__node_set:
            if node.get_shortName() == shortName:
                return node
        return None

    def get_node_by_fullName(self, fullName):
        """
        Get the Node by fullName
        :param fullName: fullName of the Node
        :return: Node found by fullName, None otherwise
        """
        for node in self.__node_set:
            if node.get_fullName() == fullName:
                return node
        return None

    # def get_available_skills(self, person):
    #     """
    #     Use the BFS manner, find the leave Nodes of the given root node(available skill to choose)
    #     :param person: the person to find the skills on
    #     :return: a collection of potential node(skill) to master
    #     """
    #     pass

    # def command_print_tree(self, layer=3):
    #     """
    #     Output the structure of the tree in str manner with layer as the maximum level counting from the root.
    #     :param layer: maximum layer to print
    #     :return: a str representing this part of the tree
    #     """
    #     for line in self.root_node.pretty_print_with_height():
    #         print(line)

    def _pretty_print_helper(self, connection_list, method, save_fig=False):
        plt.clf()
        g = nx.Graph()
        g.add_edges_from(connection_list)
        pos_counter = [0, 1, 0.1, 1.2, 0.3, 1.4, 0.5, 1.6, 0.7, 1.8]
        pos = dict()
        color_map = []

        if method == "Stack":
            for node in g:
                node = str(node)
                if node == str(self.__root_node):
                    color_map.append(self.__root_color)
                    pos[node] = [-1, 0]
                elif node.find("-") >= 0 and node.rfind("$") == -1 \
                        and node[node.rfind('-') + 1:node.rfind('-') + 2].isnumeric():
                    hard_level = int(node[node.rfind('-') + 1:node.rfind('-') + 2]) - 1
                    color_map.append(self.__colors[hard_level])
                    pos[node] = [hard_level - 0.1 * pos_counter[hard_level], pos_counter[hard_level]]
                    pos_counter[hard_level] += 2
                else:
                    hard_level = 9
                    color_map.append('#777777')
                    pos[node] = [hard_level - 0.1 * pos_counter[hard_level], pos_counter[hard_level]]
                    pos_counter[hard_level] += 2

            # pos = nx.kamada_kawai_layout(g)

            ax1 = plt.subplot(111)
            ax1.margins(0.1)

            nx.draw_networkx(g, pos=pos, node_color=color_map, edge_color="#666666", ax=ax1)

        elif method == "Spring":
            for node in g:
                node = str(node)
                if node == str(self.__root_node):
                    color_map.append(self.__root_color)
                elif node[node.rfind('-') + 1:node.rfind('-') + 2].isnumeric():
                    hard_level = int(node[node.rfind('-') + 1:node.rfind('-') + 2]) - 1
                    color_map.append(self.__colors[hard_level])
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
        self._pretty_print_helper(self.__connection, method, save_fig=save_fig)

    def pretty_print_partial_tree(self, nodes, method="Stack", root_name="root-0000", save_fig=False, verbose=False):
        """
        Print partially of the tree structure, print only the nodes passed in
        :param nodes: the list of SkillTreeNode to be printed
        :param method: The method statement is defaulted to 'Stack'. Method can be ['Stack','Spring']
        :param root_name: The name for the root node, default to 'root'
        :param save_fig: The indicator whether to show the fig or to save it in the file
        :param verbose: if set to True, then print the verbose information of each node
        :return:
        """
        node_str = dict()
        rep_dict = dict()
        if not verbose:
            for this_node in nodes:
                node_str[str(this_node)] = this_node.get_shortName()
                rep_dict[str(this_node)] = this_node
        else:
            for this_node in nodes:
                node_str[str(this_node)] = str(this_node.get_ID()) + ":" + str(this_node.get_shortName())
                rep_dict[str(this_node)] = this_node

        chosen_set = set()
        this_connection = []
        for left, right in self.__connection:
            if left in node_str and right in node_str:
                this_connection.append([node_str[left], node_str[right]])
                chosen_set.add(left)
                chosen_set.add(right)
        for node in node_str:
            # print("THIS NODE IS:")
            # print(node)
            # print(str(rep_dict[node].parent[0]))

            if node in chosen_set and rep_dict[node].get_parent()[0] != self.__root_node:
                continue
            this_connection.append([root_name, node_str[node]])

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

    def __parse(self, prerequisite_dict):
        """
        Private method to parse the prerequisites into a list from a dict
        :param prerequisite_dict: dict that holds the prerequisites of a course
        """
        t = prerequisite_dict['type']
        if t == 'course':
            return prerequisite_dict['course']
        if t == 'and':
            return [self.__parse(x) for x in prerequisite_dict['nested']]
        if t == 'or':
            return [[self.__parse(x) for x in prerequisite_dict['nested']]]
        return t

    def __flatten(self, this_list):
        """
        Flatten a logical prerequisite list
        : param l: the list to be flattened
        """
        if type(this_list) != list:
            return [this_list]
        ret = []
        for x in this_list:
            ret += self.__flatten(x)
        return ret
