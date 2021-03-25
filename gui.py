# -*- encoding:utf-8 -*-
# Dependencies
from tkinter import *
from basicClasses.InfoGatherer import InfoGatherer


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
        self.master.withdraw()
        newwindow = Toplevel(self.master)
        newContant = secondPage(newwindow)
        newwindow.mainloop()

    def guest_mode(self):
        # placeholder
        self.goNext()


class secondPage():
    def __init__(self, master):
        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)

        self.skillImg = PhotoImage(file='skilltree.png')
        self.requestImg = PhotoImage(file='RequestList.png')
        self.label1 = Label(self.master, image=self.skillImg)
        self.label2 = Label(self.master, image=self.requestImg)
        self.label1.pack()
        self.label2.pack()
        self.label1.place(x=100, y=50)
        self.label2.place(x=600, y=50)

        self.Add_sis = Button(self.master, text="Add from SIS", compound='center', height=3, width=18,
                              bg='white', command=lambda: self.addSis())
        self.Add_sis.pack()
        self.Add_sis.place(x=100, y=400)

        self.Add_Extra = Button(self.master, text="Add Extracurricular", compound='center',
                                height=3, width=18, bg='white')
        self.Add_Extra.pack()
        self.Add_Extra.place(x=260, y=400)

        self.remove = Button(self.master, text="Remove", height=3, width=18, bg='white', compound='center')
        self.remove.pack()
        self.remove.place(x=420, y=400)

        self.modify_request = Button(self.master, text="Modify Request", height=3, width=24, compound='center',
                                     bg='white', command=lambda: self.ModifyQuest())
        self.modify_request.pack()
        self.modify_request.place(x=620, y=400)

    def addSis(self):
        # function main body
        # placeholder
        self.goThird()

    def goThird(self):
        self.master.withdraw()
        newwindow = Toplevel(self.master)
        newContant = thirdPage(newwindow)
        newwindow.mainloop()

    def ModifyQuest(self):
        # function main body
        # placeholder
        self.goFourth()

    def goFourth(self):
        self.master.withdraw()
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

        self.img = PhotoImage(file='placeholder3.png')
        self.label1 = Label(self.master, image=self.img)
        self.label1.pack()
        self.label1.place(x=100, y=50)

        self.add = Button(self.master, text="ADD", height=3, width=18, bg='white', compound='center')
        self.add.pack()
        self.add.place(x=600, y=50)

        self.CRNinput = Button(self.master, text="The CRN input textbox", height=3, width=18, bg='white'
                               , compound='center')
        self.CRNinput.pack()
        self.CRNinput.place(x=600, y=200)

        self.Filter = Button(self.master, text="Fliter Text", height=3, width=18, bg='white', compound='center')
        self.Filter.pack()
        self.Filter.place(x=100, y=400)

        self.Apply = Button(self.master, text="Apply", height=3, width=18, bg='white', compound='center')
        self.Apply.pack()
        self.Apply.place(x=300, y=400)

        self.addByCRN = Button(self.master, text="Add By CRN", height=3, width=18, bg='white', compound='center')
        self.addByCRN.pack()
        self.addByCRN.place(x=600, y=400)

        self.add = Button(self.master, text="ADD", height=3, width=18, bg='white', compound='center')
        self.add.pack()
        self.add.place(x=600, y=50)

        # this needed fixed
        self.Console = Button(self.master, text="A console showing the status of addition",
                              height=5, width=70, bg='white', compound='center')
        self.Console.pack()
        self.Console.place(x=100, y=500)


class fourthPage():
    def __init__(self, master):
        self.master = master
        self.screen_width, self.screen_height = self.master.maxsize()
        self.w = int((self.screen_width - 1200) / 2)
        self.h = int((self.screen_height - 800) / 2)
        self.master.geometry(f'1200x800+{self.w}+{self.h}')
        self.master.resizable(width=False, height=False)

        self.img1 = PhotoImage(file='placeholder4_1.png')
        self.img2 = PhotoImage(file='placeholder4_2.png')
        self.label1 = Label(self.master, image=self.img1)
        self.label2 = Label(self.master, image=self.img2)
        self.label1.pack()
        self.label2.pack()
        self.label1.place(x=100, y=50)
        self.label2.place(x=600, y=50)

        self.accept = Button(self.master, text="Accept >>", height=3, width=50, bg='white', compound='center')
        self.accept.pack()
        self.accept.place(x=100, y=500)

        self.remove = Button(self.master, text="<< Remove", height=3, width=50, bg='white', compound='center')
        self.remove.pack()
        self.remove.place(x=600, y=500)

        self.check = Button(self.master, text="Check as finished", height=3, width=50, bg='white', compound='center')
        self.check.pack()
        self.check.place(x=600, y=600)


if __name__ == "__main__":
    root = Tk()
    cls = mainWindow(root)
    root.mainloop()
