# -*- encoding:utf-8 -*-
# Dependencies
from tkinter import *
from basicClasses.InfoGatherer import InfoGatherer
from basicClasses.sisscraper import SISscraper
from PIL import Image, ImageTk
import time
import enum

TEAM_SLOGAN_STR = "RPI YOUR OWN ADVENTURE"
# TO DO: connect you request list
avail_list = ['Request1', 'Request2', 'Request3', 'Request4', 'Request5', 'Request6']  # list that is available
accept_list = []  # list you have accepted

COURSE_GATHERER_FLAG = "CRAPER"


# COURSE_GATHERER_FLAG = "CHROME"


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

        self.RIN_lable = Label(self.master, width=7, text='RIN', compound='center')
        self.RIN_lable.place(x=200, y=120)
        self.password_label = Label(self.master, width=7, text='Password: ', compound='center')
        self.password_label.place(x=200, y=120 + 40)

        global RIN, password
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
        self.master.title("Logging in, please wait")
        self.RIN = self.RIN_entry.get()
        if COURSE_GATHERER_FLAG == "CRAPER":
            self.gatherer = SISscraper(rin=self.RIN_entry.get(), password=self.Password_entry.get())
        else:
            self.gatherer = InfoGatherer(username=self.RIN_entry.get(), password=self.Password_entry.get())

        if self.gatherer.logged_in:
            self.user_type = UserTypeEnum.STUDENT
            self.goNext()
        else:
            self.master.title("Failed to log in, please retry.")

    def goNext(self):
        self.master.quit()
        # self.master = Tk()
        self.label_img.destroy()
        self.next = mainWindow(self.master)
        self.master.mainloop()

    def guest_mode(self):
        # # placeholder
        # self.goNext()
        self.user_type = UserTypeEnum.GUEST
        self.goNext()


