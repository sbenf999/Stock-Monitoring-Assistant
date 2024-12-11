import customtkinter
import os
from logonDBHandler import *

customtkinter.set_default_color_theme("dark-blue")

class Logon(customtkinter.CTk):
    
    APP_NAME = "Login Window"
    WIDTH = 500
    HEIGHT = 200
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(Logon.APP_NAME)
        self.geometry(str(Logon.WIDTH) + "x" + str(Logon.HEIGHT))
        self.minsize(Logon.WIDTH, Logon.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.bind("<Shift-q>", self.onClosing)
        self.bind("<Command-w>", self.onClosing)
        self.createcommand('tk::mac::Quit', self.onClosing)
        self.after(201, lambda :self.iconbitmap('Images/person.ico'))
          
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
        
        self.buttonChangePassword = customtkinter.CTkButton(self.loginFrame, text="Change password", command=self.onClosing)
        self.buttonChangePassword.grid(row=2, column=1, sticky="w", padx=(12, 12), pady=12)
        
        self.buttonExit = customtkinter.CTkButton(self.loginFrame, text="Exit", command=self.onClosing)
        self.buttonExit.grid(row=2, column=2, sticky="w", padx=(0, 12), pady=12)

        #test with admin user
        logon_ = logonDBHandler()
        logon_.initializeDatabase()
        logon_.createUserCreds("admin", 12345, 1)

    def logonProcess(self):
        logon_ = logonDBHandler()
        logon_.initializeDatabase()

        login = logon_.validateUser(self.usernameEntry.get(), self.passwordEntry.get())
        if login:
            print("Hoorah")
            self.newWindow()
        
        else:
            self.usernameEntry.configure(text_color="red")
            self.passwordEntry.configure(text_color="red")
        
    def newWindow(self):
        self.onClosing()
        #Define the new window (this should ideally be your application that needed logging into)
        loginSuccess = customtkinter.CTk()
        loginSuccess.geometry(f"{500}x{500}")
        loginSuccess.title("App")
        
        #Add widgets
        frame_new = customtkinter.CTkFrame(master=loginSuccess,width=450, height=450, corner_radius=10)
        frame_new.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        label_new = customtkinter.CTkLabel(master=frame_new, width=200, height=60, corner_radius=10, fg_color=("gray70", "gray35"), text="You have successfully logged in")
        label_new.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        
        loginSuccess.mainloop()
    
    def onClosing(self, event=0):
        self.destroy()

if __name__ == "__main__":
    app = Logon()
    app.mainloop()