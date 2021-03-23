from tkinter import *
import tkinter.messagebox as messagebox
#Require Jack He to implement this part
#After you run this program: Enter 'test' for RIN, '123' for password
def check_password(root,RIN_entry,Password_entry):
    if RIN_entry.get() != 'test' or  Password_entry.get() !='123':
        messagebox.showerror('ERROR','Wrong password or RIN number')
    else:
        messagebox.showinfo('Correct','Welcome to RPI-Your-Own-Adventure Project')
        login_windows(root)
def guest_mode(root):
    messagebox.showinfo('Start',"Welcome to RPI-Your-Own-Adventure Project")
    guest_windows(root)
##############Next window Design#######################
def login_windows(root):
    nextwindow=Toplevel(root)
    nextwindow.geometry('300x400')
    nextwindow.title('New windows')
def guest_windows(root):
    nextwindow=Toplevel(root)
    nextwindow.geometry('300x400')
    nextwindow.title('New windows')
##############end###################################
def main_windows():
    root = Tk()
    img=PhotoImage(file='rpi.png')
    label_img=Label(root,image=img)
    label_img.pack()
    # set the size of the window
    #get the screen size of the laptop
    screen_width,screen_height = root.maxsize()
    w = int((screen_width-600)/2)
    h = int((screen_height-400)/2)
    #set background color
    #root.configure(bg='gray')
    #set the window size according to the screen size(it will be in the middle of the screen)
    root.geometry(f'600x400+{w}+{h}')
    root.resizable(width=False, height=False)#window resizable
    # make a title
    root.title('RPI YOUR OWN ADVENTURE')
    # Setting the label for RIN number and password
    RIN_label =Label(root,width=7,text='RIN: ',compound='center')
    RIN_label.place(x=200,y=80+40)
    password_label =Label(root,width=7,text='Password: ',compound='center')
    password_label.place(x=200,y=120+40)
    #Setting entry for RIN and password
    global RIN,password
    RIN=StringVar
    password=StringVar
    ##########login in account########
    RIN_entry=Entry(root,textvariable=RIN,bg='yellow')#RIN
    RIN_entry.pack()
    RIN_entry.place(x=280,y=80+40)
    Password_entry=Entry(root,textvariable=password,show='*',bg='yellow')#password
    Password_entry.pack()
    Password_entry.place(x=280,y=120+40)
    ## make two buttons
    loginButton = Button(root,text = "Login in as RPI student",width=20,compound='center',command = lambda :check_password(root,RIN_entry,Password_entry),fg='black',bg='yellow')
    loginButton.pack()
    guestButton =Button(root,text="Guest Mode",width=15,compound='center',command=lambda: guest_mode(root),fg='black',bg='yellow')
    guestButton.pack()
    ##set position of buttion
    loginButton.place(x=150,y=150+40)
    guestButton.place(x=350,y=150+40)

    # guestButton = Button(root, text = "Guest Mode", padx = 30, pady = 10)

    # # position of
    # loginButton.grid(row = 5, column = 0)
    # guestButton.grid(row = 5, column = 2)

    root.mainloop()
main_windows()