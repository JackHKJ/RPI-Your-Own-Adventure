# -*- encoding:utf-8 -*-
# Dependencies

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


if __name__ == "__main__":
    Test1_printer_test()