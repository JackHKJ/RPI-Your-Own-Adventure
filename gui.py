# -*- encoding:utf-8 -*-
# Dependencies
from tkinter import *
from basicClasses.InfoGatherer import InfoGatherer
from PIL import Image, ImageTk
import time

class mainWindow():
    """
    This is the First page
    """

    def __init__(self, master):
        self.master = master
        """
        define logo title and window dimension
        """
        self.img = PhotoImage(file='rpi.gif')
        self.label_img = Label(self.master, image=self.img)
        self.label_img.pack()
        self.screen_width = master.maxsize()[0]
        self.screen_height = master.maxsize()[1]
        self.w = int((self.screen_width - 600) / 2)
        self.h = int((self.screen_height - 400) / 2)
        self.master.geometry(f'600x400+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)
        self.master.title("RPI YOUR OWN ADVENTURE")

        self.RIN_lable = Label(self.master, width=7, text='RIN', compound='center')
        self.RIN_lable.place(x=200, y=120)
        self.password_label = Label(root, width=7, text='Password: ', compound='center')
        self.password_label.place(x=200, y=120 + 40)

        global RIN, password
        RIN = StringVar
        password = StringVar

        self.RIN_entry = Entry(root, textvariable=RIN, bg='yellow')
        self.RIN_entry.pack()
        self.RIN_entry.place(x=280, y=80 + 40)

        self.Password_entry = Entry(root, textvariable=password, show='*', bg='yellow')
        self.Password_entry.pack()
        self.Password_entry.place(x=280, y=120 + 40)

        self.loginButton = Button(root, text="Login in as RPI student", width=20, compound='center',
                                  command=lambda: self.check_password(),
                                  fg='black', bg='yellow')
        self.loginButton.pack()
        self.loginButton.place(x=150, y=150 + 40)
        self.guestButton = Button(root, text="Guest Mode", width=15, compound='center',
                                  command=lambda: self.guest_mode(), fg='black', bg='yellow')
        self.guestButton.pack()
        self.guestButton.place(x=350, y=150 + 40)

    def check_password(self):
        gather = InfoGatherer(username=self.RIN_entry.get(), password=self.Password_entry.get())
        if gather.logged_in:
            self.goNext()
        else:
            self.master.title("Failed to log in, please retry.")

    def goNext(self):
        self.master.destroy()
        newwindow = Tk()
        newContant = secondPage(newwindow)
        newwindow.mainloop()

    def guest_mode(self):
        # placeholder
        self.goNext()


class secondPage():
    def __init__(self, master):
        #resize the image
        skill_tree_path='pic_save/temp_fig.png'
        #change the image ratio here
        resize_img=Image.open(skill_tree_path).resize((620,348))      

        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)
        self.master.title("RPI YOUR OWN ADVENTURE")
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
        self.requestlist=Listbox(self.master,width=50, height=20)
        for item in ['Request1', 'Request2', 'Request3','Request4', 'Request5', 'Request6']:
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

    def addSis(self):
        # function main body
        # placeholder
        self.goThird()

    def goThird(self):
        self.master.deiconify()
        newwindow = Toplevel(self.master)
        newContant = thirdPage(newwindow)
        newwindow.mainloop()

    def ModifyQuest(self):
        # function main body
        # placeholder
        self.goFourth()

    def goFourth(self):
        self.master.deiconify()
        newwindow = Toplevel(self.master)
        newContant = fourthPage(newwindow)
        newwindow.mainloop()


