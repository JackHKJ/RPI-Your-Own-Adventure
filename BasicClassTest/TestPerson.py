# -*- encoding:utf-8 -*-
# Dependencies
import os
import sys

from basicClasses.InfoGatherer import InfoGatherer

sys.path.append(os.getcwd())

from basicClasses.Person import Person
from basicClasses.SkillTreeNode import SkillTreeNode
from basicClasses.SkillTree import SkillTree


def TreeGenerator():
    st = SkillTree(
        SkillTreeNode(
            ID=1,
            fullName='All Course Root',
            shortName='Root',
            is_abstract=True),
        'Full Course Tree')
    try:
        st.readSkillTreeFromFile('./BasicClassTest/all_courses.csv')
    except FileNotFoundError:
        st.readSkillTreeFromFile('all_courses.csv')
    return st


def Test1_testVisualizationOfPerson_simple():
    Tree = SkillTree(name="Admin")
    nodeA = SkillTreeNode(ID='001', shortName="NODE_A")
    nodeB = SkillTreeNode(ID='002', shortName="NODE_B", fullName="fullName_B")
    nodeC = SkillTreeNode(ID='003', shortName="NODE_C")
    nodeD = SkillTreeNode(ID='004', shortName="NODE_D")

    Tree.addSkill(skill=nodeA, parent=Tree.root_node)
    Tree.addSkill(skill=nodeB, parent=nodeA)
    Tree.addSkill(skill=nodeC, parent=nodeA)
    Tree.addSkill(skill=nodeD, parent=[nodeC, nodeB])

    someone = Person("someone")
    someone.add_skill(Tree, Tree.get_node_by_shortName("NODE_A"))
    someone.add_skill(Tree, Tree.get_node_by_shortName("NODE_B"))
    someone.add_skill(Tree, Tree.get_node_by_shortName("NODE_C"))
    someone.add_skill(Tree, Tree.get_node_by_shortName("NODE_D"))
    Tree.pretty_print_partial_tree(someone.skills)


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

    someone = Person("someone")
    someone.add_skill(st, st.get_node_by_shortName("CSCI-1100"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-1200"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-2200"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-2300"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-2600"))

    st.pretty_print_partial_tree(someone.skills)


def Test3_partially_print_user_tree():
    st = TreeGenerator()
    # st.command_print_tree()

    # st.readSkillTreeFromFileDefaultPath()
    # st.command_print_tree()

    someone = Person("someone")
    someone.add_skill(st, st.get_node_by_shortName("CSCI-1100"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-1200"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-2200"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-2300"))
    someone.add_skill(st, st.get_node_by_shortName("CSCI-2600"))

    st.pretty_print_partial_tree(someone.skills, verbose=False)


def Test4_print_a_real_user_tree():
    st = TreeGenerator()

    gatherer = InfoGatherer(input("Enter your SIS username: "), input("Enter your sis password: "))
    if not gatherer.logged_in:
        raise Exception("Failed to log in")

    someone = Person("someone")
    someone.add_skills_by_shortName(st, gatherer.get_learned_courses())
    st.pretty_print_partial_tree(someone.skills)


def Test5_filter_a_persons_selectable_course():
    st = SkillTree(
        SkillTreeNode(
            ID=1,
            fullName='All Courses Root',
            shortName='Courses',
            is_abstract=True
        ),
        'All Courses Tree')
    st.readSkillTreeFromFileDefaultPath()

    print("################################################################")
    someone = Person("someone")
    someone.add_skill(st, st.get_node_by_shortName("CSCI-1100"))
    print("All the course someone can select")
    print([str(rep) for rep in someone.get_selectable_courses(st)])
    print("################################################################")
    print("With CSCI filter")
    print([str(rep) for rep in someone.get_selectable_courses_filtered(st, "CSCI")])
    print("################################################################")
    print("With full name filter")


def Test6_gusetCourseAvailabilityTest():
    st = TreeGenerator()
    someone = Person("someone")
    print(someone.get_selectable_courses(st))


if __name__ == "__main__":
    # Test1_testVisualizationOfPerson_simple()
    # Test2_testVisualizationOfPerson_complex()
    Test3_partially_print_user_tree()
    # Test4_print_a_real_user_tree()
    # Test5_filter_a_persons_selectable_course()
    # Test6_gusetCourseAvailabilityTest()
