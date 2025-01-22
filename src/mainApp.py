#general lib imports
import customtkinter
from tkinter import messagebox
from time import gmtime, strftime
import json

#import processes
from processes.changePassword import *
from processes.loginProcess import *
from processes.popUpWindow import *
from processes.windowSuperClass import superWindow
from processes.autoCompleteSearch import AutocompleteEntry
from processes.scrollingWindow import scrollableWin
from processes.newUser import *

#import database handlers
from dbHandling.logonDBHandler import *
from dbHandling.productDBHandler import *
from dbHandling.supplierDBHandler import *
from dbHandling.wasteDBHandler import *
from dbHandling.stockLevelDBHandler import *

#main app class
class App(superWindow):

    WIDTH = 1100
    HEIGHT = 775

    def __init__(self, userAccessLevel, userName="user"):
        super().__init__()

        self.userAccessLevel = userAccessLevel
        self.userName = userName

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
        self.sidebar_button_7 = customtkinter.CTkButton(self.sidebar_frame, command=lambda: self.goToTab("Settings"), text="Settings")
        self.sidebar_button_7.grid(row=13, column=0, padx=20, pady=(10,20))

        #========================BUTTON-STATES======================>
        #tabview in which all UI will take place to do with functions of the application - the sidebar on the side simply allows for easier switching of the tabs
        self.setButtonStates() #set the button states (disabled or enabled) based on the user access
        
        #create the tabview according to allowances
        self.tabview = customtkinter.CTkTabview(master=self)
        self.tabview.grid(column=1, row=0)
        for tab in self.allowances[int(self.userAccessLevel)]:
            self.tabview.add(tab)

        #<========================INITIALIZE-DATABASES========================>
        self.DBHandler = DBHandler() 
        self.supplierDB = supplierDBHandler()
        self.productDB = productDBHandler()
        self.wasteDB = wasteDBHandler()  
        self.stockLevelDB = stockLevelDBHandler()

        databases = [self.supplierDB, self.productDB, self.wasteDB, self.stockLevelDB]

        for database in databases:
            try:
                database.initializeDatabase()
                print(f"Database {database} initialised successfully")

            except Exception as error:
                print(error)

        #<========================UI-SETTERS========================>
        self.homeUI()
        self.recordDeliveryUI()
        self.stockCountingUI()
        self.addProductUI()
        self.addSupplierUI()
        self.settingsUI()

    #function for buttons in the sidebar - used for navigating the tabview on the right
    def goToTab(self, tabName):
        self.tabview.set(tabName)

    def setButtonStates(self):
        #get user access level from login program in order to disable some functions
        self.tabsDefault = ["Home", "Record a delivery", "Stock counting", "Data view", "Add product", "Add supplier", "Weekly report", "Settings"]
        self.buttonsDefault = [self.sidebar_button_1, self.sidebar_button_2, self.sidebar_button_3, self.sidebar_button_4, self.sidebar_button_5, self.sidebar_button_6, self.sidebar_button_7]
        self.tabs = self.tabsDefault
        self.allowances: dict = {
                1: self.tabsDefault,
                2: list(filter(lambda tab_: tab_ not in ["Data view", "Weekly report"], self.tabs)),
                3: list(filter(lambda tab_: tab_ not in ["Add product", "Add supplier", "Data view", "Weekly report"], self.tabs))
        }

        #disable any buttons that the user doesnt have access to
        for page in self.tabsDefault:
            if page not in self.allowances[int(self.userAccessLevel)]:
                for button in self.buttonsDefault:
                    name = button.cget("text")
                    if name == page:
                        button.configure(state="disabled")

    #=================================================================================================HOME-UI-AND-FUNCTIONALITY=================================================================================================    
    def homeUI(self, tab_='Home'):
        self.tab_ = tab_

        #Configure the grid to center for the centered welcome text
        self.tabview.tab(tab_).grid_rowconfigure([0, 1, 2], weight=1)
        self.tabview.tab(tab_).grid_columnconfigure([0, 1, 2, 3], weight=1)

        #set the welcome label in the center
        self.welcomeLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text=f"Hi {self.userName}!", font=customtkinter.CTkFont(size=35, weight="bold"), padx=0, pady=0)
        self.welcomeLabel.grid(row=0, column=0, columnspan=4)

        #create product count label and label value
        self.productCountLabelValue = customtkinter.CTkLabel(self.tabview.tab(tab_), text=self.productDB.getCount("products"), font=("Arial", 20))
        self.productCountLabelValue.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        #create supplier count label and label value
        self.supplierCountLabelValue = customtkinter.CTkLabel(self.tabview.tab(tab_), text=self.supplierDB.getCount("suppliers"), font=("Arial", 20))
        self.supplierCountLabelValue.grid(row=1, column=1, padx=10, pady=10, sticky="e", columnspan=2)  

        #self.DBHandler.createBarGraphVisualisation(self.tabview.tab(tab_))

    #=========================================================================================RECORD-DELIVERY-UI-AND-FUNCTIONALITY=================================================================================================    
    def recordDeliveryUI(self, tab_='Record a delivery'): #you might want to make this a scrollable fram
        #you need to create a supplier database and then select all suppliers in order to be able to give values for the value list below
        self.tab_ = tab_
        
        self.chooseSupplierLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Choose supplier:", anchor="w")
        self.chooseSupplierLabel.grid(row=0, column=0, padx=(20, 20), pady=20, sticky='w')

        #if no data in table, CTKOptionMenu throws an error, so try except block creates failure lable if this issue is encountered
        try:
            self.chooseSupplier1 = customtkinter.CTkOptionMenu(self.tabview.tab(tab_), dynamic_resizing=False, values=self.supplierDB.getSupplierNames(), width=200) #values list should be taken from a database call once the supplier database is created
            self.chooseSupplier1.grid(row=0, column=1, padx=20, pady=20)
            
        except Exception as error:
            self.noSupplierLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="No suppliers found", anchor="w")
            self.noSupplierLabel.grid(row=0, column=1, padx=(20, 20), pady=20, sticky='w')

        #delivery date shoud create an ovveride feature if user doesnt want t   o use current system date
        self.enterDeliveryDateLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Delivery date:", anchor='w')
        self.enterDeliveryDateLabel.grid(row=1, column=0, padx=(20, 20), pady=20, sticky='w')
        self.deliveryDate = strftime("%d/%m/%y", gmtime())
        self.enterDeliveryDateLabelAbs = customtkinter.CTkLabel(self.tabview.tab(tab_), text=self.deliveryDate)
        self.enterDeliveryDateLabelAbs.grid(row=1, column=1, padx=(20, 20), pady=20, sticky='w')

        #delivery time shoud create an ovveride feature if user doesnt want to use current system time
        self.enterDeliveryTimeLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Delivery time:")
        self.enterDeliveryTimeLabel.grid(row=1, column=2, padx=(20, 20), pady=20, sticky='w')
        self.deliveryTime = strftime("%X", gmtime())
        self.enterDeliveryTimeLabelAbs = customtkinter.CTkLabel(self.tabview.tab(tab_), text=self.deliveryTime)
        self.enterDeliveryTimeLabelAbs.grid(row=1, column=3, padx=(20, 20), pady=20, sticky='w')

        #create the autocomplete search for a product
        self.findProductLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Search product:")
        self.findProductLabel.grid(row=3, column=0, padx=(20), pady=20, sticky='w')
        self.autocompleteEntry = AutocompleteEntry(self.tabview.tab(tab_), width=500, placeholder_text='Search product...')
        
        self.autocompleteEntry.setSuggestions(self.productDB.getProductNames()) #set suggestions needs to be based on a call to the product table in the database
        self.autocompleteEntry.grid(row=3, column=1, padx=20, pady=20, columnspan=3, sticky='w')
        
        self.quantityLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Quantity: ")
        self.quantityLabel.grid(row=4, column=0, padx=(20, 20), pady=10, sticky='w')
        self.quantityEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="x")
        self.quantityEntry.grid(row=4, column=1, padx=(20, 20), pady=10, sticky='w')
        self.addProduct = customtkinter.CTkButton(self.tabview.tab(tab_), text="Add product", command=self.addProductToDelivery)
        self.addProduct.grid(row=4, column=2, padx=20, pady=10)

        #create a seperator to distuinguish between sections
        seperator2 = customtkinter.CTkFrame(self.tabview.tab(tab_), height=1, fg_color="gray")
        seperator2.grid(row=5, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        #scrollable frame for added products
        self.products = []

        self.productFrame = scrollableWin(master=self.tabview.tab(tab_), width=300, height=200, corner_radius=0, fg_color="transparent")
        self.productFrame.grid(row=6, column=0, sticky="nsew", columnspan=6)
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
        seperator3.grid(row=7, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        self.confirmDelivery = customtkinter.CTkButton(self.tabview.tab(tab_), text="Confirm delivery", command=self.confirmDelivery)
        self.confirmDelivery.grid(row=8, column=0, padx=20, pady=10)
    
    # Function to add product
    def addProductToDelivery(self):
        productName = self.autocompleteEntry.get()
        productQuantity = self.quantityEntry.get()
        
        #Check if product name and quantity are not empty
        if productName and productQuantity.isdigit():
            quantity = int(productQuantity)
            self.products.append([productName, quantity])
            
            #Update the display
            self.updateProductList()
            
            #Clear entry fields after adding
            self.autocompleteEntry.delete(0, customtkinter.END)
            self.quantityEntry.delete(0, customtkinter.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid product name and quantity")

    #Function to update the product list
    def updateProductList(self):
        #Create a label and entry widget for each product in the list
        self.clearProductList()

        for i, product in enumerate(self.products):
            if i==0:
                self.clearProductList()

            countLabel = customtkinter.CTkLabel(self.productFrame, text=str(i+1))
            countLabel.grid(row=i+2, column=0, padx=20, sticky="w", pady=10)

            #Name label with fixed width
            nameLabel = customtkinter.CTkLabel(self.productFrame, text=product[0])
            nameLabel.grid(row=i+2, column=1, padx=20, sticky="w", pady=10)

            #Quantity entry with fixed width
            quantityEntryWidget = customtkinter.CTkEntry(self.productFrame)
            quantityEntryWidget.grid(row=i+2, column=2, padx=20, sticky="w", pady=10)
            quantityEntryWidget.insert(0, str(product[1]))  # Insert the current quantity

            #Delete button to remove the product
            print(self.products, i)
            print(self.products[i])
            deleteButton = customtkinter.CTkButton(self.productFrame, text="Delete", command=lambda i=i: self.deleteProductInDelivery(i))
            deleteButton.grid(row=i+2, column=3, padx=20, sticky="w", pady=10)

    #Function to delete a product
    def deleteProductInDelivery(self, index):
        #Remove product from the list
        del self.products[index]
        self.updateProductList()

    #Function to clear product list
    def clearProductList(self):
        #Clear the existing list
        for widget in self.productFrame.winfo_children():
            if widget not in [self.productNumLabel, self.itemLabel, self.itemQuantityLabel, self.toolLabel]:
                widget.destroy()

    #Function to confirm the delivery
    def confirmDelivery(self):
        if messagebox.askquestion(title='Confirm delivery', message="Do you wish to confirm the delivery?"):
            try:
                #update stock levels and any other data here
                for product in self.products:
                    #update stock level
                    productID = self.productDB.getProductID(product[0])
                    self.stockLevelDB.updateStockLevel(product[1], productID)
                    #update last delivery date for product
                    self.stockLevelDB.updateLastDelivery(f'["{self.deliveryDate}"]', productID) #check json stuff

                #clear widgets once the delivery has been confirmed
                for widget in self.tabview.tab(self.tab_).winfo_children():
                    try:
                        if widget.cget('placeholder_text'):
                            widget.delete(0, customtkinter.END)
                            widget._activate_placeholder()
                            widget.focus()
                    
                    except ValueError:
                        continue

                self.clearProductList()

            except Exception as error:
                print(f"error encountered on delivery confirmation: {error}")
                return False

        else:
            pass

    #=================================================================================================STOCK-COUNT-UI-AND-FUNCTIONALITY=================================================================================================
    def stockCountingUI(self, tab_='Stock counting'): 
        self.tab_ = tab_

        #create the autocomplete search for a product
        self.findStockCountProductLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Search product:")
        self.findStockCountProductLabel.grid(row=0, column=0, padx=(20), pady=20, sticky='w')
        self.stockCountAutocompleteEntry = AutocompleteEntry(self.tabview.tab(tab_), width=500, placeholder_text='Search product...')
        
        self.stockCountAutocompleteEntry.setSuggestions(self.productDB.getProductNames()) #set suggestions needs to be based on a call to the product table in the database
        self.stockCountAutocompleteEntry.grid(row=0, column=1, padx=20, pady=20, columnspan=3, sticky='w')
        
        self.stockCountQuantityLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Quantity: ")
        self.stockCountQuantityLabel.grid(row=1, column=0, padx=(20, 20), pady=10, sticky='w')
        self.stockCountQuantityEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="x")
        self.stockCountQuantityEntry.grid(row=1, column=1, padx=(20, 20), pady=10, sticky='w')
        self.addProduct = customtkinter.CTkButton(self.tabview.tab(tab_), text="Add product", command=self.addStockCountProductToDelivery)
        self.addProduct.grid(row=1, column=2, padx=20, pady=10)

        #scrollable frame for added products
        self.stockCountProducts = []

        self.stockCountProductFrame = scrollableWin(master=self.tabview.tab(tab_), width=300, height=200, corner_radius=0, fg_color="transparent")
        self.stockCountProductFrame.grid(row=2, column=0, sticky="nsew", columnspan=6)
        self.stockCountProductNumLabel = customtkinter.CTkLabel(self.stockCountProductFrame, text="Item num", fg_color="transparent")
        self.stockCountProductNumLabel.grid(row=0, column=0, padx=(20), pady=20, sticky='w')
        self.stockCountitemLabel = customtkinter.CTkLabel(self.stockCountProductFrame, text="Item", fg_color="transparent")
        self.stockCountitemLabel.grid(row=0, column=1, padx=(20), pady=20, sticky='w')
        self.stockCountitemQuantityLabel = customtkinter.CTkLabel(self.stockCountProductFrame, text="Quantity", fg_color="transparent")
        self.stockCountitemQuantityLabel.grid(row=0, column=2, padx=(20), pady=20, sticky='w')
        self.stockCounttoolLabel = customtkinter.CTkLabel(self.stockCountProductFrame, text="Tool")
        self.stockCounttoolLabel.grid(row=0, column=3, padx=(20), pady=20, sticky='w')
        
        #create a seperator to distuinguish between sections
        stockCountseperator = customtkinter.CTkFrame(self.tabview.tab(tab_), height=1, fg_color="gray")
        stockCountseperator.grid(row=7, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        self.confirmStockCountButton = customtkinter.CTkButton(self.tabview.tab(tab_), text="Confirm stock count", command=self.confirmStockCount)
        self.confirmStockCountButton.grid(row=8, column=0, padx=20, pady=10)

    def addStockCountProductToDelivery(self):
        productName = self.stockCountAutocompleteEntry.get()
        productQuantity = self.stockCountQuantityEntry.get()
        
        #Check if product name and quantity are not empty
        if productName and productQuantity.isdigit():
            quantity = int(productQuantity)
            self.stockCountProducts.append([productName, quantity])
            
            #Update the display
            self.updateStockCountList()
            
            #Clear entry fields after adding
            self.stockCountAutocompleteEntry.delete(0, customtkinter.END)
            self.stockCountQuantityEntry.delete(0, customtkinter.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid product name and quantity")

    #Function to update the product list
    def updateStockCountList(self):
        #Create a label and entry widget for each product in the list
        self.clearStockCountList()

        for i, stockCountProduct in enumerate(self.stockCountProducts):
            if i==0:
                self.clearStockCountList()

            stockCountLabel = customtkinter.CTkLabel(self.stockCountProductFrame, text=str(i+1))
            stockCountLabel.grid(row=i+2, column=0, padx=20, sticky="w", pady=10)

            #Name label with fixed width
            nameLabel = customtkinter.CTkLabel(self.stockCountProductFrame, text=stockCountProduct[0])
            nameLabel.grid(row=i+2, column=1, padx=20, sticky="w", pady=10)

            #Quantity entry with fixed width
            quantityEntryWidget = customtkinter.CTkEntry(self.stockCountProductFrame)
            quantityEntryWidget.grid(row=i+2, column=2, padx=20, sticky="w", pady=10)
            quantityEntryWidget.insert(0, str(stockCountProduct[1]))  # Insert the current quantity

            #Delete button to remove the product
            print(self.stockCountProducts, i)
            print(self.stockCountProducts[i])
            deleteButton = customtkinter.CTkButton(self.stockCountProductFrame, text="Delete", command=lambda i=i: self.deleteProductInStockCountList(i))
            deleteButton.grid(row=i+2, column=3, padx=20, sticky="w", pady=10)

    #Function to delete a product
    def deleteProductInStockCountList(self, index):
        #Remove product from the list
        del self.stockCountProducts[index]
        self.updateStockCountList()

    #Function to clear product list
    def clearStockCountList(self):
        #Clear the existing list
        for widget in self.stockCountProductFrame.winfo_children():
            if widget not in [self.stockCountProductNumLabel, self.stockCountitemLabel, self.stockCountitemQuantityLabel, self.stockCounttoolLabel]:
                widget.destroy()


    def confirmStockCount(self):
        pass

    #=================================================================================================ADD-PRODUCT-UI-AND-FUNCTIONALITY=================================================================================================    
    def addProductUI(self, tab_='Add product'): 
        #you need to create a product database and then select all products in order to be able to give values for the value list below
        self.tab_ = tab_

        self.chooseSupplierLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Choose supplier:", anchor="w")
        self.chooseSupplierLabel.grid(row=0, column=0, padx=(20, 20), pady=20, sticky='w')
        
        #if no data in table, CTKOptionMenu throws an error, so try except block creates failure lable if this issue is encountered
        try:
            self.chooseSupplier2 = customtkinter.CTkOptionMenu(self.tabview.tab(tab_), dynamic_resizing=False, values=self.supplierDB.getSupplierNames(), width=200) #values list should be taken from a database call once the supplier database is created
            self.chooseSupplier2.grid(row=0, column=1, padx=20, pady=20)
            
        except Exception as error:
            print(error)
            self.noSupplierLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="No suppliers found", anchor="w")
            self.noSupplierLabel.grid(row=0, column=1, padx=(20, 20), pady=20, sticky='w')

        #create entry widgets and their respective labels for data input
        self.productNameLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Product name: ")
        self.productNameLabel.grid(row=1, column=0, padx=(20, 20), pady=20, sticky='w')
        self.productNameEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="product name...")
        self.productNameEntry.grid(row=1, column=1, padx=(20, 20), pady=20, sticky='w')

        self.productPriceEntryLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Product price: ")
        self.productPriceEntryLabel.grid(row=1, column=2, padx=(20, 20), pady=20, sticky='w')
        self.productPriceEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="price...")
        self.productPriceEntry.grid(row=1, column=3, padx=(20, 20), pady=20, sticky='w')

        self.productPSLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Product pack size: ")
        self.productPSLabel.grid(row=2, column=0, padx=(20, 20), pady=20, sticky='w')
        self.productPSEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="pack size...")
        self.productPSEntry.grid(row=2, column=1, padx=(20, 20), pady=20, sticky='w')

        self.productWeightLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Product weight: ")
        self.productWeightLabel.grid(row=2, column=2, padx=(20, 20), pady=20, sticky='w')
        self.productWeightEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="weight...")
        self.productWeightEntry.grid(row=2, column=3, padx=(20, 20), pady=20, sticky='w')

        self.minimumStockLevelLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Min stock level: ")
        self.minimumStockLevelLabel.grid(row=3, column=0, padx=(20, 20), pady=20, sticky='w')
        self.minimumStockLevelEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="min stock level...")
        self.minimumStockLevelEntry.grid(row=3, column=1, padx=(20, 20), pady=20, sticky='w')

        self.reorderStockLevelLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Re-order level: ")
        self.reorderStockLevelLabel.grid(row=3, column=2, padx=(20, 20), pady=20, sticky='w')
        self.reorderStockLevelEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="re-order level...")
        self.reorderStockLevelEntry.grid(row=3, column=3, padx=(20, 20), pady=20, sticky='w')

        self.productDescriptionLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Product description: ")
        self.productDescriptionLabel.grid(row=4, column=0, padx=(20, 20), pady=20, sticky='w')
        self.productDescriptionEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), width=518, placeholder_text="product description...")
        self.productDescriptionEntry.grid(row=4, column=1, padx=(20, 20), pady=20, sticky='w', columnspan=5)

        self.confirmAddProduct = customtkinter.CTkButton(self.tabview.tab(tab_), text="Confirm add product", command=self.confirmAddproductProcess)
        self.confirmAddProduct.grid(row=5, column=0, padx=20, pady=20)

    #Creates the new product and clears all entry widgets
    def confirmAddproductProcess(self):
        try:
            if messagebox.askquestion(title='Confirm add product', message="Do you wish to confirm this new product?"):
                #create the new product - supplier_id needs to be found first#
                supplierID = self.supplierDB.getSupplierID(self.chooseSupplier2.get())
                self.productDB.createProduct(supplierID[0], self.productNameEntry.get(), self.productDescriptionEntry.get(), self.productPSEntry.get(), self.productWeightEntry.get(), self.productPriceEntry.get())
                stockLevelProductID = self.productDB.getProductID(self.productNameEntry.get())
                self.stockLevelDB.addStockLevelData(stockLevelProductID, self.minimumStockLevelEntry.get(), self.reorderStockLevelEntry.get())
                self.autocompleteEntry.setSuggestions(self.productDB.getProductNames())

                for widget in [self.productNameEntry, self.productPriceEntry, self.productPSEntry, self.productWeightEntry, self.minimumStockLevelEntry, self.reorderStockLevelEntry, self.productDescriptionEntry]:
                    try:
                        widget.delete(0, customtkinter.END)
                        widget._activate_placeholder()
                        widget.focus()
                    
                    #this handles the event that an entry widget doesnt register the placeholder text, such as an auto_complete entry
                    except Exception as error:
                        print(f"e: {error}")
                        continue

                #resume with app if "no" option is selected
                else:
                    pass
    
        except Exception as error:
            print(error)
            messagebox.showerror("Error", f"An error occurred! Please try again. If this issue persits, please contact the maintainer. Error {error}")

    #Limits entry widget to 200 characters by default
    def limit_entry(self, limit=200, *args):
        current_text = self.limiter.get()
        
        if len(current_text) > limit:
            self.limiter.set(current_text[:limit])

    #=================================================================================================ADD-SUPPLIER-UI-AND-FUNCTIONALITY=================================================================================================    
    def addSupplierUI(self, tab_='Add supplier'): 
        self.tab_ = tab_

        self.chooseSupplierLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Supplier name:", anchor="w")
        self.chooseSupplierLabel.grid(row=0, column=0, padx=(20, 20), pady=20, sticky='w')

        self.suppliertNameEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="supplier name...")
        self.suppliertNameEntry.grid(row=0, column=1, padx=(20, 20), pady=20, sticky='w')

        self.supplierDescriptionLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Supplier description: ")
        self.supplierDescriptionLabel.grid(row=2, column=0, padx=(20, 20), pady=20, sticky='w')
        self.supplierDescriptionEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), width=500, placeholder_text="supplier description...")
        self.supplierDescriptionEntry.grid(row=2, column=1, padx=(20, 20), pady=20, sticky='w', columnspan=5)

        #you need supplier dates here, consider storing this as a list in a JSON format

        self.supplierDates = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Supplier date: ")
        self.supplierDates.grid(row=3, column=0, padx=(20, 20), pady=10, sticky='w')
        self.supplierDatesEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="xx/xx/xx")
        self.supplierDatesEntry.grid(row=3, column=1, padx=(20, 20), pady=10, sticky='w')
        self.addSupplierDate = customtkinter.CTkButton(self.tabview.tab(tab_), text="Add supplier delivery date", command=self.addSupplierDeliveryDate)
        self.addSupplierDate.grid(row=3, column=2, padx=20, pady=10)

        #create a seperator to distuinguish between sections
        seperator = customtkinter.CTkFrame(self.tabview.tab(tab_), height=1, fg_color="gray")
        seperator.grid(row=4, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        #scrollable frame for added supplier dates
        self.supplierDates = []

        self.supplierDateFrame = scrollableWin(master=self.tabview.tab(tab_), width=300, height=200, corner_radius=0, fg_color="transparent")
        self.supplierDateFrame.grid(row=5, column=0, sticky="nsew", columnspan=6)
        self.supplierDateNumLabel = customtkinter.CTkLabel(self.supplierDateFrame, text="Date num", fg_color="transparent")
        self.supplierDateNumLabel.grid(row=0, column=0, padx=(20), pady=20, sticky='w')
        self.dateLabel = customtkinter.CTkLabel(self.supplierDateFrame, text="Item", fg_color="transparent")
        self.dateLabel.grid(row=0, column=1, padx=(20), pady=20, sticky='w')
        self.toolLabel = customtkinter.CTkLabel(self.supplierDateFrame, text="Tool")
        self.toolLabel.grid(row=0, column=3, padx=(20), pady=20, sticky='w')
        
        #create a seperator to distuinguish between sections
        seperator2 = customtkinter.CTkFrame(self.tabview.tab(tab_), height=1, fg_color="gray")
        seperator2.grid(row=6, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        self.confirmAddSupplier = customtkinter.CTkButton(self.tabview.tab(tab_), text="Confirm add supplier", command=self.confirmAddSupplierProcess)
        self.confirmAddSupplier.grid(row=7, column=0, padx=20, pady=20)

    #Creates the new supplier and clears all entry widgets
    def confirmAddSupplierProcess(self):
        try:
            if messagebox.askquestion(title='Confirm add supplier', message="Do you wish to confirm this new supplier?"):
                #create the new supplier
                self.supplierDB.createSupplier(self.suppliertNameEntry.get(), self.supplierDescriptionEntry.get(), json.dumps(self.supplierDates))
                
                #reset widgets
                for widget in self.tabview.tab(self.tab_).winfo_children():
                    try:
                        if widget.cget('placeholder_text'):
                            widget.delete(0, customtkinter.END)
                            widget._activate_placeholder()
                            widget.focus()
                    
                    #this handles the event that an entry widget doesnt register the placeholder text, such as an auto_complete entry
                    except ValueError:
                        continue
                
                #update supplier option menus
                self.chooseSupplier1.configure(values=self.supplierDB.getSupplierNames())
                self.chooseSupplier2.configure(values=self.supplierDB.getSupplierNames())

                #delete supplier delivery date fields upon successful supplier creation
                self.supplierDates = []
                self.updateSupplierDeliveryDateList()

            #resume with app if "no" option is selected
            else:
                pass

        except Exception as error:
            print(error)
            messagebox.showerror("Error", f"An error occurred! Please try again. If this issue persits, please contact the maintainer. Error {error}")

    def addSupplierDeliveryDate(self):
        deliveryDate = self.supplierDatesEntry.get()
        
        # Check supplier date are not empty
        if deliveryDate:
            self.supplierDates.append(deliveryDate)
            self.updateSupplierDeliveryDateList()
            self.supplierDatesEntry.delete(0, customtkinter.END)
        
        else:
            messagebox.showwarning("Input Error", "Please enter a valid delivery date")

    def updateSupplierDeliveryDateList(self):
        # Create widgets for each supplier date
        self.clearSupplierDeliveryDateList()

        for i, supplierDate in enumerate(self.supplierDates):
            if i==0:
                self.clearSupplierDeliveryDateList()

            count_label = customtkinter.CTkLabel(self.supplierDateFrame, text=str(i+1))
            count_label.grid(row=i+2, column=0, padx=20, sticky="w", pady=10)

            #Name label with fixed width
            name_label = customtkinter.CTkLabel(self.supplierDateFrame, text=supplierDate)
            name_label.grid(row=i+2, column=1, padx=20, sticky="w", pady=10)

            #Delete button to remove the supplier date
            print(self.supplierDates, i)
            print(self.supplierDates[i])
            delete_button = customtkinter.CTkButton(self.supplierDateFrame, text="Delete", command=lambda i=i: self.deleteSupplierDate(i))
            delete_button.grid(row=i+2, column=3, padx=20, sticky="w", pady=10)

    def clearSupplierDeliveryDateList(self):
        # Clear the existing list
        for widget in self.supplierDateFrame.winfo_children():
            if widget not in [self.supplierDateNumLabel, self.dateLabel, self.toolLabel]:
                widget.destroy()

    def deleteSupplierDate(self, index):
        # Remove supplier date from the list
        del self.supplierDates[index]
        self.updateSupplierDeliveryDateList()

    #=================================================================================================SETTINGS-UI-AND-FUNCTIONALITY=================================================================================================    
    def settingsUI(self, tab_='Settings'):
        self.tab_ = tab_

        #user tools
        self.userToolsLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="User tools:")
        self.userToolsLabel.grid(row=0, column=0, padx=(20, 20), pady=20, sticky='w')
        self.addUserButton = customtkinter.CTkButton(self.tabview.tab(tab_), text="Create new user", command=self.addNewUser)
        self.addUserButton.grid(row=1, column=0, padx=20, pady=20)

        #configure settings button states
        if int(self.userAccessLevel) != 1:
            for settingsButton in [self.addUserButton, self.editUserButton]:
                settingsButton.configure(state="disabled")

    def addNewUser(self):
        user = newUser()
        user.mainloop()

if __name__ == "__main__":
    initialiser = logonDBHandler()
    initialiser.initializeDatabase()
    #login = Logon()
    #login.mainloop()
    app = App(1)
    app.mainloop()
