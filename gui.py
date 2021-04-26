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
              'Join the sorosity', 'Work out at the RPI gym',
              'Take the shuttle around the campus']  # list that is available
accept_list = []  # list you have accepted
course_list = []


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
    extraWindow = "extraWindow"

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

        # Skill Tree Diagram
        resize_img = Image.open("src/skillTreeDiagramPlaceHolder.png").resize((800, 570))
        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=True, height=True)
        self.master.title(TEAM_SLOGAN_STR)

        self.skillFrame = LabelFrame(self.master, text="Skill Tree Diagram: ", padx=10, pady=12, font=("Georgia", 20))
        self.skillFrame.pack()
        self.skillImg = ImageTk.PhotoImage(resize_img)
        self.label1 = Label(self.skillFrame, image=self.skillImg)
        self.label1.pack()
        self.skillFrame.place(x=0, y=0)

        # Request List
        self.requestFrame = LabelFrame(self.master, text="Request List: ", font=("Georgia", 20))
        self.requestFrame.pack()
        self.request_data = StringVar()
        self.requestList = Listbox(self.requestFrame, width=40, height=37, listvariable=self.request_data)
        self.requestList.pack()
        self.requestFrame.place(x=840, y=0)

        # this is a button sample background
        self.buttonImg = PhotoImage(file="src/buttonSample.png")
        self.buttonImg = self.buttonImg.subsample(2, 2)

        # Add/remove button
        self.add_or_remove = Button(
            self.master,
            text="Add/Remove From SIS",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.addOrRemove()
        )
        self.add_or_remove.config(image=self.buttonImg)
        self.add_or_remove.pack()
        self.add_or_remove.place(x=75, y=650)

        # show skill tree button
        self.show = Button(
            self.master,
            text="Show Skill Tree",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.show_skill()
        )
        self.show.config(image=self.buttonImg)
        self.show.pack()
        self.show.place(x=325, y=650)

        # Add extracurricular button
        self.Add_Extra = Button(
            self.master,
            text="Add extracurricular",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.extra()
        )
        self.Add_Extra.config(image=self.buttonImg)
        self.Add_Extra.pack()
        self.Add_Extra.place(x=575, y=650)

        # Modify requests button
        self.modify_request = Button(
            self.master,
            text="Modify requests",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.ModifyQuest()
        )
        self.modify_request.config(image=self.buttonImg)
        self.modify_request.pack()
        self.modify_request.place(x=825, y=650)

    def Update_skilltree(self):
        """
        Reload the skillTree image from stored path
        """
        resize_img = Image.open('pic_save/temp_fig.png').resize((620, 348))
        self.skillImg = ImageTk.PhotoImage(resize_img)
        self.label1 = Label(self.master, image=self.skillImg)
        self.label1.pack()
        self.label1.place(x=70, y=50)

    def extra(self):
        self.go_extra_page()

    def go_extra_page(self):
        """
        Initialize and go into extracurricular page
        """
        self.sub_page_name = pageEnum.extraWindow
        self.master.deiconify()
        new_window = Toplevel(self.master)
        self.sub_page_window = new_window
        extrapage(new_window, personObj=self.PersonObj, st=self.ST, parent=self)
        new_window.mainloop()

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
        request = requestWindow(newwindow, personObj=self.PersonObj)
        self.master.wait_window(newwindow)
        accept_list = request.return_list()
        self.request_data.set(accept_list)


