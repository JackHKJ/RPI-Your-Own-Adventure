# -*- encoding:utf-8 -*-
# Dependencies
from tkinter import *
from basicClasses.InfoGatherer import InfoGatherer
from PIL import Image, ImageTk
import enum
from tkinter import ttk

TEAM_SLOGAN_STR = "RPI YOUR OWN ADVENTURE"
# The following list is a stub when failed to load from SIS
avail_list = ['Join 3 clubs', 'Go to a concert in EMPAC', 'Join the fraternity', \
            'Join the sorosity', 'Work out at the RPI gym', 'Take the shuttle around the campus']  # list that is available
accept_list = []  # list you have accepted


class UserTypeEnum(enum.Enum):
    """
    The Class for representing the user Types
    """
    STUDENT = "STUDENT"
    GUEST = "GUEST"


class pageEnum(enum.Enum):
    """
    The class for representing the current page
    """
    loginWindow = "loginWindow"
    mainWindow = "mainWindow"
    AddSkillPage = "AddSkillPage"
    requestWindow = "requestWindow"


class loginWindow:
    """
    This is the page for user login / Guest mode selection
    """

    def __init__(self, master):
        """
        :param master: the tkinter instance used to initialize the page
        """
        self.master = master
        # Data segment
        self.user_type = None
        self.gatherer = None
        self.RIN = None
        self.next = None
        self.page_name = pageEnum.loginWindow
        """
        define logo title and window dimension
        """
        self.img = PhotoImage(file='src/rpi.gif')
        self.label_img = Label(self.master, image=self.img)
        self.label_img.pack()
        self.screen_width = self.master.maxsize()[0]
        self.screen_height = self.master.maxsize()[1]
        self.w = int((self.screen_width - 600) / 2)
        self.h = int((self.screen_height - 400) / 2)
        self.master.geometry(f'600x400+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)
        self.master.title(TEAM_SLOGAN_STR)

        self.RIN_label = Label(self.master, width=7, text='RIN', compound='center')
        self.RIN_label.place(x=200, y=120)
        self.password_label = Label(self.master, width=7, text='Password: ', compound='center')
        self.password_label.place(x=200, y=120 + 40)

        RIN = StringVar
        password = StringVar

        self.RIN_entry = Entry(self.master, textvariable=RIN, bg='yellow')
        self.RIN_entry.pack()
        self.RIN_entry.place(x=280, y=80 + 40)

        self.Password_entry = Entry(self.master, textvariable=password, show='*', bg='yellow')
        self.Password_entry.pack()
        self.Password_entry.place(x=280, y=120 + 40)

        self.loginButton = Button(self.master, text="Login in as RPI student", width=20, compound='center',
                                  command=lambda: self.check_password(),
                                  fg='black', bg='yellow')
        self.loginButton.pack()
        self.loginButton.place(x=150, y=150 + 40)
        self.guestButton = Button(self.master, text="Guest Mode", width=15, compound='center',
                                  command=lambda: self.guest_mode(), fg='black', bg='yellow')
        self.guestButton.pack()
        self.guestButton.place(x=350, y=150 + 40)

    def check_password(self):
        """
        This function checks the set username and password and set the logged_in status accordingly
        """
        self.master.title("Logging in, please wait")
        self.RIN = self.RIN_entry.get()
        self.gatherer = InfoGatherer(rin=self.RIN_entry.get(), password=self.Password_entry.get())

        if self.gatherer.logged_in:
            self.user_type = UserTypeEnum.STUDENT
            self.goNext()
        else:
            self.master.title("Failed to log in, please retry.")

    def goNext(self):
        """
        Initialize and assign the next page to te current variable
        """
        self.master.quit()
        # self.master = Tk()
        self.label_img.destroy()
        self.next = mainWindow(self.master)
        self.master.mainloop()

    def guest_mode(self):
        """
        Start as guest (no skillTreeNode, an empty Tree is initialized)
        """
        self.user_type = UserTypeEnum.GUEST
        self.goNext()


class mainWindow:
    """
    This is the main page that shows the skill tree, the requests and the available options
    """

    def __init__(self, master):
        """
        :param master: the tkinter instance used to initialize the page
        """
        # Data segment
        self.page_name = pageEnum.mainWindow
        self.sub_page_name = None
        self.sub_page_window = None
        self.PersonObj = None
        self.user_type = None
        self.ST = None
        self.gatherer = None
        self.show_skill_flag = False

        # Resizing the image
        resize_img = Image.open('pic_save/place_holder_fig_for_skilltree.png').resize((800, 570))

        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=True, height=True)
        self.master.title(TEAM_SLOGAN_STR)

        # Resizing the skillTree
        self.skillframe=LabelFrame(self.master, text="Skill Tree Diagram: ",padx=10,pady=12,font=("Georgia", 20))
        self.skillframe.pack()
        self.skillImg = ImageTk.PhotoImage(resize_img)
        self.label1 = Label(self.skillframe, image=self.skillImg)
        self.label1.pack()
        self.skillframe.place(x=0, y=0)

        # The Listbox for storing the Request
        self.requestframe=LabelFrame(self.master, text="Request List: ",font=("Georgia", 20))
        self.requestframe.pack()
        self.request_data = StringVar()
        self.requestlist = Listbox(self.requestframe, width=40, height=34, listvariable=self.request_data)
        self.requestlist.pack()
        self.requestframe.place(x=830, y=0)

        
        self.group = LabelFrame(self.master, text="",padx=200,pady=56)
        self.group.pack(side=BOTTOM)
        # self.add_btn=PhotoImage(file='button_add-remove-from-sis.png')
        # self.test=Button(self.group,image=self.add_btn,borderwidth=0)
        # self.test.pack()
        # self.test.place(x=100,y=600)

        # self.add_btn=PhotoImage(file='button_add-remove-from-sis.gif')
        self.add_or_remove = Button(self.group,text="Add/Remove from SIS", compound='center', height=3, width=18,
                                    bg='white', command=lambda: self.addOrRemove(),borderwidth=0)
        self.add_or_remove.pack(side=LEFT)
        # self.add_or_remove.place(x=100, y=400)

        # Button to show skillTree in a separate window
        # self.show_btn=PhotoImage(file='button_show-the-skill-tree.gif')
        self.show = Button(self.group, text="Show the skill tree", compound='center', height=3, width=18,
                           bg='white', command=lambda: self.show_skill())
        self.show.pack(side=LEFT)
        # self.show.place(x=500, y=400)

        # self.extra_btn=PhotoImage(file='button_add-extracurricular.gif')
        self.Add_Extra = Button(self.group, text="Add extracurricular", compound='center',height=3, width=18,
                                 bg='white')
        self.Add_Extra.pack(side=LEFT)
        # self.Add_Extra.place(x=300, y=400)

        # self.request_btn=PhotoImage(file='button_modify-request.gif')
        self.modify_request = Button(self.group, text="Modify request", height=3, width=18, compound='center',
                                     bg='white', command=lambda: self.ModifyQuest())
        self.modify_request.pack(side=LEFT)
        # self.modify_request.place(x=800, y=400)

    def Update_skilltree(self):
        """
        Reload the skillTree image from stored path
        """
        resize_img = Image.open('pic_save/temp_fig.png').resize((620, 348))
        self.skillImg = ImageTk.PhotoImage(resize_img)
        self.label1 = Label(self.master, image=self.skillImg)
        self.label1.pack()
        self.label1.place(x=70, y=50)

    def addOrRemove(self):
        """
        Switch to the add/remove page
        """
        self.goto_add_remove_page()

    def show_skill(self):
        """
        Show the skillTree in a separate window
        """
        self.show_skill_flag = True

    def goto_add_remove_page(self):
        """
        Initialize and show the add/remove page
        """
        self.sub_page_name = pageEnum.AddSkillPage
        self.master.deiconify()
        new_window = Toplevel(self.master)
        AddSkillPage(new_window, personObj=self.PersonObj, st=self.ST, parent=self)
        self.sub_page_window = new_window
        new_window.mainloop()

    def ModifyQuest(self):
        """
        Goto the request modification page
        """
        self.goto_modify_request_page()

    def goto_modify_request_page(self):
        """
        Initialize the request page and then show it
        """
        self.master.deiconify()
        newwindow = Toplevel(self.master)
        request = requestWindow(newwindow)
        self.master.wait_window(newwindow)
        accept_list = request.return_list()
        self.request_data.set(accept_list)


