# -*- encoding:utf-8 -*-
# This is the main executive file for the RPI-Your-Own-Adventure Project
# Dependencies
import threading
import tkinter
from gui import *
from gui import UserTypeEnum
from basicClasses.SkillTree import *
from basicClasses.Person import *

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


class GUIThread(threading.Thread):


    def __init__(self, window_class):
        super(GUIThread, self).__init__()
        self.window_class = window_class
        self.root = None
        self.window = None
        self.start()

    def callback(self):
        self.root.destroy()

    def run(self):
        self.root = tkinter.Tk()
        # self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.window = self.window_class(self.root)
        self.root.mainloop()




# Global data segment
User = None
USER_TYPE = None

# if __name__ == "__main__":
#     login_thread = GUIThread(loginWindow)
#



if __name__ == "__main__":

    # Load the login page, wait until user choose guest_mode or
    login_thread = GUIThread(loginWindow)
    while True:
        if login_thread.window is not None and login_thread.window.user_type is not None:
            USER_TYPE = login_thread.window.user_type
            break
    print("User is {}".format(USER_TYPE))
    # Ensures the tree complete loading
    tree_loader.join()
    print("Finished loading tree")
    # Create the relative information according to the user type
    if USER_TYPE == UserTypeEnum.GUEST:
        User = Person("Guest")
    if USER_TYPE == UserTypeEnum.STUDENT:
        User = Person(login_thread.window.RIN)
        User.add_skills_by_shortName(st, login_thread.window.gatherer.get_learned_courses())
        st.pretty_print_partial_tree(User.get_skills(), save_fig=True)

    # Close the login page

    # Open the main page
    while True:
        if login_thread.window.next is not None:
            login_thread.window = login_thread.window.next
            break

    # Try to show the user skillTree fig
    if USER_TYPE == UserTypeEnum.STUDENT:
        login_thread.window.Update_skilltree()


    print('Reached the end')
