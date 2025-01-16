import customtkinter
from dbHandling.logonDBHandler import *
from processes.changePassword import *
from processes.windowSuperClass import superWindow
from mainApp import *
from time import sleep

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



if __name__ == "__main__":
    user = newUser()
