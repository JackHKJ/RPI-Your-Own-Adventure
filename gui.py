# -*- encoding:utf-8 -*-
# Dependencies
from tkinter import *
from basicClasses.InfoGatherer import InfoGatherer
from basicClasses.sisscraper import SISscraper
from PIL import Image, ImageTk
import time
import enum

TEAM_SLOGAN_STR = "RPI YOUR OWN ADVENTURE"


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
        self.gatherer = SISscraper(rin=self.RIN_entry.get(), password=self.Password_entry.get())
        # if gather.logged_in:
        #     self.goNext()
        # else:
        #     self.master.title("Failed to log in, please retry.")
        if self.gatherer.login():
            self.user_type = UserTypeEnum.STUDENT
            self.goNext()
        else:
            self.master.title("Failed to log in, please retry.")

    def goNext(self):
        self.master.quit()
        # self.master = Tk()
        self.next = mainWindow(self.master)
        self.master.mainloop()

    # def close_and_create(self):
    #     self.master.destroy()
    #     self.master = Tk()
    #
    # def goto_mainWindow(self):
    #     mainWindow(self.master)
    #     self.master.mainloop()

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

        # resize the image
        skill_tree_path = '../pic_save/place_holder_fig_for_skilltree.png'
        # change the image ratio here

        resize_img = Image.open('pic_save/place_holder_fig_for_skilltree.png').resize((620, 348))

        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)
        self.master.title(TEAM_SLOGAN_STR)
        #####resize skill tree#########
        self.skillImg = ImageTk.PhotoImage(resize_img)
        self.label1 = Label(self.master, image=self.skillImg)
        self.label1.pack()
        self.label1.place(x=70, y=50)
        #####resize skill tree#######
        ######################Request listbox############################
        ################
        # self.courselist=Listbox(self.master,width=50, height=20)
        # #give me a function that can return a courselist
        # for item in ['Operating System', 'Principle of Software', 'Intro to algorithm']:
        #     self.courselist.insert(END, item)
        # self.courselist.pack()
        # self.courselist.place(x=100, y=50)
        ##################
        self.requestlist = Listbox(self.master, width=50, height=20)
        for item in ['Request1', 'Request2', 'Request3', 'Request4', 'Request5', 'Request6']:
            self.requestlist.insert(END, item)
        self.requestlist.pack()
        self.requestlist.place(x=700, y=50)

        self.Add_sis = Button(self.master, text="Add from SIS", compound='center', height=3, width=18,
                              bg='white', command=lambda: self.addSis())
        self.Add_sis.pack()
        self.Add_sis.place(x=100, y=400)

        self.Add_Extra = Button(self.master, text="Add Extracurricular", compound='center',
                                height=3, width=18, bg='white')
        self.Add_Extra.pack()
        self.Add_Extra.place(x=300, y=400)

        self.remove = Button(self.master, text="Remove", height=3, width=18, bg='white', compound='center')
        self.remove.pack()
        self.remove.place(x=500, y=400)

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

    def addSis(self):
        # function main body
        # placeholder
        self.goThird()

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
        newContant = requestWindow(newwindow)
        newwindow.mainloop()


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
        self.courselist = Listbox(self.master, width=50, height=20)
        # Available course list:
        self.course_dict = dict()
        course_list = []
        if self.PersonObj is not None:
            for item in self.PersonObj.get_selectable_courses(self.ST):
                course_list.append(str(item))
                self.course_dict[str(item)] = item
        else:
            course_list = ['mock list', 'Operating System', 'Principle of Software', 'Intro to algorithm']
            for item in course_list:
                self.course_dict[item] = item

        # give me a function that can return a courselist
        for item in course_list:
            self.courselist.insert(END, item)
        self.courselist.pack()
        self.courselist.place(x=100, y=50)
        #############END###################################################
        ##############CRN input#########################
        self.CRN_num = StringVar
        self.CRNinput = Entry(self.master, textvariable=self.CRN_num)
        self.CRNinput.insert(0, "Enter CRN here")
        self.CRNinput.pack()
        self.CRNinput.place(x=600, y=200, width=200, height=50)

        self.addByCRN = Button(self.master, text="Add By CRN", command=lambda: self.add_CRN(), height=3, width=18,
                               bg='white', compound='center')
        self.addByCRN.pack()
        self.addByCRN.place(x=600, y=250)
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

        self.back = Button(self.master, text="Go Back", command=lambda: self.goBack(), height=3, width=18, bg='white',
                           compound='center')
        self.back.pack()
        self.back.place(x=600, y=400)

    def just_add(self):
        self.statusvar.set("Adding course........")
        self.console.update()
        print(self.courselist.curselection()[0])
        if self.courselist.curselection()[0] >= 0:
            selected = self.courselist.get(self.courselist.curselection())
            self.PersonObj.add_skill(self.ST, self.course_dict[selected])
            self.courselist.delete(self.courselist.curselection())
            self.statusvar.set("Added {}".format(selected))
            self.console.update()

            # Try to add to SIS if logged in
            if self.parent.user_type == UserTypeEnum.STUDENT:
                self.parent.gatherer.add_course_from_SIS()

    def add_CRN(self):
        self.statusvar.set("Busy!!! Adding course........")
        self.console.update()
        time.sleep(5)
        self.statusvar.set("Course is added!!!!!")
        ########TO DO: add the course with CRN######
        pass

    def filter(self):
        filter_text = self.Filter.get()
        if filter_text == "" or filter_text == "Filter Text":
            return
        self.courselist.delete(0, self.courselist.size())
        for item in self.PersonObj.get_selectable_courses_filtered(self.ST, filter_text):
            self.courselist.insert(END, item)

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

        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)

        ###############Request processing############
        ####available request#####
        self.avail_request = Listbox(self.master, width=50, height=25)
        for item in ['Request1', 'Request2', 'Request3', 'Request4', 'Request5', 'Request6']:
            self.avail_request.insert(END, item)
        self.avail_request.pack()
        self.avail_request.place(x=100, y=50)
        ######accept request#####
        self.accept_request = Listbox(self.master, width=50, height=25)
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

        self.back = Button(self.master, text="Go Back", command=lambda: self.goBack(), height=3, width=50, bg='white',
                           compound='center')
        self.back.pack()
        self.back.place(x=100, y=600)

    def accept_move(self):
        self.accept_request.insert(0, self.avail_request.get(self.avail_request.curselection()))
        self.avail_request.delete(self.avail_request.curselection())

    def remove_move(self):
        self.avail_request.insert(0, self.accept_request.get(self.accept_request.curselection()))
        self.accept_request.delete(self.accept_request.curselection())

    def finished(self):
        ############TO DO:Update request back to the back end#########################
        pass

    def goBack(self):
        self.master.destroy()


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
