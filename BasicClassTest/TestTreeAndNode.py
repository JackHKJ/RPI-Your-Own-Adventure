# -*- encoding:utf-8 -*-
# Dependencies
import os
import sys
from basicClasses.SkillTree import SkillTree
from basicClasses.SkillTreeNode import SkillTreeNode

sys.path.append(os.getcwd())


def Test1_printer_test():
    node_a = SkillTreeNode(ID='001', shortName="NODE_A")
    node_b = SkillTreeNode(ID='002', shortName="NODE_B")
    node_c = SkillTreeNode(ID='003', shortName="NODE_C")
    node_d = SkillTreeNode(ID='004', shortName="NODE_D")

    # print(str(node_a))

    node_a.add_child(node_b)
    node_a.add_child(node_c)
    node_b.add_child(node_d)

    for line in node_a.pretty_print_with_height():
        print(line)


def Test2_basicTreeTest():
    tree = SkillTree(name="Admin")
    node_a = SkillTreeNode(ID='001', shortName="NODE_A")
    node_b = SkillTreeNode(ID='002', shortName="NODE_B")
    node_c = SkillTreeNode(ID='003', shortName="NODE_C")
    node_d = SkillTreeNode(ID='004', shortName="NODE_D")

    tree.addSkill(skill=node_a, parent=tree.root_node)
    tree.addSkill(skill=node_b, parent=node_a)
    tree.addSkill(skill=node_c, parent=node_a)
    tree.addSkill(skill=node_d, parent=node_b)

    tree.pretty_print_tree()


def Test3_basicGetNodeTest():
    tree = SkillTree(name="Admin")
    node_a = SkillTreeNode(ID='001', shortName="NODE_A")
    node_b = SkillTreeNode(ID='002', shortName="NODE_B")
    node_c = SkillTreeNode(ID='003', shortName="NODE_C")
    node_d = SkillTreeNode(ID='004', shortName="NODE_D")

    tree.addSkill(skill=node_a, parent=tree.root_node)
    tree.addSkill(skill=node_b, parent=node_a)
    tree.addSkill(skill=node_c, parent=node_a)
    tree.addSkill(skill=node_d, parent=node_b)

    print(tree.get_node_by_ID('001'))
    print(tree.get_node_by_shortName("NODE_B"))
    print(tree.get_node_by_fullName("fullName_B"))

    print(tree.get_node_by_ID('005'))
    print(tree.get_node_by_shortName("NODE_E"))
    print(tree.get_node_by_fullName("fullName_A"))


def Test4_readSkillTreeFromFileTest():
    st = SkillTree(
        SkillTreeNode(
            ID=1,
            fullName='Computer Science Root',
            shortName='CSCI',
            is_abstract=True),
        'Computer Science Tree')
    try:
        st.readSkillTreeFromFile('./BasicClassTest/all_courses.csv')
    except FileNotFoundError:
        st.readSkillTreeFromFile('all_courses.csv')
    # st.command_print_tree()


def Test5_pretty_print_tree():
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
    st.pretty_print_tree()


def Test6_pretty_print_all():
    st = SkillTree(
        SkillTreeNode(
            ID=1,
            fullName='All Courses Root',
            shortName='Courses',
            is_abstract=True
        ),
        'All Courses Tree')

    st.readSkillTreeFromFileDefaultPath()

    # st.command_print_tree()

    # very slow, uncomment carefully
    st.pretty_print_tree()

    # A better way to construct a skill tree for all courses is to have all
    # courses from a single department form their own tree, then attach all tree
    # to one root. For example, all MATH courses and all CSCI courses are in
    # two separate trees. However, this will hide prerequisites from another
    # discipline, i.e. even if CSCI 2200 has MATH 1010 as a prerequisite, the
    # former won't be the latter's child since they are in separate trees. This
    # also requires changes to readSkillTreeFromFile().


def Test7_savefigTest():
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
    st.pretty_print_tree(save_fig=True)


if __name__ == "__main__":
    # Test1_printer_test()
    # Test2_basicTreeTest()
    # Test3_basicGetNodeTest()
    Test4_readSkillTreeFromFileTest()
    # Test5_pretty_print_tree()
    # Test6_pretty_print_all()
    # Test7_savefigTest()