class mainWindow:
    """
    This is the main page that shows the skill tree, the requests and the available options
    """

    def __init__(self, master):
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

        resize_img = Image.open('pic_save/place_holder_fig_for_skilltree.png').resize((620, 348))

        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=True, height=True)
        self.master.title(TEAM_SLOGAN_STR)

        # Resizing the skillTree
        self.skillImg = ImageTk.PhotoImage(resize_img)
        self.label1 = Label(self.master, image=self.skillImg)
        self.label1.pack()
        self.label1.place(x=70, y=50)

        # The Listbox for storing the Request

        self.request_data = StringVar()
        self.requestlist = Listbox(self.master, width=50, height=20, listvariable=self.request_data)
        self.requestlist.pack()
        self.requestlist.place(x=700, y=50)

        self.add_or_remove = Button(self.master, text="Add/Remove from SIS", compound='center', height=3, width=18,
                                    bg='white', command=lambda: self.addOrRemove())
        self.add_or_remove.pack()
        self.add_or_remove.place(x=100, y=400)

        # Button to show skillTree in a separate window
        self.show = Button(self.master, text="Show the skill tree", compound='center', height=3, width=18,
                           bg='white', command=lambda: self.show_skill())
        self.show.pack()
        self.show.place(x=500, y=400)
        #####End####

        self.Add_Extra = Button(self.master, text="Add Extracurricular", compound='center',
                                height=3, width=18, bg='white')
        self.Add_Extra.pack()
        self.Add_Extra.place(x=300, y=400)

        self.modify_request = Button(self.master, text="Modify Request", height=3, width=24, compound='center',
                                     bg='white', command=lambda: self.ModifyQuest())
        self.modify_request.pack()
        self.modify_request.place(x=800, y=400)

    def Update_skilltree(self):
        resize_img = Image.open('pic_save/temp_fig.png').resize((620, 348))
        self.skillImg = ImageTk.PhotoImage(resize_img)
        self.label1 = Label(self.master, image=self.skillImg)
        self.label1.pack()
        self.label1.place(x=70, y=50)

    def addOrRemove(self):
        # function main body
        # placeholder
        self.goThird()

    def show_skill(self):
        self.show_skill_flag = True

    def goThird(self):
        self.sub_page_name = pageEnum.AddSkillPage
        self.master.deiconify()
        new_window = Toplevel(self.master)
        AddSkillPage(new_window, personObj=self.PersonObj, st=self.ST, parent=self)
        self.sub_page_window = new_window
        new_window.mainloop()

    def ModifyQuest(self):
        # function main body
        # placeholder
        self.goFourth()

    def goFourth(self):
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
        # self.added_dict = None
        # Temp list for addition
        self.course_list = None
        self.added_list = None

        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)
        ###############Statu Bar set up############################
        self.statusvar = StringVar()
        self.statusvar.set("Ready")
        self.console = Label(self.master, textvariable=self.statusvar, height=3, relief=SUNKEN, anchor="w")
        self.console.pack(side=BOTTOM, fill=X)
        ############End#############################

        ##############Courselist set up here################################
        self.courseList_listbox = Listbox(self.master, width=25, height=20)
        # Available course list:
        self.course_dict = dict()
        self.course_list = []
        # self.added_dict = dict()
        self.added_list = []

        if self.PersonObj is not None:
            # Update the selectable courses
            for item in self.PersonObj.get_selectable_courses(self.ST):
                self.course_list.append(str(item))
                self.course_dict[str(item)] = item
            # Update the selected courses
            for course in self.PersonObj.get_skills():
                self.added_list.append(str(course))
                # self.added_dict[str(course)] = course
        else:
            self.course_list = ['mock list', 'Operating System', 'Principle of Software', 'Intro to algorithm']
            for item in self.course_list:
                self.course_dict[item] = item

        # Show the representation in a list
        for item in self.course_list:
            if item not in self.added_list:
                self.courseList_listbox.insert(END, item)
        self.courseList_listbox.pack()
        self.courseList_listbox.place(x=100, y=50)
        #############END###################################################

        self.addedList_listbox = Listbox(self.master, width=25, height=20)
        for course in self.added_list:
            self.addedList_listbox.insert(END, course)
        self.addedList_listbox.pack()
        self.addedList_listbox.place(x=350, y=50)

        ##############CRN input#########################
        self.CRN_num = StringVar
        self.CRNinput = Entry(self.master, textvariable=self.CRN_num)
        self.CRNinput.insert(0, "Enter CRN here")
        self.CRNinput.pack()
        self.CRNinput.place(x=600, y=200, width=200, height=50)
        # add course
        self.addByCRN = Button(self.master, text="Add By CRN", command=lambda: self.add_CRN(), height=3, width=18,
                               bg='white', compound='center')
        self.addByCRN.pack()
        self.addByCRN.place(x=600, y=250)
        # End
        # remove course
        self.removeByCRN = Button(self.master, text="Remove By CRN", command=lambda: self.remove_CRN(), height=3,
                                  width=18,
                                  bg='white', compound='center')
        self.removeByCRN.pack()
        self.removeByCRN.place(x=600, y=300)
        ###############End#################################################
        ##########Filter Text#############################
        self.filter_text = StringVar
        self.Filter = Entry(self.master, textvariable=self.filter_text)
        self.Filter.insert(0, "Filter Text")
        self.Filter.pack()
        self.Filter.place(x=100, y=400, width=200, height=60)

        self.Apply = Button(self.master, text="Apply", command=lambda: self.filter(), height=3, width=18, bg='white',
                            compound='center')
        self.Apply.pack()
        self.Apply.place(x=300, y=400)
        ###########End##################################################
        self.add = Button(self.master, text="ADD", command=lambda: self.just_add(), height=3, width=18, bg='white',
                          compound='center')
        self.add.pack()
        self.add.place(x=600, y=50)

        self.remove = Button(self.master, text="REMOVE", command=lambda: self.just_remove(), height=3, width=18,
                             bg='white',
                             compound='center')
        self.remove.pack()
        self.remove.place(x=600, y=125)

        self.back = Button(self.master, text="Go Back", command=lambda: self.goBack(), height=3, width=18, bg='white',
                           compound='center')
        self.back.pack()
        self.back.place(x=600, y=400)

    def just_add(self):
        self.statusvar.set("Adding course........")
        self.console.update()
        print(self.courseList_listbox.curselection()[0])
        if self.courseList_listbox.curselection()[0] >= 0:
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
        self.statusvar.set("Removing course........")
        self.console.update()
        print(self.addedList_listbox.curselection()[0])
        if self.addedList_listbox.curselection()[0] >= 0:
            # Get selection and remove the skill
            selected = self.addedList_listbox.get(self.addedList_listbox.curselection())
            self.PersonObj.remove_skill(self.ST, self.course_dict[selected])
            self.addedList_listbox.delete(self.addedList_listbox.curselection())
            self.added_list.remove(str(self.course_dict[selected]))
            # Update the available skills
            self.courseList_listbox.insert(END, str(self.course_dict[selected]))
            self.course_list.append(str(self.course_dict[selected]))
            self.statusvar.set("Removed {}".format(selected))
            self.console.update()

            # Try to remove from SIS if logged in
            if self.parent.user_type == UserTypeEnum.STUDENT:
                self.parent.gatherer.remove_course_from_SIS()

    def add_CRN(self):
        self.statusvar.set("Busy!!! Adding course........")
        self.console.update()
        time.sleep(5)
        self.statusvar.set("Course is added!!!!!")
        ########TO DO: add the course with CRN######
        pass

    def remove_CRN(self):
        self.statusvar.set("Busy!!! removing course........")
        self.console.update()
        time.sleep(5)
        self.statusvar.set("Course is removed!!!!!")
        ########TO DO: remove the course with CRN######
        pass

    def filter(self):
        filter_text = self.Filter.get()
        if filter_text == "" or filter_text == "Filter Text":
            return
        self.courseList_listbox.delete(0, self.courseList_listbox.size())
        for item in self.PersonObj.get_selectable_courses_filtered(self.ST, filter_text):
            if str(item) not in self.added_list:
                self.courseList_listbox.insert(END, item)

    def goBack(self):
        self.parent.sub_page_name = None
        self.parent.sub_page_window = None
        self.master.destroy()


