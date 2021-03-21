# -*- encoding:utf-8 -*-
# Dependencies
import os
import sys
sys.path.append(os.getcwd())
from basicClasses.Request import Request
from basicClasses.Person import Person


def Test1_request_test():
    r_a=Request("R1",[["Do something"],["Do B","Do C"]],"Good student")
    someone = Person("someone")
    print(r_a.show_prerequisite())
    print(r_a.get_achievement())
    r_a.try_to_complete(someone)
    print(r_a.get_achievement())


if __name__ == "__main__":
    Test1_request_test()