class extrapage:
    def __init__(self, master, personObj=None, st=None, parent=None):
        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 800) / 2)
        self.h = int((self.screen_height - 600) / 2)
        self.master.geometry(f'800x600+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)
        # Course List

        # ###################################################################################
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
        else:
            self.course_list = ['mock list', 'Operating System', 'Principle of Software', 'Intro to algorithm']
            for item in self.course_list:
                self.course_dict[item] = item

        # self.courseframe=LabelFrame(self.master, text="Course List: ", font=("Georgia", 20))
        # self.courseframe.pack(side=TOP)
        self.course_data = StringVar()
        self.courseList = Listbox(self.master, height=30, width=50, listvariable=self.course_data,selectmode='multiple')

        print(self.added_list)

        for course in self.added_list:
            self.courseList.insert(END, course)

        self.courseList.pack()
        self.courseList.place(x=10, y=10)
        # Extra course
        self.extra_course = StringVar()
        self.extra_entry = Entry(self.master, textvariable=self.extra_course)
        self.extra_entry.insert(0, "Enter Course here")
        self.extra_entry.pack()
        self.extra_entry.place(x=500, y=150, width=150, height=50)

        # this is a button sample background
        self.buttonImg = PhotoImage(file="src/buttonSample.png")
        self.buttonImg = self.buttonImg.subsample(2, 2)
        # Add button
        self.addExtra = Button(
            self.master,
            text="Add",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.add()
        )
        self.addExtra.config(image=self.buttonImg)
        self.addExtra.pack()
        self.addExtra.place(x=500, y=200, width=150, height=50)


    def add(self):
        # print(self.extra_entry.get())
        this_input = str(self.extra_entry.get())
        selected_course_index = []
        if this_input == "Enter Course here" or this_input == "":
            return
        try:
            selected_course_index = self.courseList.curselection()
            # print(selected_course_index)
        except:
            return
        selected_course = [self.ST.get_node_by_shortName(self.courseList.get(index)) for index in selected_course_index]
        this_skill = self.ST.add_custom_skill(skill_name=this_input, parent=selected_course)
        self.PersonObj.add_skill(self.ST, this_skill)



        self.go_back()




    def go_back(self):
        self.parent.sub_page_name = None
        self.parent.sub_page_window = None
        self.master.destroy()


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
        self.course.place(x=0, y=0)
        self.added = Label(master, width=20, text='Added courses', compound='center', font=("Georgia", 25))
        self.added.place(x=350, y=0)
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
        self.statusBar = StringVar()
        self.statusBar.set("Ready")
        self.console = Label(self.master, textvariable=self.statusBar, height=3, relief=SUNKEN, anchor="w")
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
        self.addedList_listbox.place(x=450, y=50)

        # this is a button sample background
        self.buttonImg = PhotoImage(file="src/buttonSample.png")
        self.buttonImg = self.buttonImg.subsample(2, 2)

        # entry for potential added course
        self.potentialCourseName = StringVar
        self.entryPotentialCourse = Entry(self.master, textvariable=self.potentialCourseName)
        self.entryPotentialCourse.insert(0, "Enter course name")
        self.entryPotentialCourse.pack()
        self.entryPotentialCourse.place(x=750, y=50, width=150, height=50)

        # Add button
        self.add = Button(
            self.master,
            text="Add",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.just_add()
        )
        self.add.config(image=self.buttonImg)
        self.add.pack()
        self.add.place(x=740, y=110)

        # remove button
        self.remove = Button(
            self.master,
            text="Remove",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.just_remove()
        )
        self.remove.config(image=self.buttonImg)
        self.remove.pack()
        self.remove.place(x=740, y=180)

        # entry for CRN input
        self.CRN_num = StringVar
        self.entryCRN = Entry(self.master, textvariable=self.CRN_num)
        self.entryCRN.insert(0, "Enter CRN here")
        self.entryCRN.pack()
        self.entryCRN.place(x=750, y=280, width=150, height=50)

        # another add course button
        self.addByCRN = Button(
            self.master,
            text="Add by CRN",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.add_CRN()
        )
        self.addByCRN.config(image=self.buttonImg)
        self.addByCRN.pack()
        self.addByCRN.place(x=740, y=330)

        # entry for filter
        self.filter_text = StringVar
        self.Filter = Entry(self.master, textvariable=self.filter_text)
        self.Filter.insert(0, "Enter Text here")
        self.Filter.pack()
        self.Filter.place(x=750, y=430, width=150, height=50)

        # apply button
        self.Apply = Button(
            self.master,
            text="Apply Filter",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.filter()
        )
        self.Apply.config(image=self.buttonImg)
        self.Apply.pack()
        self.Apply.place(x=740, y=480)

        # go back button
        self.back = Button(
            self.master,
            text="Go Back",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.goBack()
        )
        self.back.config(image=self.buttonImg)
        self.back.pack()
        self.back.place(x=740, y=550)

    def just_add(self):
        """
        Add the selected course from the list to the user skillTree, if nothing is selected, return
        """
        self.statusBar.set("Adding course........")
        self.console.update()
        # print(self.courseList_listbox.curselection()[0])
        if self.courseList_listbox.curselection()[0] is not None and self.courseList_listbox.curselection()[0] >= 0:
            # Get selection and add the skill
            selected = self.courseList_listbox.get(self.courseList_listbox.curselection())
            self.PersonObj.add_skill(self.ST, self.course_dict[selected])
            self.courseList_listbox.delete(self.courseList_listbox.curselection())
            self.course_list.remove(str(self.course_dict[selected]))
            # Update the added skill
            self.addedList_listbox.insert(END, str(self.course_dict[selected]))
            self.added_list.append(str(self.course_dict[selected]))
            self.statusBar.set("Added {}".format(selected))
            self.console.update()

            # Try to add to SIS if logged in
            if self.parent.user_type == UserTypeEnum.STUDENT:
                self.parent.gatherer.add_course_from_SIS()

    def just_remove(self):
        """
        Remove the selected course from the added list, if nothing is selected, return
        """
        self.statusBar.set("Removing course........")
        self.console.update()
        print(self.addedList_listbox.curselection()[0])
        if self.addedList_listbox.curselection()[0] is not None and self.addedList_listbox.curselection()[0] >= 0:
            # Get selection and remove the skill
            selected = self.addedList_listbox.get(self.addedList_listbox.curselection())
            self.PersonObj.remove_skill(self.ST, self.course_dict[selected])
            self.addedList_listbox.delete(self.addedList_listbox.curselection())
            self.added_list.remove(str(self.course_dict[selected]))
            # Update the available skills
            self.courseList_listbox.insert(END, str(self.course_dict[selected]))
            self.course_list.append(str(self.course_dict[selected]))
            self.statusBar.set("Removed {}".format(selected))
            self.console.update()

            # Try to remove from SIS if logged in
            if self.parent.user_type == UserTypeEnum.STUDENT:
                self.parent.gatherer.remove_course_from_SIS()

    def add_CRN(self):
        """
        Add the course by the CRN input, hint when necessary
        """
        self.statusBar.set("Busy!!! Adding course........")
        self.console.update()
        this_input = self.entryCRN.get()
        print(this_input)
        # Try to find the course in the ST:
        this_course = self.ST.get_node_by_ID(this_input)
        if this_course is None:
            self.statusBar.set("No such course found.")
            self.console.update()
            return
        if this_course not in self.PersonObj.get_selectable_courses(self.ST):
            self.statusBar.set("Course cannot be selected, prerequisite not satisfied")
            self.console.update()
            return
        self.filter(force_str=str(this_course))
        self.courseList_listbox.selection_set(0)
        self.just_add()
        self.filter(force_str="$RELOAD$")
        self.statusBar.set("Course is added!!!!!")
        self.console.update()

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

        # Available Request List
        self.avalFrame = LabelFrame(self.master, text="Available Request List: ", font=("Georgia", 20))
        self.avalFrame.pack(side=TOP)
        self.avail_item = StringVar()
        self.avail_item.set(self.PersonObj.get_avail_request())
        self.avail_request = Listbox(self.avalFrame, width=67, height=35, listvariable=self.avail_item)
        self.avail_request.pack()
        self.avalFrame.place(x=50, y=0)

        # Accepted Request List
        self.acceptFrame = LabelFrame(self.master, text="Accepted Request List: ", font=("Georgia", 20))
        self.acceptFrame.pack(side=TOP)
        self.accept_item = StringVar()
        self.accept_item.set(self.PersonObj.get_accept_request())
        self.accept_request = Listbox(self.acceptFrame, width=70, height=35, listvariable=self.accept_item)
        self.accept_request.pack()
        self.acceptFrame.place(x=610, y=0)

        # this is a button sample background
        self.buttonImg = PhotoImage(file="src/buttonSample.png")
        self.buttonImg = self.buttonImg.subsample(2, 2)

        # Accept button
        self.accept = Button(
            self.master,
            text="Accept>>",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.accept_move()
        )
        self.accept.config(image=self.buttonImg)
        self.accept.pack()
        self.accept.place(x=170, y=600)

        # remove button
        self.remove = Button(
            self.master,
            text="<<Remove",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.remove_move()
        )
        self.remove.config(image=self.buttonImg)
        self.remove.pack()
        self.remove.place(x=740, y=600)

        # Check button
        self.check = Button(
            self.master,
            text="Check as finished",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.finished()
        )
        self.check.config(image=self.buttonImg)
        self.check.pack()
        self.check.place(x=740, y=660)

        # Go back button
        self.back = Button(
            self.master,
            text="Go Back",
            compound='center',
            font="arial 10",
            fg="black",
            bd=0,
            command=lambda: self.goBack()
        )
        self.back.config(image=self.buttonImg)
        self.back.pack()
        self.back.place(x=170, y=660)

    def accept_move(self):
        """
        Accept the selected request
        """
        self.PersonObj.add_accept_request(self.PersonObj.remove_avail_request( \
            self.avail_request.get(self.avail_request.curselection())))
        self.avail_item.set(self.PersonObj.get_avail_request())
        self.accept_item.set(self.PersonObj.get_accept_request())

    def remove_move(self):
        """
        Remove the selected request
        """
        self.PersonObj.add_avail_request(self.PersonObj.remove_accept_request( \
            self.accept_request.get(self.accept_request.curselection())))
        self.avail_item.set(self.PersonObj.get_avail_request())
        self.accept_item.set(self.PersonObj.get_accept_request())

    def finished(self):
        """
        Check the selected request as finished
        """
        self.PersonObj.check_finished(self.accept_request.get(self.accept_request.curselection()))
        self.accept_item.set(self.PersonObj.get_accept_request())

    def return_list(self):
        """
        Return the accepted list
        """
        return self.PersonObj.get_accept_request()

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
