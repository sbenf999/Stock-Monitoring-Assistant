import customtkinter
from dbHandling.logonDBHandler import *
from processes.changePassword import *
from processes.windowSuperClass import superWindow

customtkinter.set_default_color_theme("dark-blue")

class newUser(customtkinter.CTkToplevel):
    
    APP_NAME = "New User window"
    WIDTH = 650
    HEIGHT = 325
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(newUser.APP_NAME)
        self.geometry(str(newUser.WIDTH) + "x" + str(newUser.HEIGHT))
        self.minsize(newUser.WIDTH, newUser.HEIGHT)
          
        #create new user frame
        self.newUserFrame = customtkinter.CTkFrame(self, corner_radius=10, width=750)
        self.newUserFrame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

        #create widgets
        self.usernameLabel = customtkinter.CTkLabel(self.newUserFrame, text="New Username:", anchor="w")
        self.usernameLabel.grid(row=0, column=0)
        self.usernameEntry = customtkinter.CTkEntry(self.newUserFrame, placeholder_text="new username...")
        self.usernameEntry.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)
        
        self.passwordLabel = customtkinter.CTkLabel(self.newUserFrame, text="New Password:", anchor="w")
        self.passwordLabel.grid(row=1, column=0)
        self.passwordEntry = customtkinter.CTkEntry(self.newUserFrame, show="*", placeholder_text="new password...")
        self.passwordEntry.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)

        self.confirmpasswordLabel = customtkinter.CTkLabel(self.newUserFrame, text="Confirm password:", anchor="w")
        self.confirmpasswordLabel.grid(row=1, column=3)
        self.confirmpasswordEntry = customtkinter.CTkEntry(self.newUserFrame, show="*", placeholder_text="confirm password...")
        self.confirmpasswordEntry.grid(row=1, column=4, columnspan=2, sticky="nsew", padx=(12), pady=12)

        self.accessLevelLabel = customtkinter.CTkLabel(self.newUserFrame, text="Access level:", anchor="w")
        self.accessLevelLabel.grid(row=2, column=0)
        self.accessLevelEntry = customtkinter.CTkEntry(self.newUserFrame, placeholder_text="access level...")
        self.accessLevelEntry.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)

        self.emailAddrLabel = customtkinter.CTkLabel(self.newUserFrame, text="Email address:", anchor="w")
        self.emailAddrLabel.grid(row=2, column=3)
        self.emailAddrEntry = customtkinter.CTkEntry(self.newUserFrame, placeholder_text="email address...")
        self.emailAddrEntry.grid(row=2, column=4, columnspan=2, sticky="nsew", padx=(12), pady=12)

        #create a seperator to distuinguish between sections
        seperator = customtkinter.CTkFrame(self.newUserFrame, height=1, fg_color="gray")
        seperator.grid(row=3, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        self.createNewUserButton = customtkinter.CTkButton(self.newUserFrame, text="Create new user", command=lambda:self.logonDB.createUserCreds(self.usernameEntry.get(), self.confirmpasswordEntry.get(), self.accessLevelEntry.get(), self.emailAddrEntry.get()))
        self.createNewUserButton.grid(row=4, column=0, sticky="w", padx=(12, 0), pady=12)

        self.buttonExit = customtkinter.CTkButton(self.newUserFrame, text="Exit", command=self.onClosing)
        self.buttonExit.grid(row=4, column=2, sticky="w", padx=(10, 12), pady=12)

        #initialise the logondbhandler for making a new user
        self.logonDB = logonDBHandler()
        self.logonDB.initializeDatabase()

        if (self.confirmpasswordEntry.get() == self.passwordEntry.get()):
            self.createNewUserButton.configure(command=lambda:self.logonDB.createUserCreds(self.usernameEntry.get(), self.confirmpasswordEntry.get(), self.accessLevelEntry.get(), self.emailAddrEntry.get()))

        else:
            self.passwordEntry.configure(text_color="red")
            self.confirmpasswordEntry.configure(text_color="red")

    def onClosing(self, event=0):
        self.destroy()
