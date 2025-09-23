import customtkinter
import tkinter
from tkinter import messagebox
from tksheet import Sheet

from processes.windowSuperClass import *
from dbHandling.DBHandler import *
from dbHandling.logonDBHandler import *

class viewUserAccountWindow(superWindow):
    def __init__(self, windowName="User accounts"):
        self.windowName = windowName

    def create(self):
        self.box = customtkinter.CTk()
        self.box.geometry(f"{900}x{300}")
        self.box.title(self.windowName)
        
        self.sheetFrame = customtkinter.CTkFrame(master=self.box,width=800, height=200, corner_radius=10)
        self.sheetFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        logonDB = logonDBHandler() 
        self.userAccounts = logonDB.readUserCreds() #get the user accounts from the database
        print(self.userAccounts)

        dbHandling = DBHandler() 
        self.tableHeaders = dbHandling.getColumnNames("users") #get the column names for the tksheet headers

        self.userAccountsSheet = Sheet(self.sheetFrame, data=self.userAccounts, header=self.tableHeaders, auto_resize_columns=True, width=800, height=200)
        self.userAccountsSheet.grid(row=0, column=0, padx=5, pady=5)
        self.userAccountsSheet.change_theme("dark_blue")
        self.userAccountsSheet.set_column_widths(110)

        self.box.mainloop()