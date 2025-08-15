import customtkinter
import tkinter
from tkinter import messagebox
import re

from processes.windowSuperClass import *

class popUpWindow(superWindow):
    def __init__(self, message, windowName="Popup Message", buttonText="Dismiss"):
        self.message = message
        self.windowName = windowName
        self.buttonText = buttonText

    def create(self):
        self.box = customtkinter.CTk()
        self.box.geometry(f"{310}x{50}")
        self.box.title(self.windowName)
        
        frame_new = customtkinter.CTkFrame(master=self.box,width=310, height=50, corner_radius=10)
        frame_new.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        label_new = customtkinter.CTkLabel(master=frame_new, width=200, corner_radius=10, text=self.message)
        label_new.grid(row=0, column=0, sticky="w", padx=(0, 12), pady=12) 

        confirmButton = customtkinter.CTkButton(master=frame_new, width=20, corner_radius=10, text="Dismiss", command=self.onClosing)
        confirmButton.grid(row=0, column=1, sticky="w", padx=(0, 12), pady=12) 

        self.box.mainloop()

    def createWithInputDialog(self, regexInputChecking=None, examples=None):
        self.box = customtkinter.CTk()
        self.box.geometry(f"{360}x{120}")
        self.box.title(self.windowName)
        self.regexInputChecking = regexInputChecking
        self.examples = examples
        
        frame_new = customtkinter.CTkFrame(master=self.box,width=360, height=50, corner_radius=10)
        frame_new.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        label_new = customtkinter.CTkLabel(master=frame_new, width=200, corner_radius=10, text=self.message)
        label_new.grid(row=0, column=0, sticky="w", padx=(20, 2), pady=12) 

        self.entry_new = customtkinter.CTkEntry(master=frame_new, width=200, corner_radius=10, placeholder_text="email addr...")
        self.entry_new.grid(row=1, column=0, sticky="w", padx=(20, 20), pady=12) 

        confirmButton = customtkinter.CTkButton(master=frame_new, width=20, corner_radius=10, text=self.buttonText, command=self.getValue)
        confirmButton.grid(row=1, column=1, sticky="w", padx=(0, 12), pady=12) 

    def onClosing(self, event=0):
        self.box.destroy()

    def getValue(self):
        def isValidInput(input):
            pattern = self.regexInputChecking
            return re.match(pattern, input) is not None
        
        if self.entry_new.winfo_exists() and self.entry_new.get():
            #sanitise any inputs
            if self.regexInputChecking and isValidInput(self.entry_new.get()):
                self.data = self.entry_new.get()
                self.entry_new.delete(0, customtkinter.END)
                self.onClosing()

                return self.data
            
            else:
                messagebox.showwarning("Input Error", f"Please enter a valid input conforming to the RegEx: \n{self.regexInputChecking}. \n\n{self.examples}")


        else:
            messagebox.showwarning("Input Error", "Please enter a valid input")