class requestWindow():
    def __init__(self, master, personObj=None, st=None):
        # Data segment
        self.page_name = pageEnum.requestWindow
        self.PersonObj = personObj
        self.ST = st
        self.requestinfo = None

        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)

        ###############Request processing############
        ####available request#####
        self.avail_item = StringVar()
        # TO DO: set up the request here
        self.avail_item.set(avail_list)
        self.avail_request = Listbox(self.master, width=50, height=25, listvariable=self.avail_item)
        self.avail_request.pack()
        self.avail_request.place(x=100, y=50)
        ######accept request#####

        self.accept_item = StringVar()
        self.accept_item.set(accept_list)
        self.accept_request = Listbox(self.master, width=50, height=25, listvariable=self.accept_item)
        self.accept_request.pack()
        self.accept_request.place(x=600, y=50)
        ###############End##########################

        self.accept = Button(self.master, text="Accept >>", command=lambda: self.accept_move(), height=3, width=50,
                             bg='white', compound='center')
        self.accept.pack()
        self.accept.place(x=100, y=500)

        self.remove = Button(self.master, text="<< Remove", command=lambda: self.remove_move(), height=3, width=50,
                             bg='white', compound='center')
        self.remove.pack()
        self.remove.place(x=600, y=500)

        self.check = Button(self.master, text="Check as finished", command=lambda: self.finished(), height=3, width=50,
                            bg='white', compound='center')
        self.check.pack()
        self.check.place(x=600, y=600)

        # self.back = Button(self.master, text="Update", command=lambda: self.goBack(), height=3, width=50, bg='white',
        #                    compound='center')
        # self.back.pack()
        # self.back.place(x=100, y=600)

    def accept_move(self):
        # TO DO: sychronize your accept operation with your function
        avail_list.remove(self.avail_request.get(self.avail_request.curselection()))
        accept_list.append(self.avail_request.get(self.avail_request.curselection()))
        self.avail_item.set(avail_list)
        self.accept_item.set(accept_list)

    def remove_move(self):
        # TO DO: sychronize your remove operation with your function
        accept_list.remove(self.accept_request.get(self.accept_request.curselection()))
        avail_list.append(self.accept_request.get(self.accept_request.curselection()))
        self.avail_item.set(avail_list)
        self.accept_item.set(accept_list)

    def finished(self):
        # TO DO: what you wanna do with check as finished buttion
        pass

    def return_list(self):
        return accept_list

    # def goBack(self):
    #     self.master.destroy()


# class App(threading.Thread):
#     def __init__(self):
#         super(App, self).__init__()
#         self.start()
#
#     def callback(self):
#         self.root.quit()
#
#     def run(self):
#         self.root = Tk()
#         self.root.protocol("WM_DELETE_WINDOW", self.callback)
#         loginWindow(self.root)
#         self.root.mainloop()
#


if __name__ == "__main__":
    root = Tk()
    loginWindow(root)
    root.mainloop()
    # App()
    #
    # for i in range(1000):
    #     time.sleep(1)
    #     print(i)
