import tkinter as tk
from tkinter import ttk

root = tk.Tk()

b1 = tk.Button(root, text='tk.Button', borderwidth=0)
b1.pack()

s = ttk.Style(root)
s.theme_use('clam')
s.configure('flat.TButton', borderwidth=0)
# s.configure('flat.TButton', relief='flat') gives the same result

b2 = ttk.Button(root, style='flat.TButton', text='ttk.Button')
b2.pack()