class AddSkillPage:
    """
    This is the page that allows you modify your skill tree via SIS
    """

    def __init__(self, master, personObj=None, st=None, parent=None):
        """
        :param master: the tkinter instance used to initialize the page
        :param personObj: the Person class instance used to store user info
        :param st: the SkillTree instance for fetching the courses
        :param parent: the parent page of the current page
        """
        self.course = Label(master, width=20, text='CourseList', compound='center', font=("Georgia", 25))
        self.course.place(x=100, y=10)
        self.added = Label(master, width=20, text='Added courses', compound='center', font=("Georgia", 25))
        self.added.place(x=550, y=10)
        # Data segment
        self.page_name = pageEnum.AddSkillPage
        self.PersonObj = personObj
        self.ST = st
        self.parent = parent
        # Listbox representation for displaying the added/available courses
        self.courseList_listbox = None
        self.addedList_listbox = None
        # Data representation for the course/added list as dict
        self.course_dict = None
        # Temp list for addition
        self.course_list = None
        self.added_list = None

        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)

        # Set up the status bar
        self.statusvar = StringVar()
        self.statusvar.set("Ready")
        self.console = Label(self.master, textvariable=self.statusvar, height=3, relief=SUNKEN, anchor="w")
        self.console.pack(side=BOTTOM, fill=X)

        # Set up the course list
        self.courseList_listbox = Listbox(self.master, width=35, height=35)
        # Available course list:
        self.course_dict = dict()
        self.course_list = []
        self.added_list = []

        if self.PersonObj is not None:
            # Update the selectable courses
            for item in self.PersonObj.get_selectable_courses(self.ST):
                self.course_list.append(str(item))
                self.course_dict[str(item)] = item
            # Update the selected courses
            for course in self.PersonObj.get_skills():
                self.added_list.append(str(course))
                self.course_dict[str(course)] = course
        else:
            self.course_list = ['mock list', 'Operating System', 'Principle of Software', 'Intro to algorithm']
            for item in self.course_list:
                self.course_dict[item] = item

        # Show the selectable course in a list
        for item in self.course_list:
            if item not in self.added_list:
                self.courseList_listbox.insert(END, item)
        self.courseList_listbox.pack()
        self.courseList_listbox.place(x=100, y=50)

        # Show the added course in a list
        self.addedList_listbox = Listbox(self.master, width=35, height=35)
        for course in self.added_list:
            self.addedList_listbox.insert(END, course)
        self.addedList_listbox.pack()
        self.addedList_listbox.place(x=550, y=50)

        # CRN input box
        self.CRNframe=LabelFrame(self.master, text="Add/remove")
        self.CRNframe.pack()
        self.CRN_num = StringVar
        # The remove button
        # self.add_btn=PhotoImage(file='button_add.gif')
        self.add = Button(self.CRNframe, text="Add", command=lambda: self.just_add(), height=3, width=18, bg='white',
                          compound='center')
        self.add.pack()
        self.CRNframe.place(x=900, y=50)

        # self.remove_btn=PhotoImage(file='button_remove.gif')
        self.remove = Button(self.CRNframe, text="Remove", command=lambda: self.just_remove(), height=3, width=18,
                             bg='white',
                             compound='center')
        self.remove.pack()
        # self.remove.place(x=900, y=125)
        self.CRNinput = Entry(self.CRNframe, textvariable=self.CRN_num)
        self.CRNinput.insert(0, "Enter CRN here")
        self.CRNinput.pack()
        # self.CRNinput.place(x=900, y=200, width=200, height=50)
        # add course
        # self.CRN_btn=PhotoImage(file='button_add-by-crn.gif')
        self.addByCRN = Button(self.CRNframe, text="Add By CRN", command=lambda: self.add_CRN(), height=3, width=18,
                               bg='white', compound='center')
        self.addByCRN.pack()
        # self.addByCRN.place(x=900, y=250)

        # self.back_btn=PhotoImage(file='button_go-back.gif')
        self.back = Button(self.master, text="Go Back", command=lambda: self.goBack(), height=3, width=18, bg='white',
                           compound='center')
        self.back.pack()
        self.back.place(x=900, y=590)

        # The text input for filtering
        self.filterframe=LabelFrame(self.master, text="Filter Text")
        self.filterframe.pack()
        self.filter_text = StringVar
        # self.filter_btn=PhotoImage(file='button_apply.gif')
        self.Filter = Entry(self.filterframe, textvariable=self.filter_text)
        self.Filter.insert(0, "Enter Text here")
        self.Filter.pack()

        self.filterframe.place(x=900, y=300)
        self.Apply = Button(self.filterframe, text="Apply", command=lambda: self.filter(), height=3, width=18, bg='white',
                            compound='center')
        self.Apply.pack()
        # self.Filter.place(x=900, y=460, width=200, height=60)

    def just_add(self):
        """
        Add the selected course from the list to the user skillTree, if nothing is selected, return
        """
        self.statusvar.set("Adding course........")
        self.console.update()
        print(self.courseList_listbox.curselection()[0])
        if self.courseList_listbox.curselection()[0] is not None and self.courseList_listbox.curselection()[0] >= 0:
            # Get selection and add the skill
            selected = self.courseList_listbox.get(self.courseList_listbox.curselection())
            self.PersonObj.add_skill(self.ST, self.course_dict[selected])
            self.courseList_listbox.delete(self.courseList_listbox.curselection())
            self.course_list.remove(str(self.course_dict[selected]))
            # Update the added skill
            self.addedList_listbox.insert(END, str(self.course_dict[selected]))
            self.added_list.append(str(self.course_dict[selected]))
            self.statusvar.set("Added {}".format(selected))
            self.console.update()

        # Try to add to SIS if logged in
        if self.parent.user_type == UserTypeEnum.STUDENT:
            self.parent.gatherer.add_course_from_SIS()

    def just_remove(self):
        """
        Remove the selected course from the added list, if nothing is selected, return
        """
        self.statusvar.set("Removing course........")
        self.console.update()
        print(self.addedList_listbox.curselection()[0])
        if self.addedList_listbox.curselection()[0] is not None and self.addedList_listbox.curselection()[0] >= 0:
            # Get selection and remove the skill
            selected = self.addedList_listbox.get(self.addedList_listbox.curselection())
            # print(self.course_dict)
            self.PersonObj.remove_skill(self.ST, self.course_dict[selected])
            self.addedList_listbox.delete(self.addedList_listbox.curselection())
            self.added_list.remove(str(self.course_dict[selected]))
            # Update the available skills
            self.courseList_listbox.insert(END, str(self.course_dict[selected]))
            self.course_list.append(str(self.course_dict[selected]))
            self.statusvar.set("Removed {}".format(selected))
            self.console.update()

    def add_CRN(self):
        """
        Add the course by the CRN input, hint when necessary
        """
        self.statusvar.set("Busy!!! Adding course........")
        self.console.update()
        this_input = self.CRNinput.get()
        print(this_input)
        # Try to find the course in the ST:
        this_course = self.ST.get_node_by_ID(this_input)
        if this_course is None:
            self.statusvar.set("No such course found.")
            self.console.update()
            return
        if this_course not in self.PersonObj.get_selectable_courses(self.ST):
            self.statusvar.set("Course cannot be selected, prerequisite not satisfied")
            self.console.update()
            return
        self.filter(force_str=str(this_course))
        self.courseList_listbox.selection_set(0)
        self.just_add()
        self.filter(force_str="$RELOAD$")
        self.statusvar.set("Course is added!!!!!")
        self.console.update()

         # Try to remove from SIS if logged in
        if self.parent.user_type == UserTypeEnum.STUDENT:
            self.parent.gatherer.remove_course_from_SIS()

    def filter(self, force_str=None):
        """
        Filter the selectable course by the given string, null string or default text will not be recognized
        :param force_str: the str used to adjust the status
        """
        if force_str is not None:
            filter_text = force_str
        else:
            filter_text = self.Filter.get()
        if filter_text == "" or filter_text == "Filter Text":
            return
        self.courseList_listbox.delete(0, self.courseList_listbox.size())
        if filter_text == "$RELOAD$":
            for item in self.PersonObj.get_selectable_courses(self.ST):
                self.courseList_listbox.insert(END, item)
        for item in self.PersonObj.get_selectable_courses_filtered(self.ST, filter_text):
            if str(item) not in self.added_list:
                self.courseList_listbox.insert(END, item)

    def goBack(self):
        """
        Go back to the parent page
        """
        self.parent.sub_page_name = None
        self.parent.sub_page_window = None
        self.master.destroy()


