# -*- encoding:utf-8 -*-
# This is the main executive file for the RPI-Your-Own-Adventure Project
# Dependencies
import threading
from gui import *
from gui import UserTypeEnum
from basicClasses.SkillTree import *
from basicClasses.Person import *


# Global variables


class GUIThread(threading.Thread):
    def __init__(self, window_class):
        super(GUIThread, self).__init__()
        self.window_class = window_class
        self.root = None
        self.window = None
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.window = self.window_class(self.root)
        self.root.mainloop()


# Load the SkillTree
st = SkillTree(
    SkillTreeNode(
        ID=00000000,
        fullName='All Course Root',
        shortName='Root',
        is_abstract=True),
    'Full Course Tree')
tree_loader = threading.Thread(target=st.readSkillTreeFromFile, args=['./BasicClassTest/all_courses.csv'])
tree_loader.start()


# Global data segment
User = None
USER_TYPE = None

if __name__ == "__main__":
    # Load the login page, wait until user choose guest_mode or
    login_thread = GUIThread(loginWindow)
    while True:
        if login_thread.window is not None and login_thread.window.user_type is not None:
            USER_TYPE = login_thread.window.user_type
            break
    print("User is {}".format(login_thread.window.user_type))
    # Ensures the tree complete loading
    tree_loader.join()

    # Create the relative information according to the user type


    for i in range(1000):
        time.sleep(1)
        print(i)
