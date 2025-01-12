import customtkinter
import os
import tkinter
from dbHandling.logonDBHandler import *
from processes.changePassword import *
from processes.windowSuperClass import superWindow
from mainApp import *
from time import sleep

customtkinter.set_default_color_theme("dark-blue")

class Logon(superWindow):
    
    APP_NAME = "Login Window"
    WIDTH = 500
    HEIGHT = 200
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(Logon.APP_NAME)
        self.geometry(str(Logon.WIDTH) + "x" + str(Logon.HEIGHT))
        self.minsize(Logon.WIDTH, Logon.HEIGHT)
          
        #create login frame
        self.loginFrame = customtkinter.CTkFrame(self, corner_radius=10)
        self.loginFrame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        
        #create logon buttons and entries
        self.usernameLabel = customtkinter.CTkLabel(self.loginFrame, text="Enter Username:", anchor="w")
        self.usernameLabel.grid(row=0, column=0)
        
        self.usernameEntry = customtkinter.CTkEntry(self.loginFrame, placeholder_text="Username...")
        self.usernameEntry.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)
        
        self.passwordLabel = customtkinter.CTkLabel(self.loginFrame, text="Enter Password:", anchor="w")
        self.passwordLabel.grid(row=1, column=0)
        
        self.passwordEntry = customtkinter.CTkEntry(self.loginFrame, show="*", placeholder_text="Password...")
        self.passwordEntry.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)
        
        self.buttonLogon = customtkinter.CTkButton(self.loginFrame, text="Login", command=self.logonProcess)
        self.buttonLogon.grid(row=2, column=0, sticky="w", padx=(12, 0), pady=12)
        
        self.buttonChangePassword = customtkinter.CTkButton(self.loginFrame, text="Change password", command=self.changePasswordWindow)
        self.buttonChangePassword.grid(row=2, column=1, sticky="w", padx=(12, 12), pady=12)
        
        self.buttonExit = customtkinter.CTkButton(self.loginFrame, text="Exit", command=self.onClosing)
        self.buttonExit.grid(row=2, column=2, sticky="w", padx=(0, 12), pady=12)

        #test with admin user
        

    def logonProcess(self):
        self.logon_ = logonDBHandler()
        self.logon_.initializeDatabase()

        login = self.logon_.validateUser(self.usernameEntry.get(), self.passwordEntry.get())
        if login:
            print("Hoorah")
            self.newWindow()
        
        else:
            self.usernameEntry.configure(text_color="red")
            self.passwordEntry.configure(text_color="red")
            message = popUpWindow("Incorrect username or password")
            message.create()

    def changePasswordWindow(self):
        changePasswordWin = changePassword()
        changePasswordWin.mainloop()
        
    def newWindow(self):
        givenLevel = str(self)
        givenUsername = self.usernameEntry.get()
        self.onClosing()
        message = popUpWindow("You have successfully logged in")
        message.create()
        app = App(givenLevel, givenUsername)
        app.mainloop()

    def __str__(self):
        return self.logon_.getUserAccessLevel(self.usernameEntry.get())

