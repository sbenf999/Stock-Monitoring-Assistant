import customtkinter
import tkinter

from processes.windowSuperClass import *

class popUpWindow(superWindow):
    def __init__(self, message, windowName="Popup Message"):
        self.message = message
        self.windowName = windowName

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

    def onClosing(self, event=0):
        self.box.destroy()