class thirdPage():
    def __init__(self, master):
        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)
        ###############Statu Bar set up############################
        self.statusvar=StringVar()
        self.statusvar.set("Ready")
        self.console=Label(self.master, textvariable=self.statusvar,height=3, relief=SUNKEN, anchor="w")
        self.console.pack(side=BOTTOM, fill=X)
        ############End#############################

        ##############Courselist set up here################################
        self.courselist=Listbox(self.master,width=50, height=20)
        #give me a function that can return a courselist
        for item in ['Operating System', 'Principle of Software', 'Intro to algorithm']:
            self.courselist.insert(END, item)
        self.courselist.pack()
        self.courselist.place(x=100, y=50)
        #############END###################################################
        ##############CRN input#########################
        self.CRN_num=StringVar
        self.CRNinput=Entry(self.master,textvariable=self.CRN_num)
        self.CRNinput.insert(0,"Enter CRN here")
        self.CRNinput.pack()
        self.CRNinput.place(x=600, y=200,width=200, height=50)

        self.addByCRN = Button(self.master, text="Add By CRN",command=lambda: self.add_CRN(),height=3, width=18, bg='white', compound='center')
        self.addByCRN.pack()
        self.addByCRN.place(x=600, y=250)
        ###############End#################################################
        ##########Filter Text#############################
        self.filter_text=StringVar
        self.Filter = Entry(self.master,textvariable=self.filter_text)
        self.Filter.insert(0,"Filter Text")
        self.Filter.pack()
        self.Filter.place(x=100, y=400,width=200, height=60)

        self.Apply = Button(self.master, text="Apply",command=lambda: self.filter(), height=3, width=18, bg='white', compound='center')
        self.Apply.pack()
        self.Apply.place(x=300, y=400)
        ###########End##################################################
        self.add = Button(self.master, text="ADD",command=lambda: self.add_CRN(), height=3, width=18, bg='white', compound='center')
        self.add.pack()
        self.add.place(x=600, y=50)
    def just_add(self):
        self.statusvar.set("Busy!!! Adding course........")
        self.console.update()
        time.sleep(5)
        self.statusvar.set("Course is added!!!!!")
        ########TO DO: add the course######
        pass
    def add_CRN(self):
        self.statusvar.set("Busy!!! Adding course........")
        self.console.update()
        time.sleep(5)
        self.statusvar.set("Course is added!!!!!")
        ########TO DO: add the course with CRN######
        pass
    def filter(self):
        self.statusvar.set("Busy!!! Filtering Text..........")
        self.console.update()
        time.sleep(5)
        self.statusvar.set("The course is founded")
        ########TO DO: filter
        pass



class fourthPage():
    def __init__(self, master):
        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)


        ###############Request processing############
        ####available request#####
        self.avail_request=Listbox(self.master,width=50, height=25)
        for item in ['Request1', 'Request2', 'Request3','Request4', 'Request5', 'Request6']:
            self.avail_request.insert(END,item)
        self.avail_request.pack()
        self.avail_request.place(x=100, y=50)
        ######accept request#####
        self.accept_request=Listbox(self.master,width=50, height=25)
        self.accept_request.pack()
        self.accept_request.place(x=600, y=50)
        ###############End##########################

        self.accept = Button(self.master, text="Accept >>",command=lambda:self.accept_move(),height=3, width=50, bg='white', compound='center')
        self.accept.pack()
        self.accept.place(x=100, y=500)

        self.remove = Button(self.master, text="<< Remove",command=lambda:self.remove_move(), height=3, width=50, bg='white', compound='center')
        self.remove.pack()
        self.remove.place(x=600, y=500)

        self.check = Button(self.master, text="Check as finished", command=lambda:self.finished(),height=3, width=50, bg='white', compound='center')
        self.check.pack()
        self.check.place(x=600, y=600)
    def accept_move(self):
        self.accept_request.insert(0,self.avail_request.get(self.avail_request.curselection()))
        self.avail_request.delete(self.avail_request.curselection())
    def remove_move(self):
        self.avail_request.insert(0,self.accept_request.get(self.accept_request.curselection()))
        self.accept_request.delete(self.accept_request.curselection())
    def finished(self):
        ############TO DO:Update request back to the back end#########################
        pass


if __name__ == "__main__":
    root = Tk()
    cls = mainWindow(root)
    root.mainloop()
