import customtkinter
from tkinter import ttk
import tkinter as tk
from logonDBHandler import *
from changePassword import *
from login_process import *
from popUpWindow import *
from windowSuperClass import superWindow
from autoCompleteSearch import AutocompleteEntry
from time import gmtime, strftime
from scrollingWindow import scrollableWin
from tkinter import messagebox

class App(superWindow):

    WIDTH = 1100
    HEIGHT = 775

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
        

        #create a section of buttons for database tools, such as adding a product or supplier
        seperator1 = customtkinter.CTkFrame(self.sidebar_frame, height=0, width=100,fg_color="gray")
        #seperator1.grid(row=4, column=0, padx=20, pady=10)
        self.label2 = customtkinter.CTkLabel(self.sidebar_frame, text="Database tools:", font=customtkinter.CTkFont(size=12))
        self.label2.grid(row=5, column=0, padx=20)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Data view"), text="Data view")
        self.sidebar_button_3.grid(row=6, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Add product"), text="Add product")
        self.sidebar_button_4.grid(row=7, column=0, padx=20, pady=10)
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Add supplier"), text="Add supplier")
        self.sidebar_button_5.grid(row=8, column=0, padx=20, pady=10)

        #create a section of buttons for tools that present data in graph format etc
        seperator2 = customtkinter.CTkFrame(self.sidebar_frame, height=1, width=100,fg_color="gray")
        seperator2.grid(row=9, column=0, padx=20, pady=10)
        self.label3 = customtkinter.CTkLabel(self.sidebar_frame, text="Data tools:", font=customtkinter.CTkFont(size=12))
        self.label3.grid(row=10, column=0, padx=20)
        self.sidebar_button_6 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Weekly report"), text="Weekly report")
        self.sidebar_button_6.grid(row=11, column=0, padx=20, pady=10)
        self.sidebar_button_7 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Profit margins"), text="Profit margins")
        self.sidebar_button_7.grid(row=12, column=0, padx=20, pady=10)
        self.sidebar_button_8 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Settings"), text="Settings")
        self.sidebar_button_8.grid(row=13, column=0, padx=20, pady=(10,20))

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
        self.buttonsDefault = [self.sidebar_button_1, self.sidebar_button_2, self.sidebar_button_3, self.sidebar_button_4, self.sidebar_button_5, self.sidebar_button_6, self.sidebar_button_7, self.sidebar_button_8]
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
        self.tab_ = tab_
        
        self.chooseSupplierLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Choose supplier:", anchor="w")
        self.chooseSupplierLabel.grid(row=0, column=0, padx=(20, 20), pady=20, sticky='w')
        self.chooseSupplier = customtkinter.CTkOptionMenu(self.tabview.tab(tab_), dynamic_resizing=False, values=["Value 1", "Value 2", "Value Long Long Long"], width=200) #values list should be taken from a database call once the supplier database is created
        self.chooseSupplier.grid(row=0, column=1, padx=20, pady=20)

        #delivery date shoud create an ovveride feature if user doesnt want t   o use current system date
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
        self.autocomplete_entry = AutocompleteEntry(self.tabview.tab(tab_), width=500, placeholder_text='Search product...')
        self.autocomplete_entry.set_suggestions(["Banana", "Bagels"])
        self.autocomplete_entry.grid(row=4, column=1, padx=20, pady=20, columnspan=3, sticky='w')
        self.quantityLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Quantity: ")
        self.quantityLabel.grid(row=5, column=0, padx=(20, 20), pady=10, sticky='w')
        self.quantityEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="x")
        self.quantityEntry.grid(row=5, column=1, padx=(20, 20), pady=10, sticky='w')
        self.addProduct = customtkinter.CTkButton(self.tabview.tab(tab_), text="Add product", command=self.add_product)
        self.addProduct.grid(row=5, column=2, padx=20, pady=10)

        #create a seperator to distuinguish between sections
        seperator2 = customtkinter.CTkFrame(self.tabview.tab(tab_), height=1, fg_color="gray")
        seperator2.grid(row=6, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        #scrollable frame for added products
        self.products = []

        self.productFrame = scrollableWin(master=self.tabview.tab(tab_), width=300, height=200, corner_radius=0, fg_color="transparent")
        self.productFrame.grid(row=7, column=0, sticky="nsew", columnspan=6)
        self.productNumLabel = customtkinter.CTkLabel(self.productFrame, text="Item num", fg_color="transparent")
        self.productNumLabel.grid(row=0, column=0, padx=(20), pady=20, sticky='w')
        self.itemLabel = customtkinter.CTkLabel(self.productFrame, text="Item", fg_color="transparent")
        self.itemLabel.grid(row=0, column=1, padx=(20), pady=20, sticky='w')
        self.itemQuantityLabel = customtkinter.CTkLabel(self.productFrame, text="Quantity", fg_color="transparent")
        self.itemQuantityLabel.grid(row=0, column=2, padx=(20), pady=20, sticky='w')
        self.toolLabel = customtkinter.CTkLabel(self.productFrame, text="Tool")
        self.toolLabel.grid(row=0, column=3, padx=(20), pady=20, sticky='w')
        
        #create a seperator to distuinguish between sections
        seperator3 = customtkinter.CTkFrame(self.tabview.tab(tab_), height=1, fg_color="gray")
        seperator3.grid(row=8, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        self.confirmDelivery = customtkinter.CTkButton(self.tabview.tab(tab_), text="Confirm delivery", command=self.confirmDelivery)
        self.confirmDelivery.grid(row=9, column=0, padx=20, pady=10)
    
    # Function to add product
    def add_product(self):
        product_name = self.autocomplete_entry.get()
        product_quantity = self.quantityEntry.get()
        
        # Check if product name and quantity are not empty
        if product_name and product_quantity.isdigit():
            quantity = int(product_quantity)
            self.products.append({"name": product_name, "quantity": quantity})
            
            # Update the display
            self.update_product_list()
            
            # Clear entry fields after adding
            self.autocomplete_entry.delete(0, customtkinter.END)
            self.quantityEntry.delete(0, customtkinter.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid product name and quantity")

    # Function to update the product list
    def update_product_list(self):
        # Create a label and entry widget for each product in the list
        self.clearProductList()

        for i, product in enumerate(self.products):
            if i==0:
                self.clearProductList()
            count_label = customtkinter.CTkLabel(self.productFrame, text=str(i+1))
            count_label.grid(row=i+2, column=0, padx=20, sticky="w", pady=10)

            # Name label with fixed width
            name_label = customtkinter.CTkLabel(self.productFrame, text=product['name'])
            name_label.grid(row=i+2, column=1, padx=20, sticky="w", pady=10)

            # Quantity entry with fixed width
            quantity_entry_widget = customtkinter.CTkEntry(self.productFrame)
            quantity_entry_widget.grid(row=i+2, column=2, padx=20, sticky="w", pady=10)
            quantity_entry_widget.insert(0, str(product['quantity']))  # Insert the current quantity

            # Delete button to remove the product
            print(self.products, i)
            print(self.products[i])
            delete_button = customtkinter.CTkButton(self.productFrame, text="Delete", command=lambda i=i: self.delete_product(i))
            delete_button.grid(row=i+2, column=3, padx=20, sticky="w", pady=10)

    # Function to delete a product
    def delete_product(self, index):
        # Remove product from the list
        del self.products[index]
        self.update_product_list()

    def clearProductList(self):
        # Clear the existing list
        for widget in self.productFrame.winfo_children():
            if widget not in [self.productNumLabel, self.itemLabel, self.itemQuantityLabel, self.toolLabel]:
                widget.destroy()

    def confirmDelivery(self):
        messagebox.askquestion(title='Confirm delivery', message="Do you wish to confirm the delivery?")
        for widget in self.tabview.tab(self.tab_).winfo_children():
            try:
                if widget.cget('placeholder_text'):
                    widget.delete(0, customtkinter.END)
                    widget._activate_placeholder()
                    widget.focus()
            
            except ValueError:
                continue

        self.clearProductList()



if __name__ == "__main__":
    #login = Logon()
    #login.mainloop()
    app = App(1)
    app.mainloop()