class requestWindow:
    """
    The window for modifying the request
    """

    def __init__(self, master, personObj=None, st=None):
        """
        :param master: the tkinter instance used to initialize the page
        :param personObj: the Person class instance used to store user info
        :param st: the SkillTree instance for fetching the courses
        """
        # Data segment
        self.page_name = pageEnum.requestWindow
        self.PersonObj = personObj
        self.ST = st
        self.requestinfo = None

        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 760) / 2)
        self.master.geometry(f'1200x760+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)

        # Selectable request
        self.avalframe=LabelFrame(self.master, text="Available Request List: ",font=("Georgia", 20))
        self.avalframe.pack(side=TOP)
        self.avail_item = StringVar()
        self.avail_item.set(avail_list)
        self.avail_request = Listbox(self.avalframe, width=67, height=35, listvariable=self.avail_item)
        self.avail_request.pack()
        self.avalframe.place(x=0, y=0)

        # Accepted request
        self.acceptframe=LabelFrame(self.master, text="Accepted Request List: ",font=("Georgia", 20))
        self.acceptframe.pack(side=TOP)
        self.accept_item = StringVar()
        self.accept_item.set(accept_list)
        self.accept_request = Listbox(self.acceptframe, width=70, height=35, listvariable=self.accept_item)
        self.accept_request.pack()
        self.acceptframe.place(x=610, y=0)

        # The accept button
        # self.accept_btn=PhotoImage(file='button_accept.gif')
        self.accept = Button(self.avalframe, text="Accept >>", command=lambda: self.accept_move(), height=3, width=50,
                             bg='white', compound='center')
        self.accept.pack(side=RIGHT)
        # self.accept.place(x=100, y=500)

        # The remove button
        # self.remove_btn=PhotoImage(file='button_remove2.gif')
        self.remove = Button(self.acceptframe, text="<< Remove", command=lambda: self.remove_move(), height=3, width=50,
                             bg='white', compound='center')
        self.remove.pack(side=LEFT)
        # self.remove.place(x=600, y=500)
        #bottom frame
        self.bottom_frame=LabelFrame(self.master, text="",padx=120,pady=10)
        self.bottom_frame.pack()
        # The check button
        # self.check_btn=PhotoImage(file='button_check-as-finished.gif')
        self.check = Button(self.bottom_frame, text="Check as finished", command=lambda: self.finished(), height=3, width=50,
                            bg='white', compound='center')
        self.check.pack(side=RIGHT)
        self.bottom_frame.place(x=0,y=680)
        # self.check.place(x=100, y=600)

        # self.back_btn=PhotoImage(file='button_go-back.gif')
        self.back = Button(self.bottom_frame, text="Go Back", command=lambda: self.goBack(), height=3, width=50, bg='white',
                           compound='center')
        self.back.pack(side=LEFT)
        # self.bottom_frame.place(x=600,y=700)
        # self.back.place(x=600, y=600)

    def accept_move(self):
        """
        Accept the selected request
        """
        avail_list.remove(self.avail_request.get(self.avail_request.curselection()))
        accept_list.append(self.avail_request.get(self.avail_request.curselection()))
        self.avail_item.set(avail_list)
        self.accept_item.set(accept_list)

    def remove_move(self):
        """
        Remove the selected request
        """
        accept_list.remove(self.accept_request.get(self.accept_request.curselection()))
        avail_list.append(self.accept_request.get(self.accept_request.curselection()))
        self.avail_item.set(avail_list)
        self.accept_item.set(accept_list)

    def finished(self):
        """
        Check the selected request as finished
        """
        accept_list.remove(self.accept_request.get(self.accept_request.curselection()))
        self.avail_item.set(avail_list)
        self.accept_item.set(accept_list)

    def return_list(self):
        """
        Return the accepted list
        """
        return accept_list
    def goBack(self):
        """
        Go back to the parent page
        """
        self.master.destroy()


if __name__ == "__main__":
    # #Do not use this in the actual runtime
    root = Tk()
    loginWindow(root)
    root.mainloop()
