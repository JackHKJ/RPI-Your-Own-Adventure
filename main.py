# -*- encoding:utf-8 -*-
# This is the main executive file for the RPI-Your-Own-Adventure Project
# Dependencies
import threading
import tkinter
from gui import *
from gui import UserTypeEnum
from basicClasses.SkillTree import *
from basicClasses.Person import *
from basicClasses.Request import *
import time


avail_list = ['Join 3 clubs', 'Go to a concert in EMPAC', 'Join the fraternity', \
            'Join the sorosity', 'Work out at the RPI gym', 'Take the shuttle around the campus']  # list that is available
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
USER_GATHERER = None

# if __name__ == "__main__":
#     login_thread = GUIThread(loginWindow)
#


if __name__ == "__main__":

    # Load the login page, wait until user choose guest_mode or
    GUI_thread = GUIThread(loginWindow)
    while True:
        if GUI_thread.window is not None and GUI_thread.window.user_type is not None:
            USER_TYPE = GUI_thread.window.user_type
            break
    print("User is {}".format(USER_TYPE))
    # Ensures the tree complete loading
    tree_loader.join()
    print("Finished loading tree")
    # Create the relative information according to the user type
    if USER_TYPE == UserTypeEnum.GUEST:
        User = Person("Guest")
    if USER_TYPE == UserTypeEnum.STUDENT:
        User = Person(GUI_thread.window.RIN)
        User.add_skills_by_shortName(st, GUI_thread.window.gatherer.get_learned_courses())
        st.pretty_print_partial_tree(User.get_skills(), save_fig=True)
        USER_GATHERER = GUI_thread.window.gatherer
    for request in avail_list:
        User.add_avail_request(Request(request,[],""))
    # Open the main page
    while True:
        if GUI_thread.window.next is not None:
            GUI_thread.window = GUI_thread.window.next
            GUI_thread.window.PersonObj = User
            GUI_thread.window.ST = st
            GUI_thread.window.user_type = USER_TYPE
            GUI_thread.window.gatherer = USER_GATHERER
            break

    # Try to show the user skillTree fig
    if USER_TYPE == UserTypeEnum.STUDENT:
        GUI_thread.window.master.title("Updating your Skill Tree...")
        GUI_thread.window.Update_skilltree()
        GUI_thread.window.master.title(TEAM_SLOGAN_STR)

    # pass the person item to the page

    # Enter the main loop:
    while True:
        time.sleep(0.5)
        if GUI_thread.window.sub_page_name is not None:
            print("Switched to window {}".format(GUI_thread.window.sub_page_name))
            while True:
                time.sleep(0.5)
                if GUI_thread.window.sub_page_name is None:
                    print("Returning to the main Page")
                    for skill in User.get_skills():
                        print(str(skill))
                    st.pretty_print_partial_tree(User.get_skills(), root_name=User.name + "-0000", save_fig=True)
                    time.sleep(1)
                    GUI_thread.window.Update_skilltree()
                    break

        if GUI_thread.window.show_skill_flag:
            st.pretty_print_partial_tree(User.get_skills(), root_name=User.name + "-0000", save_fig=False, verbose=True)
            GUI_thread.window.show_skill_flag = False

    print('Reached the end')
