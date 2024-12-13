import customtkinter
from logonDBHandler import *

customtkinter.set_default_color_theme("dark-blue")

class forgotPassword(customtkinter.CTk):
    
    APP_NAME = "Forgot Password"
    WIDTH = 500
    HEIGHT = 250
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(forgotPassword.APP_NAME)
        self.geometry(str(forgotPassword.WIDTH) + "x" + str(forgotPassword.HEIGHT))
        self.minsize(forgotPassword.WIDTH, forgotPassword.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Shift-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)
        
        #create change password frame
        self.forgotPasswordFrame = customtkinter.CTkFrame(self, corner_radius=10)
        self.forgotPasswordFrame.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        
        self.usernameLabel = customtkinter.CTkLabel(self.forgotPasswordFrame, text="Enter Username:", anchor="w")
        self.usernameLabel.grid(row=0, column=0)
        
        self.usernameEntry = customtkinter.CTkEntry(self.forgotPasswordFrame, placeholder_text="Username...")
        self.usernameEntry.grid(row=0, column=1, columnspan=2, sticky="nsew", padx=(12), pady=12)
        
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
        
        self.buttonExit = customtkinter.CTkButton(self.forgotPasswordFrame, text="Exit", command=self.on_closing)
        self.buttonExit.grid(row=3, column=2, sticky="w", padx=(12, 165), pady=12)
        
    def validateRecoveryPassword(self):
        pass
    
    def on_closing(self, event=0):
        self.destroy()

if __name__ == "__main__":
    test = forgotPassword()
    test.mainloop()