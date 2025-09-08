import customtkinter
from dbHandling.logonDBHandler import *
from processes.changePassword import *
from processes.windowSuperClass import superWindow
from mainApp import *
from time import sleep
from processes.stockLevelChecker import CheckStockCount
from dbHandling.eventTrackingDBHandler import *
from PIL import Image

customtkinter.set_default_color_theme("dark-blue")

class Logon(superWindow):
    
    APP_NAME = "Login Window"
    WIDTH = 270
    HEIGHT = 330
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(Logon.APP_NAME)
        self.geometry(str(Logon.WIDTH) + "x" + str(Logon.HEIGHT))
        self.minsize(Logon.WIDTH, Logon.HEIGHT)
        self.bind("<Return>", self.logonProcess)
        
        # Configure login frame
        self.loginFrame = customtkinter.CTkFrame(self, corner_radius=10)
        self.loginFrame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        self.loginFrame.grid_columnconfigure(0, weight=1)
        self.loginFrame.grid_columnconfigure(1, weight=1)
        self.loginFrame.grid_rowconfigure(2, weight=1)

        # Logo section
        self.logoFrame = customtkinter.CTkFrame(self.loginFrame, corner_radius=10, fg_color="transparent")
        self.logoFrame.grid(row=0, column=0, columnspan=2, sticky="nsew")  # span 2 columns
        self.logoFrame.grid_columnconfigure(0, weight=1)

        self.personImg = customtkinter.CTkImage(dark_image=Image.open("img/logo.png"), size=(100, 100))
        self.personImgLabel = customtkinter.CTkLabel(self.logoFrame, image=self.personImg, text="")
        self.personImgLabel.grid(row=0, column=0, pady=(20, 20), sticky="n")

        # Entry labels (with alignment)
        self.usernameLabel = customtkinter.CTkLabel(self.loginFrame, text="Username:")
        self.usernameLabel.grid(row=1, column=0, sticky="w", padx=10)
        self.usernameEntry = customtkinter.CTkEntry(self.loginFrame, placeholder_text="username...")
        self.usernameEntry.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.passwordLabel = customtkinter.CTkLabel(self.loginFrame, text="Password:")
        self.passwordLabel.grid(row=2, column=0, sticky="w", padx=10)
        self.passwordEntry = customtkinter.CTkEntry(self.loginFrame, show="*", placeholder_text="password...")
        self.passwordEntry.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        #center buttons
        self.buttonFrame = customtkinter.CTkFrame(self.loginFrame, fg_color="transparent")
        self.buttonFrame.grid(row=3, column=0, columnspan=2, pady=20)

        self.buttonLogon = customtkinter.CTkButton(self.buttonFrame, text="Login", command=self.logonProcess, width=100)
        self.buttonLogon.pack(side="left", padx=10)

        self.buttonExit = customtkinter.CTkButton(self.buttonFrame, text="Exit", command=self.onClosing, width=100)
        self.buttonExit.pack(side="left", padx=10)

        self.lift()
        self.focus_force()
        self.usernameEntry.focus_set()

    def logonProcess(self, event=None):
        self.logon_ = logonDBHandler()
        self.logon_.initializeDatabase()
        print(self.usernameEntry.get(), self.passwordEntry.get())

        login = self.logon_.validateUser(self.usernameEntry.get(), self.passwordEntry.get())
        if login:
            print("Hoorah")
            eventTrackingDB = eventTrackingDBHandler()
            userID = self.logon_.getUserIDByUsername(self.usernameEntry.get())
            eventTrackingDB.logEvent(userID, self.usernameEntry.get(), "Log on")
            self.newWindow()
        
        else:
            self.usernameEntry.configure(text_color="red")
            self.passwordEntry.configure(text_color="red")
            message = popUpWindow("Incorrect username or password")
            message.create()

    def changePasswordWindow(self):
        changePasswordWin = changePassword(False)
        changePasswordWin.mainloop()
        
    def newWindow(self):
        givenLevel = str(self)
        givenUsername = self.usernameEntry.get()
        self.onClosing()
        app = App(givenLevel, givenUsername)
        app.mainloop()

    def __str__(self):
        return self.logon_.getUserAccessLevel(self.usernameEntry.get())

