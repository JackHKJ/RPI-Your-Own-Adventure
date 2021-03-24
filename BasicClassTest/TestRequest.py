# -*- encoding:utf-8 -*-
# Dependencies
import os
import sys
sys.path.append(os.getcwd())
from basicClasses.Request import Request
from basicClasses.Person import Person
from basicClasses.SkillTreeNode import SkillTreeNode

def Test1_request_test():
    r_a=Request("R1",[["Do something"],["Do B","Do C"]],"Good student")
    someone = Person("someone")
    print(r_a)
    print(r_a.show_prerequisite())
    print(r_a.get_achievement())
    r_a.try_to_complete(someone)
    print(r_a.get_achievement())
    print('Test check_prerequisites():')
    print(r_a.check_prerequisite(someone))
    someone.add_skill(None, SkillTreeNode(1, shortName='Do something'))
    print(r_a.check_prerequisite(someone))
    someone.add_skill(None, SkillTreeNode(2, shortName='Do C'))
    print(r_a.check_prerequisite(someone))
    anotherone = Person('anotherone')
    anotherone.add_skill(None, SkillTreeNode(2, shortName='Do C'))
    anotherone.add_skill(None, SkillTreeNode(3, shortName='Do B'))
    print(r_a.check_prerequisite(anotherone))
    print(r_a)

if __name__ == "__main__":
    Test1_request_test()