# -*- encoding:utf-8 -*-
# Dependencies
import os
import sys

sys.path.append(os.getcwd())

from basicClasses.Person import Person
from basicClasses.SkillTreeNode import SkillTreeNode
from basicClasses.SkillTree import SkillTree


def Test1_testVisualizationOfPerson_simple():
    Tree = SkillTree(name="Admin")
    nodeA = SkillTreeNode(ID='001', shortName="NODE_A")
    nodeB = SkillTreeNode(ID='002', shortName="NODE_B", fullName="fullName_B")
    nodeC = SkillTreeNode(ID='003', shortName="NODE_C")
    nodeD = SkillTreeNode(ID='004', shortName="NODE_D")

    Tree.addSkill(skill=nodeA, parent=Tree.root_node)
    Tree.addSkill(skill=nodeB, parent=nodeA)
    Tree.addSkill(skill=nodeC, parent=nodeA)
    Tree.addSkill(skill=nodeD, parent=[nodeC,nodeB])

    someone = Person("someone")
    someone.add_skill(Tree, Tree.get_node_by_shortName("NODE_A"))
    someone.add_skill(Tree, Tree.get_node_by_shortName("NODE_B"))
    someone.add_skill(Tree, Tree.get_node_by_shortName("NODE_C"))
    someone.add_skill(Tree, Tree.get_node_by_shortName("NODE_D"))
    someone.visualize_skills()


def Test2_testVisualizationOfPerson_complex():
    st = SkillTree(
        SkillTreeNode(
            ID=1,
            fullName='Computer Science Root',
            shortName='CSCI',
            is_abstract=True),
        'Computer Science Tree')
    try:
        st.readSkillTreeFromFile('./BasicClassTest/test_file.csv')
    except FileNotFoundError:
        st.readSkillTreeFromFile('test_file.csv')

    st.command_print_tree()

    someone = Person("someone")
    someone.add_skill(st, st.get_node_by_shortName("CSCI-1100"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-1200"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-2200"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-2300"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-2600"))

    someone.visualize_skills()

def Test3_partially_print_user_tree():
    st = SkillTree(
        SkillTreeNode(
            ID=1,
            fullName='Computer Science Root',
            shortName='CSCI',
            is_abstract=True),
        'Computer Science Tree')
    try:
        st.readSkillTreeFromFile('./BasicClassTest/test_file.csv')
    except FileNotFoundError:
        st.readSkillTreeFromFile('test_file.csv')

    # st.command_print_tree()

    someone = Person("someone")
    someone.add_skill(st, st.get_node_by_shortName("CSCI-1100"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-1200"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-2200"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-2300"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-2600"))

    st.pretty_print_partial_tree(someone.skills)

if __name__ == "__main__":
    # Test1_testVisualizationOfPerson_simple()
    # Test2_testVisualizationOfPerson_complex()
    Test3_partially_print_user_tree()