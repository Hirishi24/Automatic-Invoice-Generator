from tkinter import *

root = Tk()
root.geometry("400x300")
root.title("Test Window")

label = Label(root, text="Hello, Tkinter!")
label.pack()

root.mainloop()