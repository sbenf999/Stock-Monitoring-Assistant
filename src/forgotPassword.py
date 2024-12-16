import customtkinter
from logonDBHandler import *
from changePassword import *
from windowSuperClass import superWindow

customtkinter.set_default_color_theme("dark-blue")

class forgotPassword(superWindow):
    
    APP_NAME = "Forgot Password"
    WIDTH = 500
    HEIGHT = 250
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(forgotPassword.APP_NAME)
        self.geometry(str(forgotPassword.WIDTH) + "x" + str(forgotPassword.HEIGHT))
        self.minsize(forgotPassword.WIDTH, forgotPassword.HEIGHT)
        
        #create change password frame
        self.forgotPasswordFrame = customtkinter.CTkFrame(self, corner_radius=10)
        self.forgotPasswordFrame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        
        self.usernameLabel = customtkinter.CTkLabel(self.forgotPasswordFrame, text="Enter Username:", anchor="w")
        self.usernameLabel.grid(row=0, column=0)
        
        self.userEntry = customtkinter.CTkEntry(self.forgotPasswordFrame, placeholder_text="Username...")
        self.userEntry.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)
        
        self.leftHandRCLabel = customtkinter.CTkLabel(self.forgotPasswordFrame, text="Left-hand R.C.:", anchor="w")
        self.leftHandRCLabel.grid(row=1, column=0)
        
        self.leftHandRCEntry = customtkinter.CTkEntry(self.forgotPasswordFrame, placeholder_text="Recovery code left-hand...")
        self.leftHandRCEntry.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)
        
        self.rightHandRCLabel = customtkinter.CTkLabel(self.forgotPasswordFrame, text="Right-hand R.C.:", anchor="w")
        self.rightHandRCLabel.grid(row=2, column=0)
        
        self.rightHandRCEntry = customtkinter.CTkEntry(self.forgotPasswordFrame, placeholder_text="Recovery code right-hand...")
        self.rightHandRCEntry.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)
        
        self.buttonValidate = customtkinter.CTkButton(self.forgotPasswordFrame, text="Validate R.C.", command=self.validateRecoveryPassword)
        self.buttonValidate.grid(row=3, column=0, sticky="w", padx=(12, 0), pady=12)
        
        self.buttonExit = customtkinter.CTkButton(self.forgotPasswordFrame, text="Exit", command=self.onClosing)
        self.buttonExit.grid(row=3, column=2, sticky="w", padx=(12, 165), pady=12)
        
    def validateRecoveryPassword(self):
        check = logonDBHandler()
        check.initializeDatabase()
        
        if check.validateRecoveryCode(self.userEntry.get(), self.leftHandRCEntry.get(), self.rightHandRCEntry.get()):
            tempPass = check.genTempPass()
            print(f"Temporary password: {tempPass} - use this password to create a new password")
            message = popUpWindow(f"Temporary password: {tempPass}")
            message.create()
            check.changePasswordOutright(self.userEntry.get(), tempPass)
            self.on_closing()
            # you now need to generate a new recovery code. this code is not displayed to the user, rather emailed, as a form of security.
            changePasswordWin = changePassword()
            changePasswordWin.mainloop()

        else:
            self.userEntry.configure(text_color="red")
            self.leftHandRCEntry.configure(text_color="red")
            self.rightHandRCEntry.configure(text_color="red")
            message = popUpWindow("Incorrect information")
            message.create()

if __name__ == "__main__":
    test = forgotPassword()
    test.mainloop()