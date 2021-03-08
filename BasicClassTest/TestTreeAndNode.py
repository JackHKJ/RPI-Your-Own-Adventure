# -*- encoding:utf-8 -*-
# Dependencies
import os
import sys

sys.path.append(os.getcwd())

from basicClasses.SkillTree import SkillTree
from basicClasses.SkillTreeNode import SkillTreeNode


def Test1_printer_test():
    nodeA = SkillTreeNode(ID='001', shortName="NODE_A")
    nodeB = SkillTreeNode(ID='002', shortName="NODE_B")
    nodeC = SkillTreeNode(ID='003', shortName="NODE_C")
    nodeD = SkillTreeNode(ID='004', shortName="NODE_D")

    # print(str(nodeA))

    nodeA.add_child(nodeB)
    nodeA.add_child(nodeC)
    nodeB.add_child(nodeD)

    for line in nodeA.pretty_print_with_height():
        print(line)


def Test2_basicTreeTest():
    Tree = SkillTree(name="Admin")
    nodeA = SkillTreeNode(ID='001', shortName="NODE_A")
    nodeB = SkillTreeNode(ID='002', shortName="NODE_B")
    nodeC = SkillTreeNode(ID='003', shortName="NODE_C")
    nodeD = SkillTreeNode(ID='004', shortName="NODE_D")

    Tree.addSkill(skill=nodeA, parent=Tree.root_node)
    Tree.addSkill(skill=nodeB, parent=nodeA)
    Tree.addSkill(skill=nodeC, parent=nodeA)
    Tree.addSkill(skill=nodeD, parent=nodeB)

    Tree.print_tree()


def Test3_basicGetNodeTest():
    Tree = SkillTree(name="Admin")
    nodeA = SkillTreeNode(ID='001', shortName="NODE_A")
    nodeB = SkillTreeNode(ID='002', shortName="NODE_B", fullName="fullName_B")
    nodeC = SkillTreeNode(ID='003', shortName="NODE_C")
    nodeD = SkillTreeNode(ID='004', shortName="NODE_D")

    Tree.addSkill(skill=nodeA, parent=Tree.root_node)
    Tree.addSkill(skill=nodeB, parent=nodeA)
    Tree.addSkill(skill=nodeC, parent=nodeA)
    Tree.addSkill(skill=nodeD, parent=nodeB)

    print(Tree.get_node_by_ID('001'))
    print(Tree.get_node_by_shortName("NODE_B"))
    print(Tree.get_node_by_fullName("fullName_B"))

    print(Tree.get_node_by_ID('005'))
    print(Tree.get_node_by_shortName("NODE_E"))
    print(Tree.get_node_by_fullName("fullName_A"))


def Test3_readSkillTreeFromFileTest():
    st = SkillTree(
        SkillTreeNode(
            ID=1,
            fullName='Computer Science Root',
            shortName='CSCI',
            is_abstract=True),
        'Computer Science Tree')
    st.readSkillTreeFromFile('./BasicClassTest/test_file.csv')
    st.print_tree()


if __name__ == "__main__":
    # Test1_printer_test()
    # Test2_basicTreeTest()
    Test3_readSkillTreeFromFileTest()
