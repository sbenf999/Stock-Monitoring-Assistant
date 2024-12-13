import customtkinter
from logonDBHandler import *

customtkinter.set_default_color_theme("dark-blue")

class changePassword(customtkinter.CTk):
    
    APP_NAME = "Change Password"
    WIDTH = 500
    HEIGHT = 250
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(changePassword.APP_NAME)
        self.geometry(str(changePassword.WIDTH) + "x" + str(changePassword.HEIGHT))
        self.minsize(changePassword.WIDTH, changePassword.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Shift-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)
        self.after(201, lambda :self.iconbitmap('person.ico'))
        
        #create change password frame
        self.changePasswordFrame = customtkinter.CTkFrame(self, corner_radius=10)
        self.changePasswordFrame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        
        self.usernameLabel = customtkinter.CTkLabel(self.changePasswordFrame, text="Enter Username:", anchor="w")
        self.usernameLabel.grid(row=0, column=0)
        
        self.usernameEntry = customtkinter.CTkEntry(self.changePasswordFrame, placeholder_text="Username...")
        self.usernameEntry.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)
        
        self.oldPasswordLabel = customtkinter.CTkLabel(self.changePasswordFrame, text="Enter Old Password:", anchor="w")
        self.oldPasswordLabel.grid(row=1, column=0)
        
        self.oldPasswordEntry = customtkinter.CTkEntry(self.changePasswordFrame, show="*", placeholder_text="Old Password...")
        self.oldPasswordEntry.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)
        
        self.newPasswordLabel = customtkinter.CTkLabel(self.changePasswordFrame, text="Enter New Password:", anchor="w")
        self.newPasswordLabel.grid(row=2, column=0)
        
        self.newPasswordEntry = customtkinter.CTkEntry(self.changePasswordFrame, show="*", placeholder_text="New Password...")
        self.newPasswordEntry.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)
        
        self.buttonChangePassword = customtkinter.CTkButton(self.changePasswordFrame, text="Change", command=self.change)
        self.buttonChangePassword.grid(row=3, column=0, sticky="w", padx=(12, 0), pady=12)
        
        self.buttonForgotPassword = customtkinter.CTkButton(self.changePasswordFrame, text="Forgot password", command=self.forgotPassword)
        self.buttonForgotPassword.grid(row=3, column=1, sticky="w", padx=(12, 12), pady=12)
        
        self.buttonExit = customtkinter.CTkButton(self.changePasswordFrame, text="Exit", command=self.on_closing)
        self.buttonExit.grid(row=3, column=2, sticky="w", padx=(0, 12), pady=12)
        
    def change(self):
        logonDBHandler.initializeDatabase()
        
        print(self.usernameEntry.get(), self.oldPasswordEntry.get(), self.newPasswordEntry.get())
        changePass = logonDBHandler.changePasswordProcess(self.usernameEntry.get(), self.oldPasswordEntry.get(), self.newPasswordEntry.get())
        
        if changePass:
            print("Password Changed")
            return True
            
        else:
            self.usernameEntry.configure(text_color="red")
            self.oldPasswordEntry.configure(text_color="red")
    
    def forgotPassword(self):
        pass
    
    def on_closing(self, event=0):
        self.destroy()
        
if __name__ == "__main__":
    app = changePassword()
    app.mainloop()
