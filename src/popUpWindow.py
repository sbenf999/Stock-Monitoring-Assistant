import customtkinter
import tkinter

class popUpWindow(customtkinter.CTk):
    def __init__(self, message, windowName="Popup Message"):
        self.message = message
        self.windowName = windowName

    def create(self):
        box = customtkinter.CTk()
        box.geometry(f"{200}x{50}")
        box.title(self.windowName)
        
        frame_new = customtkinter.CTkFrame(master=box,width=200, height=50, corner_radius=10)
        frame_new.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        label_new = customtkinter.CTkLabel(master=frame_new, width=200, corner_radius=10, text=self.message)
        label_new.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER) 

        box.mainloop()
        
if __name__ == "__main__":
    box = popUpWindow("Password changed successfuly")
    box.create()


