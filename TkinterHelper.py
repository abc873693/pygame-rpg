from tkinter import*
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox


class TKEditBox:
    def __init__(self, title):
        self.root = Tk()
        self.root.title(title)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.width = 300
        self.height = 300
        self.x = (self.screen_width / 2) - (self.width / 2)
        self.y = (self.screen_height / 2) - (self.height / 2)
        self.root.geometry('%dx%d+%d+%d' %
                           (self.width, self.height, self.x, self.y))
        self.root.resizable(0, 0)

        self.NAME = StringVar()
        self.Top = Frame(self.root, width=900, height=50, bd=8, relief="raise")
        self.Top.pack(side=TOP)
        self.Bottom = Frame(self.root, width=900,
                            height=250, bd=8, relief="raise")
        self.Bottom.pack(side=BOTTOM)
        self.Left = Frame(self.root, width=300,
                          height=500, bd=8, relief="raise")
        self.Left.pack(side=LEFT)
        self.Right = Frame(self.root, width=600,
                           height=500, bd=8, relief="raise")
        self.Right.pack(side=RIGHT)
        self.Center = Frame(self.root, width=300,
                            height=50, bd=8, relief="raise")
        self.Center.pack(side=TOP)
        Forms = Frame(self.Top, width=300, height=450)
        Forms.pack(side=TOP)
        Buttons = Frame(self.Bottom, width=0, height=0, bd=8, relief="raise")
        Buttons.pack(side=BOTTOM)
        #==================================ENTRY WIDGET=======================================
        name = Entry(Forms, textvariable=self.NAME, width=30)
        name.grid(row=0, column=1)
        buttonOK = Button(Buttons, width=10, text="確定", command=self.ok)
        buttonOK.pack(side=BOTTOM)

    def ok(self):
        self.root.quit()
        self.root.destroy()

    def loop(self):
        self.root.mainloop()
