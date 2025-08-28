import customtkinter
import tkinter
from tkinter import messagebox
import re

from processes.windowSuperClass import *
from processes.pieChart import *
from dbHandling.DBHandler import *

class popUpWindow(superWindow):
    def __init__(self, message=None, windowName="Popup Message", buttonText="Dismiss"):
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

    def createGraph(self, width, height):
        self.box = customtkinter.CTk()
        self.box.geometry(f"{width}x{height}")
        self.box.title(self.windowName)

        graphValHandler = DBHandler()
        
        centeredFrame = customtkinter.CTkFrame(master=self.box,width=width, height=height, corner_radius=10)
        centeredFrame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        pieChart = CTkPieChart(centeredFrame, line_width=50)
        pieChart.grid(row=0, column=0, padx=10, pady=(10, 50), sticky="e")

        try:
            pieChart.add("Products", graphValHandler.getCount("products", False), text_color="black", color="#1F538D")
            pieChart.add("Suppliers", graphValHandler.getCount("suppliers", False), text_color="black", color="gray")
            pieChart.add("Waste", graphValHandler.getCount("waste", False), text_color="black", color="green")
            pieChart.add("Stocklevel", graphValHandler.getCount("stocklevel", False), text_color="black", color="purple")
            pieChart.add("Users", graphValHandler.getCount("users", False), text_color="black", color="yellow")
            pieChart.add("StockLevelHistory", graphValHandler.getCount("stocklevelhistory", False), text_color="black", color="indigo")
            pieChart.add("EventTracking", graphValHandler.getCount("eventTracking", False), text_color="black", color="blue")

        except Exception as error:
            print("Error")
        
        #get the dictionary of key value pairs to create the key for the pie chart
        pieChartValues = pieChart.get()

        #create a frame for the piechart
        pieChartFrame = customtkinter.CTkFrame(centeredFrame, fg_color="transparent")
        pieChartFrame.grid(row=1, column=1, padx=10, pady=10, sticky="e", columnspan=2) 

        #display the values for the key
        for key, values in pieChartValues.items():
            dataCircle = customtkinter.CTkRadioButton(pieChartFrame, hover=False, text=key, width=1,fg_color=values["color"])
            dataCircle.select()
            dataCircle.pack(side='top', anchor='nw', pady=5)

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

    def onClosing(self, event=0):
        self.box.destroy()





