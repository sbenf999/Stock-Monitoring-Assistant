import customtkinter
from tkinter import ttk
from logonDBHandler import *
from changePassword import *
from login_process import *
from popUpWindow import *
from windowSuperClass import superWindow
from autoCompleteSearch import AutocompleteEntry
from time import gmtime, strftime

class App(superWindow):

    WIDTH = 1100
    HEIGHT = 580

    def __init__(self, userAccessLevel):
        super().__init__()

        self.userAccessLevel = userAccessLevel

        # configure window
        self.title("OneStop Stock Assistant System")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(False, False)

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets and create the logo text
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="OSSMA", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        #create a section of buttons for stock taking tools
        self.label1 = customtkinter.CTkLabel(self.sidebar_frame, text="Stock taking tools:", font=customtkinter.CTkFont(size=12))
        self.label1.grid(row=1, column=0, padx=20)
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Record a delivery"), text="Record a delivery")
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Stock counting"), text="Stock counting")
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Data view"), text="Data view")
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)

        #create a section of buttons for database tools, such as adding a product or supplier
        seperator1 = customtkinter.CTkFrame(self.sidebar_frame, height=1, width=100,fg_color="gray")
        seperator1.grid(row=5, column=0, padx=20, pady=10)
        self.label2 = customtkinter.CTkLabel(self.sidebar_frame, text="Database tools:", font=customtkinter.CTkFont(size=12))
        self.label2.grid(row=6, column=0, padx=20)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Add product"), text="Add product")
        self.sidebar_button_3.grid(row=7, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Add supplier"), text="Add supplier")
        self.sidebar_button_4.grid(row=8, column=0, padx=20, pady=10)

        #create a section of buttons for tools that present data in graph format etc
        seperator2 = customtkinter.CTkFrame(self.sidebar_frame, height=1, width=100,fg_color="gray")
        seperator2.grid(row=9, column=0, padx=20, pady=10)
        self.label3 = customtkinter.CTkLabel(self.sidebar_frame, text="Data tools:", font=customtkinter.CTkFont(size=12))
        self.label3.grid(row=10, column=0, padx=20)
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Weekly report"), text="Weekly report")
        self.sidebar_button_5.grid(row=11, column=0, padx=20, pady=10)
        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Profit margins"), text="Profit margins")
        self.sidebar_button_6.grid(row=12, column=0, padx=20, pady=10)
        self.sidebar_button_7 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Settings"), text="Settings")
        self.sidebar_button_7.grid(row=13, column=0, padx=20, pady=(10,20))

        #tabview in which all UI will take place to do with functions of the application - the sidebar on the side simply allows for easier switching of the tabs
        self.setButtonStates() #set the button states (disabled or enabled) based on the user access
        
        self.tabview = customtkinter.CTkTabview(master=self)
        self.tabview.grid(column=1, row=0)
        for tab in self.allowances[int(self.userAccessLevel)]:
            self.tabview.add(tab)

        #<========================UI-SETTERS========================>
        #STOCK TAKING TOOLS
        self.recordDeliveryUI()

    #function for buttons in the sidebar - used for navigating the tabview on the right
    def goToTab(self, tabName):
        self.tabview.set(tabName)

    def setButtonStates(self):
        #get user access level from login program in order to disable some functions
        self.tabsDefault = ["Home", "Record a delivery", "Stock counting", "Data view", "Add product", "Add supplier", "Weekly report", "Profit margins", "Settings"]
        self.buttonsDefault = [self.sidebar_button_1, self.sidebar_button_2, self.sidebar_button_3, self.sidebar_button_4, self.sidebar_button_5, self.sidebar_button_6, self.sidebar_button_7]
        self.tabs = self.tabsDefault
        self.allowances: dict = {
                1: self.tabsDefault,
                2: list(filter(lambda tab_: tab_ not in ["Profit margins"], self.tabs)),
                3: list(filter(lambda tab_: tab_ not in ["Profit margins", "Add product", "Add supplier", "Data view", "Weekly report", "Settings"], self.tabs))
        }

        #disable any buttons that the user doesnt have access to
        for page in self.tabsDefault:
            if page not in self.allowances[int(self.userAccessLevel)]:
                for button in self.buttonsDefault:
                    name = button.cget("text")
                    if name == page:
                        button.configure(state="disabled")

    def recordDeliveryUI(self, tab_='Record a delivery'): #you might want to make this a scrollable fram
        #you need to create a supplier database and then select all suppliers in order to be able to give values for the value list below
        self.chooseSupplierLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Choose supplier:", anchor="w")
        self.chooseSupplierLabel.grid(row=0, column=0, padx=(20, 20), pady=20, sticky='w')
        self.chooseSupplier = customtkinter.CTkOptionMenu(self.tabview.tab(tab_), dynamic_resizing=False, values=["Value 1", "Value 2", "Value Long Long Long"], width=200) #values list should be taken from a database call once the supplier database is created
        self.chooseSupplier.grid(row=0, column=1, padx=20, pady=20)

        #delivery date shoud create an ovveride feature if user doesnt want to use current system date
        self.enterDeliveryDateLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Delivery date:", anchor='w')
        self.enterDeliveryDateLabel.grid(row=1, column=0, padx=(20, 20), pady=20, sticky='w')
        self.deliveryDate = strftime("%d/%m/%y", gmtime())
        self.enterDeliveryDateLabelAbs = customtkinter.CTkLabel(self.tabview.tab(tab_), text=self.deliveryDate)
        self.enterDeliveryDateLabelAbs.grid(row=1, column=1, padx=(20, 20), pady=20, sticky='w')

        self.enterDeliveryDateLabelOverride = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Override: ")
        self.enterDeliveryDateLabelOverride.grid(row=2, column=0, padx=(20, 20), pady=20, sticky='w')
        self.enterDeliveryDateEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="xx/xx/xx...")
        self.enterDeliveryDateEntry.grid(row=2, column=1, padx=(20, 20), pady=20, sticky='w')

        #delivery time shoud create an ovveride feature if user doesnt want to use current system time
        self.enterDeliveryTimeLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Delivery time:")
        self.enterDeliveryTimeLabel.grid(row=1, column=2, padx=(20, 20), pady=20, sticky='w')
        self.deliveryTime = strftime("%X", gmtime())
        self.enterDeliveryTimeLabelAbs = customtkinter.CTkLabel(self.tabview.tab(tab_), text=self.deliveryTime)
        self.enterDeliveryTimeLabelAbs.grid(row=1, column=3, padx=(20, 20), pady=20, sticky='w')

        self.enterDeliveryTimeLabelOverride = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Override: ")
        self.enterDeliveryTimeLabelOverride.grid(row=2, column=2, padx=(20, 20), pady=20, sticky='w')
        self.enterDeliveryTimeEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="xx:xx:xx...")
        self.enterDeliveryTimeEntry.grid(row=2, column=3, padx=(20, 20), pady=20, sticky='w')

        #create a seperator to distuinguish between sections
        seperator = customtkinter.CTkFrame(self.tabview.tab(tab_), height=1, fg_color="gray")
        seperator.grid(row=3, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        #create the autocomplete search for a product
        self.findProductLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Search product:")
        self.findProductLabel.grid(row=4, column=0, padx=(20), pady=20, sticky='w')
        autocomplete_entry = AutocompleteEntry(self.tabview.tab(tab_), width=500, placeholder_text="search product...")
        autocomplete_entry.set_suggestions(["Banana", "Bagels"])
        autocomplete_entry.grid(row=4, column=1, padx=20, pady=20, columnspan=3, sticky='w')

if __name__ == "__main__":
    #login = Logon()
    #login.mainloop()
    app = App(1)
    app.mainloop()
