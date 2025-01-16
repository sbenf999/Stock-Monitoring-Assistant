import customtkinter
from dbHandling.logonDBHandler import *
from processes.changePassword import *
from processes.windowSuperClass import superWindow
from mainApp import *

customtkinter.set_default_color_theme("dark-blue")

class newUser(superWindow):
    
    APP_NAME = "New User Window"
    WIDTH = 750
    HEIGHT = 400
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(newUser.APP_NAME)
        self.geometry(str(newUser.WIDTH) + "x" + str(newUser.HEIGHT))
        self.minsize(newUser.WIDTH, newUser.HEIGHT)
          
        #create new user frame
        self.newUserFrame = customtkinter.CTkFrame(self, corner_radius=10)
        self.newUserFrame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        #create widgets
        self.usernameLabel = customtkinter.CTkLabel(self.newUserFrame, text="New Username:", anchor="w")
        self.usernameLabel.grid(row=0, column=0)
        self.usernameEntry = customtkinter.CTkEntry(self.newUserFrame, placeholder_text="new username...")
        self.usernameEntry.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)
        
        self.passwordLabel = customtkinter.CTkLabel(self.newUserFrame, text="New Password:", anchor="w")
        self.passwordLabel.grid(row=0, column=2)
        self.passwordEntry = customtkinter.CTkEntry(self.newUserFrame, show="*", placeholder_text="new password...")
        self.passwordEntry.grid(row=0, column=3, columnspan=2, sticky="nsew", padx=(12), pady=12)

        self.confirmpasswordLabel = customtkinter.CTkLabel(self.newUserFrame, text="confirm Password:", anchor="w")
        self.confirmpasswordLabel.grid(row=1, column=2)
        self.confirmpasswordEntry = customtkinter.CTkEntry(self.newUserFrame, show="*", placeholder_text="confirm password...")
        self.confirmpasswordEntry.grid(row=1, column=3, columnspan=2, sticky="nsew", padx=(12), pady=12)

        self.accessLevelLabel = customtkinter.CTkLabel(self.newUserFrame, text="access level:", anchor="w")
        self.accessLevelLabel.grid(row=2, column=0)
        self.accessLevelEntry = customtkinter.CTkEntry(self.newUserFrame, placeholder_text="access level...")
        self.accessLevelEntry.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)

        self.emailAddrLabel = customtkinter.CTkLabel(self.newUserFrame, text="Email address:", anchor="w")
        self.emailAddrLabel.grid(row=2, column=2)
        self.emailAddrEntry = customtkinter.CTkEntry(self.newUserFrame, placeholder_text="email address...")
        self.emailAddrEntry.grid(row=2, column=3, columnspan=2, sticky="nsew", padx=(12), pady=12)

        #initialise the logondbhandler for making a new user
        self.logonDB = logonDBHandler()
        self.logonDB.initializeDatabase()

        if self.confirmpasswordEntry.get() == self.passwordEntry.get():
            self.createNewUserButton = customtkinter.CTkButton(self.newUserFrame, text="Create new user", command=lambda:self.logonDB.createUserCreds(self.usernameEntry.get(), self.confirmpasswordEntry.get(), self.accessLevelEntry.get(), self.emailAddrEntry.get()))
            self.createNewUserButton.grid(row=2, column=0, sticky="w", padx=(12, 0), pady=12)
            self.onClosing()

        else:
            self.passwordEntry.configure(text_color="red")
            self.confirmpasswordEntry.configure(text_color="red")