from tkinter import *

root = Tk()
# make a title
title = Label(root,text = "RPI YOUR OWN ADVENTURE")
# make two buttons
loginButton = Button(root, text = "Login in as RPI student", padx = 30, pady = 10)
guestButton = Button(root, text = "Guest Mode", padx = 30, pady = 10)

# position of
title.grid(row = 0, column = 1)
loginButton.grid(row = 1, column = 0)
guestButton.grid(row = 1, column = 2)



root.mainloop()