#Author: Soma Benfell
#Version number: v1.0.0

#general lib imports
import customtkinter
from tkinter import messagebox
from time import gmtime, strftime
from datetime import timedelta
import json
import dotenv
from functools import reduce
import threading
from CTkTable import *
import os
from os import path
import sys 
import shutil
from datetime import *

#import processes
from processes.changePassword import *
from processes.loginProcess import *
from processes.popUpWindow import *
from processes.windowSuperClass import superWindow
from processes.autoCompleteSearch import AutocompleteEntry
from processes.newUser import *
from processes.stockLevelChecker import *

#not programmed by me
from processes.pieChart import *
from processes.doubleAxesScrollingFrame import *
from processes.CTkDatePicker import *

#import database handlers
from dbHandling.logonDBHandler import *
from dbHandling.productDBHandler import *
from dbHandling.supplierDBHandler import *
from dbHandling.wasteDBHandler import *
from dbHandling.stockLevelDBHandler import *
from dbHandling.stockLevelHistoryDBHandler import *
from dbHandling.weeklyReportDBHandler import *

#main app class
class App(superWindow):

    WIDTH = 1100
    HEIGHT = 675
    _appLocation = os.path.dirname(os.path.abspath(sys.argv[0]))
    _defAlertEmail = os.getenv('DEF_ALERT_RECIPIENT_EMAIL')

    def __init__(self, userAccessLevel, userName="user"):
        super().__init__()

        self.userAccessLevel = userAccessLevel
        self.userName = userName

        #configure window
        self.title("OneStop Stock Assistant System")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(True, False)

        #configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        #create sidebar frame with widgets and create the logo text
        self.sidebarFrame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebarFrame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebarFrame.grid_rowconfigure(4, weight=1)
        self.logoLabel = customtkinter.CTkLabel(self.sidebarFrame, text="OSSMA", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logoLabel.grid(row=0, column=0, padx=20, pady=(20, 10))

        #create a section of buttons for stock taking tools
        self.label1 = customtkinter.CTkLabel(self.sidebarFrame, text="Stock taking tools:", font=customtkinter.CTkFont(size=12))
        self.label1.grid(row=1, column=0, padx=20)
        self.sideBarButton1 = customtkinter.CTkButton(self.sidebarFrame, command=lambda: self.goToTab("Record a delivery"), text="Record a delivery")
        self.sideBarButton1.grid(row=2, column=0, padx=20, pady=10)
        self.sideBarButton2 = customtkinter.CTkButton(self.sidebarFrame, command=lambda: self.goToTab("Stock counting"), text="Stock counting")
        self.sideBarButton2.grid(row=3, column=0, padx=20, pady=10)

        #exit button
        self.sidebarExitButton = customtkinter.CTkButton(self.sidebarFrame, command=self.onClosing, text="Exit")
        self.sidebarExitButton.grid(row=4, column=0, padx=20, pady=10)
        
        #create a section of buttons for database tools, such as adding a product or supplier
        self.label2 = customtkinter.CTkLabel(self.sidebarFrame, text="Database tools:", font=customtkinter.CTkFont(size=12))
        self.label2.grid(row=5, column=0, padx=20)
        self.sideBarButton3 = customtkinter.CTkButton(self.sidebarFrame, command=lambda: self.goToTab("Data view"), text="Data view")
        self.sideBarButton3.grid(row=6, column=0, padx=20, pady=10)
        self.sideBarButton4 = customtkinter.CTkButton(self.sidebarFrame, command=lambda: self.goToTab("Add product"), text="Add product")
        self.sideBarButton4.grid(row=7, column=0, padx=20, pady=10)
        self.sideBarButton5 = customtkinter.CTkButton(self.sidebarFrame, command=lambda: self.goToTab("Add supplier"), text="Add supplier")
        self.sideBarButton5.grid(row=8, column=0, padx=20, pady=10)
        self.sideBarButton6 = customtkinter.CTkButton(self.sidebarFrame, command=lambda: self.goToTab("Waste"), text="Waste")
        self.sideBarButton6.grid(row=9, column=0, padx=20, pady=10)

        #create a section of buttons for tools that present data in graph format etc
        seperator2 = customtkinter.CTkFrame(self.sidebarFrame, height=1, width=100,fg_color="gray")
        seperator2.grid(row=10, column=0, padx=20, pady=10)
        self.label3 = customtkinter.CTkLabel(self.sidebarFrame, text="Data tools:", font=customtkinter.CTkFont(size=12))
        self.label3.grid(row=11, column=0, padx=20)
        self.sideBarButton7 = customtkinter.CTkButton(self.sidebarFrame, command=lambda: self.goToTab("Weekly report"), text="Weekly report")
        self.sideBarButton7.grid(row=12, column=0, padx=20, pady=10)
        self.sideBarButton8 = customtkinter.CTkButton(self.sidebarFrame, command=lambda: self.goToTab("Settings"), text="Settings")
        self.sideBarButton8.grid(row=13, column=0, padx=20, pady=(10,20))

        #========================BUTTON-STATES=======================>
        #tabview in which all UI will take place to do with functions of the application - the sidebar on the side simply allows for easier switching of the tabs
        self.setButtonStates() #set the button states (disabled or enabled) based on the user access
        
        #create the tabview according to allowances
        self.tabview = customtkinter.CTkTabview(master=self)
        self.tabview.grid(column=1, row=0)
        for tab in self.tabsDefault:
            self.tabview.add(tab)

        #disable any buttons & tabview tabs that the user doesnt have access to
        for page in self.tabsDefault:
            if page not in self.allowances[int(self.userAccessLevel)]:
                self.tabview.delete(page)

                for button in self.buttonsDefault:
                    name = button.cget("text")
                    if name == page:
                        button.configure(state="disabled")
                
        #<========================INITIALIZE-DATABASES========================>
        self.DBHandler = DBHandler() 
        self.supplierDB = supplierDBHandler()
        self.productDB = productDBHandler()
        self.wasteDB = wasteDBHandler()  
        self.stockLevelDB = stockLevelDBHandler()
        self.stockLevelHistoryDB = stockLevelHistoryDBHandler()
        self.weeklyReportDB = weeklyReportDBHandler()

        databases = [self.supplierDB, self.productDB, self.wasteDB, self.stockLevelDB, self.stockLevelHistoryDB, self.weeklyReportDB]

        for database in databases:
            try:
                database.initializeDatabase()

            except Exception as error:
                print(error)

        #<========================UI-SETTERS========================>
        uiSetters = [
            [self.homeUI, 3], 
            [self.recordDeliveryUI, 3], 
            [self.stockCountingUI, 3], 
            [self.dataViewUI, 1], 
            [self.addProductUI, 2], 
            [self.addSupplierUI, 2], 
            [self.wasteUI, 2], 
            [self.weeklyReportUI, 1],
            [self.settingsUI, 1]
            ]
        
        for uiSetter in uiSetters:
            if int(self.userAccessLevel) <= uiSetter[1]:  
                uiSetter[0]()  

    #function for buttons in the sidebar - used for navigating the tabview on the right
    def goToTab(self, tabName):
        self.tabview.set(tabName)

    def setButtonStates(self):
        #get user access level from login program in order to disable some functions
        self.tabsDefault = ["Home", "Record a delivery", "Stock counting", "Data view", "Add product", "Add supplier", "Waste", "Weekly report", "Settings"]
        self.buttonsDefault = [self.sideBarButton1, self.sideBarButton2, self.sideBarButton3, self.sideBarButton4, self.sideBarButton5, self.sideBarButton6, self.sideBarButton7, self.sideBarButton8]
        self.tabs = self.tabsDefault
        self.allowances: dict = {
                1: self.tabsDefault,
                2: list(filter(lambda tab_: tab_ not in ["Data view", "Weekly report", "Settings"], self.tabs)),
                3: list(filter(lambda tab_: tab_ not in ["Add product", "Add supplier", "Data view", "Weekly report", "Settings", "Waste"], self.tabs))
        }

    #=================================================================================================HOME-UI-AND-FUNCTIONALITY=================================================================================================    
    def homeUI(self, tab_='Home'):
        self.tab_ = tab_

        #Configure the grid to center for the centered welcome text
        self.tabview.tab(tab_).grid_rowconfigure([0, 1, 2], weight=1)
        self.tabview.tab(tab_).grid_columnconfigure([0, 1, 2, 3], weight=1)

        #set the welcome label in the center
        self.welcomeLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text=f"Hi {self.userName}!", font=customtkinter.CTkFont(size=35, weight="bold"), padx=0, pady=0)
        self.welcomeLabel.grid(row=0, column=0, columnspan=4, pady=(30,30))

        self.databaseBreakdown = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Database table breakdown:", font=customtkinter.CTkFont(size=15, weight="normal"), padx=0, pady=0)
        self.databaseBreakdown.grid(row=1, column=0, columnspan=4, pady=(15,30))

        #create the pie chart for displaying the table values
        pieChart = CTkPieChart(self.tabview.tab(tab_), line_width=50)
        pieChart.grid(row=2, column=0, padx=10, pady=(10, 50), sticky="e")

        try:
            pieChart.add("Products", self.productDB.getCount("products", False), text_color="black", color="#1F538D")
            pieChart.add("Suppliers", self.productDB.getCount("suppliers", False), text_color="black", color="gray")
            pieChart.add("Waste", self.productDB.getCount("waste", False), text_color="black", color="green")
            pieChart.add("Stocklevel", self.productDB.getCount("stocklevel", False), text_color="black", color="purple")
            pieChart.add("Users", self.productDB.getCount("users", False), text_color="black", color="yellow")
            pieChart.add("StockLevelHistory", self.productDB.getCount("stocklevelhistory", False), text_color="black", color="indigo")

        except TypeError:
            pass
        
        #get the dictionary of key value pairs to create the key for the pie chart
        pieChartValues = pieChart.get()

        #create a frame for the piechart
        pieChartFrame = customtkinter.CTkFrame(self.tabview.tab(tab_), fg_color="transparent")
        pieChartFrame.grid(row=2, column=1, padx=10, pady=10, sticky="e", columnspan=2) 

        #display the values for the key
        for key, values in pieChartValues.items():
            dataCircle = customtkinter.CTkRadioButton(pieChartFrame, hover=False, text=key, width=1,fg_color=values["color"])
            dataCircle.select()
            dataCircle.pack(side='top', anchor='nw', pady=5)

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
        self.deliveryDate = CTkDatePicker(self.tabview.tab(tab_))
        self.deliveryDate.grid(row=1, column=1, padx=(15, 20), pady=10, sticky='w')

        self.month = str(datetime.now().month)
        if len(self.month) == 1:
            self.month = f"0{datetime.now().month}"

        self.deliveryDate.date_entry.insert(0, f"{datetime.now().day}/{self.month}/{datetime.now().year}")

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
        seperator2 = customtkinter.CTkFrame(self.tabview.tab(tab_), height=2, fg_color="gray")
        seperator2.grid(row=5, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        #scrollable frame for added products
        self.products = []

        self.productFrame = customtkinter.CTkScrollableFrame(master=self.tabview.tab(tab_), width=300, height=200, corner_radius=0, fg_color="transparent")
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
        seperator3 = customtkinter.CTkFrame(self.tabview.tab(tab_), height=2, fg_color="gray")
        seperator3.grid(row=7, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        self.confirmDelivery = customtkinter.CTkButton(self.tabview.tab(tab_), text="Confirm delivery", command=self.confirmDelivery)
        self.confirmDelivery.grid(row=8, column=0, padx=20, pady=10)
    
    #function to add product
    def addProductToDelivery(self):
        productName = self.autocompleteEntry.get()
        productQuantity = self.quantityEntry.get()
        
        #check if product name and quantity are not empty
        if productName and productQuantity.isdigit():
            quantity = int(productQuantity)
            self.products.append([productName, quantity])
            
            #update the display
            self.updateProductList()
            
            #clear entry fields after adding
            self.autocompleteEntry.delete(0, customtkinter.END)
            self.quantityEntry.delete(0, customtkinter.END)

        else:
            messagebox.showwarning("Input Error", "Please enter a valid product name and quantity")

    #function to update the product list
    def updateProductList(self):
        #create a label and entry widget for each product in the list
        self.clearProductList()

        for i, product in enumerate(self.products):
            if i==0:
                self.clearProductList()

            countLabel = customtkinter.CTkLabel(self.productFrame, text=str(i+1))
            countLabel.grid(row=i+2, column=0, padx=20, sticky="w", pady=10)

            #name label with fixed width
            nameLabel = customtkinter.CTkLabel(self.productFrame, text=product[0])
            nameLabel.grid(row=i+2, column=1, padx=20, sticky="w", pady=10)

            #quantity entry with fixed width
            quantityEntryWidget = customtkinter.CTkEntry(self.productFrame)
            quantityEntryWidget.grid(row=i+2, column=2, padx=20, sticky="w", pady=10)
            quantityEntryWidget.insert(0, str(product[1]))  #insert the current quantity

            #delete button to remove the product
            print(self.products, i)
            print(self.products[i])
            deleteButton = customtkinter.CTkButton(self.productFrame, text="Delete", command=lambda i=i: self.deleteProductInDelivery(i))
            deleteButton.grid(row=i+2, column=3, padx=20, sticky="w", pady=10)

    #function to delete a product
    def deleteProductInDelivery(self, index):
        #remove product from the list
        del self.products[index]
        self.updateProductList()

    #Function to clear product list
    def clearProductList(self):
        #clear the existing list
        for widget in self.productFrame.winfo_children():
            if widget not in [self.productNumLabel, self.itemLabel, self.itemQuantityLabel, self.toolLabel]:
                widget.destroy()

        self.deliveryDate.date_entry.delete(0, customtkinter.END)
        self.deliveryDate.date_entry.insert(0, f"{datetime.now().day}/{self.month}/{datetime.now().year}")

    #Function to confirm the delivery
    def confirmDelivery(self):
        if messagebox.askquestion(title='Confirm delivery', message="Do you wish to confirm the delivery?"):
            try:
                #update stock levels and any other data here
                for product in self.products:
                    #update stock level
                    productID = self.productDB.getProductID(product[0])
                    self.stockLevelDB.updateStockLevel(product[1], productID, True)
                    #update last delivery date for product
                    self.stockLevelDB.updateLastDelivery(json.dumps(self.deliveryDate.get_date()), productID) #check json stuff

                #clear widgets once the delivery has been confirmed
                self.uiWidgetClearer()
                self.clearProductList()
                self.products = []

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

        #create a seperator to distuinguish between sections
        stockSeperator = customtkinter.CTkFrame(self.tabview.tab(tab_), height=2, fg_color="gray")
        stockSeperator.grid(row=2, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        #scrollable frame for added products
        self.stockCountProducts = []

        self.stockCountProductFrame = customtkinter.CTkScrollableFrame(master=self.tabview.tab(tab_), width=300, height=200, corner_radius=0, fg_color="transparent")
        self.stockCountProductFrame.grid(row=3, column=0, sticky="nsew", columnspan=6)
        self.stockCountProductNumLabel = customtkinter.CTkLabel(self.stockCountProductFrame, text="Item num", fg_color="transparent")
        self.stockCountProductNumLabel.grid(row=0, column=0, padx=(20), pady=20, sticky='w')
        self.stockCountitemLabel = customtkinter.CTkLabel(self.stockCountProductFrame, text="Date", fg_color="transparent")
        self.stockCountitemLabel.grid(row=0, column=1, padx=(20), pady=20, sticky='w')
        self.stockCountitemQuantityLabel = customtkinter.CTkLabel(self.stockCountProductFrame, text="Quantity", fg_color="transparent")
        self.stockCountitemQuantityLabel.grid(row=0, column=2, padx=(20), pady=20, sticky='w')
        self.stockCounttoolLabel = customtkinter.CTkLabel(self.stockCountProductFrame, text="Tool")
        self.stockCounttoolLabel.grid(row=0, column=3, padx=(20), pady=20, sticky='w')
        
        #create a seperator to distuinguish between sections
        stockCountseperator = customtkinter.CTkFrame(self.tabview.tab(tab_), height=2, fg_color="gray")
        stockCountseperator.grid(row=7, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        self.confirmStockCountButton = customtkinter.CTkButton(self.tabview.tab(tab_), text="Confirm stock count", command=self.confirmStockCount)
        self.confirmStockCountButton.grid(row=8, column=0, padx=20, pady=10)

    def addStockCountProductToDelivery(self):
        productName = self.stockCountAutocompleteEntry.get()
        productQuantity = self.stockCountQuantityEntry.get()
        
        #check if product name and quantity are not empty
        if productName and productQuantity.isdigit():
            quantity = int(productQuantity)
            self.stockCountProducts.append([productName, quantity])
            
            #update the display
            self.updateStockCountList()
            
            #clear entry fields after adding
            self.stockCountAutocompleteEntry.delete(0, customtkinter.END)
            self.stockCountQuantityEntry.delete(0, customtkinter.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a valid product name and quantity")

    #function to update the product list
    def updateStockCountList(self):
        #create a label and entry widget for each product in the list
        self.clearStockCountList()

        for i, stockCountProduct in enumerate(self.stockCountProducts):
            if i==0:
                self.clearStockCountList()

            stockCountLabel = customtkinter.CTkLabel(self.stockCountProductFrame, text=str(i+1))
            stockCountLabel.grid(row=i+2, column=0, padx=20, sticky="w", pady=10)

            #name label with fixed width
            nameLabel = customtkinter.CTkLabel(self.stockCountProductFrame, text=stockCountProduct[0])
            nameLabel.grid(row=i+2, column=1, padx=20, sticky="w", pady=10)

            #quantity entry with fixed width
            quantityEntryWidget = customtkinter.CTkEntry(self.stockCountProductFrame)
            quantityEntryWidget.grid(row=i+2, column=2, padx=20, sticky="w", pady=10)
            quantityEntryWidget.insert(0, str(stockCountProduct[1]))  #insert the current quantity

            #delete button to remove the product
            print(self.stockCountProducts, i)
            print(self.stockCountProducts[i])
            deleteButton = customtkinter.CTkButton(self.stockCountProductFrame, text="Delete", command=lambda i=i: self.deleteProductInStockCountList(i))
            deleteButton.grid(row=i+2, column=3, padx=20, sticky="w", pady=10)

    #Function to delete a product
    def deleteProductInStockCountList(self, index):
        #Remove product from the list
        del self.stockCountProducts[index]
        self.updateStockCountList()

    #function to clear product list
    def clearStockCountList(self):
        #clear the existing list
        for widget in self.stockCountProductFrame.winfo_children():
            if widget not in [self.stockCountProductNumLabel, self.stockCountitemLabel, self.stockCountitemQuantityLabel, self.stockCounttoolLabel]:
                widget.destroy()

    def confirmStockCount(self):
        if messagebox.askquestion(title='Confirm stockcount', message="Do you wish to confirm the stockcount?"):
            try:
                #update stock levels and any other data here
                for stockCountProduct in self.stockCountProducts:
                    #update stock level
                    productID = self.productDB.getProductID(stockCountProduct[0])
                    self.stockLevelDB.updateStockLevel(stockCountProduct[1], productID)

                #clear widgets once the stockcount has been confirmed
                self.uiWidgetClearer()
                self.clearStockCountList()

            except Exception as error:
                print(f"error encountered on stock count confirmation: {error}")
                return False

        else:
            pass

    #===================================================================================================DATA-VIEW-AND-FUNCTIONALITY====================================================================================================
    def dataViewUI(self, tab_='Data view'): 
        self.tab_ = tab_
        self.dataViewTabs = self.DBHandler.getTables()
        self.dataViewTabs.pop(self.dataViewTabs.index('users')) #remove the user table from data that can be displayed
        print(self.dataViewTabs)

        try: #windows based db table names are lowercase
            self.dataViewTabs.pop(self.dataViewTabs.index('stocklevelhistory')) #remove the stockLevelHistory table from data that can be displayed
            self.dataViewTabs.pop(self.dataViewTabs.index('weeklyreportrecords')) #^^^^

        except: #mac data view tab names are case sensitive for some reason
            self.dataViewTabs.pop(self.dataViewTabs.index('stockLevelHistory')) #remove the stockLevelHistory table from data that can be displayed
            self.dataViewTabs.pop(self.dataViewTabs.index('weeklyReportRecords')) #^^^^

        self.dataViewTabView = customtkinter.CTkTabview(self.tabview.tab(tab_))
        self.dataViewTabView.grid(row=1, column=0, pady=(50,50), padx=(50, 50))

        self.searchEntries = []
        self.dataSets = []
        self.displayTables = []

        #each search entry for each tab will produce suggestions based on the data in these respective columns. The index is the number of the column to be used when the the search button command is called
        searchEntrySuggestionsColumns = [
                                    ["product_name", 2], 
                                    ["stock_id", 0], 
                                    ["supplier_name", 1], 
                                    ["waste_id", 0],
                                    ]

        #add table tabs to tabview
        for i, _tab in enumerate(self.dataViewTabs):
            self.dataViewTabView.add(_tab)
            self.seeTableData(_tab, searchEntrySuggestionsColumns[i][0], searchEntrySuggestionsColumns[i][1], i) #set the individual dataview UI for each respective table and its UI
        
    #function to display the data inside the current table
    def seeTableData(self, tab__, searchEntrySuggestions, columnIndex, counter):
        self.tabbbb = tab__
        self.counter = counter

        #search entry to search the tableValues list
        self.searchEntry = AutocompleteEntry(self.dataViewTabView.tab(tab__), placeholder_text="search...", width=400)

        #sanitise columnData that was originally in tuple form and convert it into a string form
        suggestions = self.DBHandler.getColumnData(searchEntrySuggestions, tab__)
        for i, suggestion in enumerate(suggestions):
            suggestions[i] = str(reduce(lambda x, y: str(x) + ' ' + str(y), suggestion))
        
        #set the suggestions for the auto compplete based on the sanitsed data
        self.searchEntry.setSuggestions(suggestions)
        self.searchEntry.grid(row=0, column=0, padx=20, pady=30, sticky='nsew')

        #add search entry to search entries 2d list alongisde counter
        self.searchEntries.append([self.searchEntry, counter])

        self.searchButton = customtkinter.CTkButton(self.dataViewTabView.tab(tab__), text="Search 🔍", command=lambda:self.searchButtonAlgo(self.searchEntries[counter][0].get(), columnIndex, self.dataSets[counter], self.displayTables[counter], tab__))
        self.searchButton.grid(row=0, column=1, sticky='nsew', padx=20, pady=30)

        self.xy_frame = CTkXYFrame(self.dataViewTabView.tab(tab__), width=600, height=150)
        self.xy_frame.grid(row=2, column=0, sticky="nsew", columnspan=6)

        #display the table of values
        self.displayTable = CTkTable(self.xy_frame, values=self.getTableData(self.tabbbb), header_color="#1F538D")
        self.displayTable.grid(row=0, column=0)
        self.displayTables.append(self.displayTable)

    def getTableData(self, currentTab):
        #this needs to contain the database in a 2d list
        self.tableValues = [self.DBHandler.getColumnNames(currentTab)]
        self.dataSets.append(self.tableValues)

        for row in self.DBHandler.getData(currentTab):
            listVersion = list(row)

            for i, listItem in enumerate(listVersion):
                if type(listItem) is bytearray: #if the listItem is a byteArray (aka supplier dates as its stored in json), remove the byteArray prefixes
                    listVersion[i] = str(listItem.decode("utf-8"))

            self.tableValues.append(listVersion)

        return self.tableValues
        
    def searchButtonAlgo(self, itemToFind, column, dataSet, table, tab):
        self.graphVisualiser = CheckStockCount()
        for i, row in enumerate(dataSet):
            if str(row[int(column)]) == str(itemToFind):
                print(row)
                table.select_row(row=i)
                
                if tab == "products":
                    self.visualizeButtonLabel = customtkinter.CTkLabel(self.dataViewTabView.tab(tab), text="Stock level trends:")
                    self.visualizeButtonLabel.grid(row=3, column=0, padx=(10, 20), pady=20, sticky='w')
                    self.visualizeButton = customtkinter.CTkButton(self.dataViewTabView.tab(tab), text="Visualize ", command=lambda:self.visualize(itemToFind))
                    self.visualizeButton.grid(row=3, column=1, pady=20, padx=(10,20), sticky="w")

                if tab == "waste":
                    if row[4] == 0: #if waste isnt resolved, then allow user to resolve by updating waste_dealt_with value to 1
                        self.changeResolvementStatusLabel = customtkinter.CTkLabel(self.dataViewTabView.tab(tab), text="Update resolvement status:")
                        self.changeResolvementStatusLabel.grid(row=4, column=0, padx=(10), pady=20, sticky='w')

                        self.changeResolvementStatusButton = customtkinter.CTkButton(self.dataViewTabView.tab(tab), text="Change", command=lambda:self.wasteDB.updateWasteResolvementValue(row[0]))
                        self.changeResolvementStatusButton.grid(row=4, column=1, pady=20, padx=(10,20), sticky="w")
                    
                    else:
                        self.resolvementStatusLabel = customtkinter.CTkLabel(self.dataViewTabView.tab(tab), text="Waste already resolved")
                        self.resolvementStatusLabel.grid(row=4, column=0, padx=10, pady=20, sticky='w')

            else:
                table.deselect_row(row=i)

    def visualize(self, itemToFind):
        xAxisVals = []
        xAxisValsPrettified = []
        yAxisVals = []

        for row in self.stockLevelHistoryDB.getGraphValues(itemToFind):
            xAxisVals.append(row[0])
            xAxisValsPrettified.append(str(row[0])[:-9])
            yAxisVals.append(row[1])

        x = xAxisVals
        y = yAxisVals

        #create a line chart
        plt.figure(figsize=(8, 6))
        plt.plot(x, y, marker='o', linestyle='-')

        #add annotations
        for i, (xi, yi) in enumerate(zip(x, y)):
            plt.annotate(f'({yi})', (xi, yi), textcoords="offset points", xytext=(0, 10), ha='center')

        #add title and labels
        plt.title(f"{itemToFind} stock level")
        plt.xlabel("Date")
        plt.ylabel("Stock level")

        #display grid
        plt.grid(True)

        #show the plot
        plt.show()

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
        self.productNameLabel.grid(row=0, column=2, padx=(20, 20), pady=20, sticky='w')
        self.productNameEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="product name...")
        self.productNameEntry.grid(row=0, column=3, padx=(20, 20), pady=20, sticky='w')

        self.productBuyPriceEntryLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Product buy price: ")
        self.productBuyPriceEntryLabel.grid(row=1, column=0, padx=(20, 20), pady=20, sticky='w')
        self.productBuyPriceEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="buy price...")
        self.productBuyPriceEntry.grid(row=1, column=1, padx=(20, 20), pady=20, sticky='w')

        self.productSellPriceEntryLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Product sell price: ")
        self.productSellPriceEntryLabel.grid(row=1, column=2, padx=(20, 20), pady=20, sticky='w')
        self.productSellPriceEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="sell price...")
        self.productSellPriceEntry.grid(row=1, column=3, padx=(20, 20), pady=20, sticky='w')

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
                self.productDB.createProduct(supplierID[0], self.productNameEntry.get(), self.productDescriptionEntry.get(), self.productPSEntry.get(), self.productWeightEntry.get(), self.productBuyPriceEntry.get(), self.productSellPriceEntry.get())
                stockLevelProductID = self.productDB.getProductID(self.productNameEntry.get())
                self.stockLevelDB.addStockLevelData(stockLevelProductID, self.minimumStockLevelEntry.get(), self.reorderStockLevelEntry.get())
                self.autocompleteEntry.setSuggestions(self.productDB.getProductNames())

                for widget in [self.productNameEntry, self.productBuyPriceEntry, self.productSellPriceEntry, self.productPSEntry, self.productWeightEntry, self.minimumStockLevelEntry, self.reorderStockLevelEntry, self.productDescriptionEntry]:
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

    #limits entry widget to 200 characters by default
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
        self.supplierDatesEntry = CTkDatePicker(self.tabview.tab(tab_))
        self.supplierDatesEntry.grid(row=3, column=1, padx=(15, 20), pady=10, sticky='w')


        self.addSupplierDate = customtkinter.CTkButton(self.tabview.tab(tab_), text="Add supplier delivery date", command=self.addSupplierDeliveryDate)
        self.addSupplierDate.grid(row=3, column=2, padx=20, pady=10)

        #create a seperator to distuinguish between sections
        seperator = customtkinter.CTkFrame(self.tabview.tab(tab_), height=2, fg_color="gray")
        seperator.grid(row=4, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        #scrollable frame for added supplier dates
        self.supplierDates = []

        self.supplierDateFrame = customtkinter.CTkScrollableFrame(master=self.tabview.tab(tab_), width=300, height=200, corner_radius=0, fg_color="transparent")
        self.supplierDateFrame.grid(row=5, column=0, sticky="nsew", columnspan=6)
        self.supplierDateNumLabel = customtkinter.CTkLabel(self.supplierDateFrame, text="Date num", fg_color="transparent")
        self.supplierDateNumLabel.grid(row=0, column=0, padx=(20), pady=20, sticky='w')
        self.dateLabel = customtkinter.CTkLabel(self.supplierDateFrame, text="Item", fg_color="transparent")
        self.dateLabel.grid(row=0, column=1, padx=(20), pady=20, sticky='w')
        self.toolLabel = customtkinter.CTkLabel(self.supplierDateFrame, text="Tool")
        self.toolLabel.grid(row=0, column=3, padx=(20), pady=20, sticky='w')
        
        #create a seperator to distuinguish between sections
        seperator2 = customtkinter.CTkFrame(self.tabview.tab(tab_), height=2, fg_color="gray")
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
                self.uiWidgetClearer()
                
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
        deliveryDate = self.supplierDatesEntry.get_date()
        
        #check supplier date are not empty
        if deliveryDate:
            self.supplierDates.append(deliveryDate)
            self.updateSupplierDeliveryDateList()
            self.supplierDatesEntry.date_entry.delete(0, customtkinter.END)
        
        else:
            messagebox.showwarning("Input Error", "Please enter a valid delivery date")

    def updateSupplierDeliveryDateList(self):
        #create widgets for each supplier date
        self.clearSupplierDeliveryDateList()

        for i, supplierDate in enumerate(self.supplierDates):
            if i==0:
                self.clearSupplierDeliveryDateList()

            count_label = customtkinter.CTkLabel(self.supplierDateFrame, text=str(i+1))
            count_label.grid(row=i+2, column=0, padx=20, sticky="w", pady=10)

            #name label with fixed width
            name_label = customtkinter.CTkLabel(self.supplierDateFrame, text=supplierDate)
            name_label.grid(row=i+2, column=1, padx=20, sticky="w", pady=10)

            #delete button to remove the supplier date
            print(self.supplierDates, i)
            print(self.supplierDates[i])
            delete_button = customtkinter.CTkButton(self.supplierDateFrame, text="Delete", command=lambda i=i: self.deleteSupplierDate(i))
            delete_button.grid(row=i+2, column=3, padx=20, sticky="w", pady=10)

    def clearSupplierDeliveryDateList(self):
        #clear the existing list
        for widget in self.supplierDateFrame.winfo_children():
            if widget not in [self.supplierDateNumLabel, self.dateLabel, self.toolLabel]:
                widget.destroy()

    def deleteSupplierDate(self, index):
        #remove supplier date from the list
        del self.supplierDates[index]
        self.updateSupplierDeliveryDateList()

    #===================================================================================================WASTE-UI-AND-FUNCTIONALITY==================================================================================================
    def wasteUI(self, tab_='Waste'):
        self.tab_ = tab_

        self.findWasteProductLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Search product:")
        self.findWasteProductLabel.grid(row=0, column=0, padx=(20), pady=20, sticky='w')
        self.findWasteProductEntry = AutocompleteEntry(self.tabview.tab(tab_), width=500, placeholder_text='search product...')
        
        self.findWasteProductEntry.setSuggestions(self.productDB.getProductNames()) #set suggestions needs to be based on a call to the product table in the database
        self.findWasteProductEntry.grid(row=0, column=1, padx=20, pady=20, columnspan=3, sticky='w')
        
        self.wasteDescriptionLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Waste description: ")
        self.wasteDescriptionLabel.grid(row=1, column=0, padx=(20, 20), pady=20, sticky='w')
        self.wasteDescriptionEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), width=500, placeholder_text="waste description...")
        self.wasteDescriptionEntry.grid(row=1, column=1, padx=(20, 20), sticky='w', columnspan=5)

        self.wasteQuantityLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Quantity: ")
        self.wasteQuantityLabel.grid(row=2, column=0, padx=(20, 20), pady=10, sticky='w')
        self.wasteQuanitityEntry = customtkinter.CTkEntry(self.tabview.tab(tab_), placeholder_text="x")
        self.wasteQuanitityEntry.grid(row=2, column=1, padx=(20, 20), pady=10, sticky='w')
        self.wasteStateCheckboxVar = customtkinter.StringVar(value=False)
        self.wasteStateCheckbox = customtkinter.CTkCheckBox(self.tabview.tab(tab_), text="Dealt with",variable=self.wasteStateCheckboxVar, onvalue=True, offvalue=False)
        self.wasteStateCheckbox.grid(row=2, column=2)
        self.addWasteProduct = customtkinter.CTkButton(self.tabview.tab(tab_), text="Add waste product", command=self.addWasteProductToList)
        self.addWasteProduct.grid(row=2, column=3, padx=20, pady=10)

        #create a seperator to distuinguish between sections
        wasteSeperator1 = customtkinter.CTkFrame(self.tabview.tab(tab_), height=2, fg_color="gray")
        wasteSeperator1.grid(row=3, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        #scrollable frame for added products
        self.wasteProducts = []

        self.wasteProductFrame = customtkinter.CTkScrollableFrame(master=self.tabview.tab(tab_), width=300, height=200, corner_radius=0, fg_color="transparent")
        self.wasteProductFrame.grid(row=4, column=0, sticky="nsew", columnspan=6)
        self.wasteProductNumLabel = customtkinter.CTkLabel(self.wasteProductFrame, text="Item num", fg_color="transparent")
        self.wasteProductNumLabel.grid(row=0, column=0, padx=(20), pady=20, sticky='w')
        self.wasteItemLabel = customtkinter.CTkLabel(self.wasteProductFrame, text="Item", fg_color="transparent")
        self.wasteItemLabel.grid(row=0, column=1, padx=(20), pady=20, sticky='w')
        self.wasteItemQuantityLabel = customtkinter.CTkLabel(self.wasteProductFrame, text="Quantity", fg_color="transparent")
        self.wasteItemQuantityLabel.grid(row=0, column=2, padx=(20), pady=20, sticky='w')
        self.wasteStatusLabel = customtkinter.CTkLabel(self.wasteProductFrame, text="Status", fg_color="transparent")
        self.wasteStatusLabel.grid(row=0, column=3, padx=(20), pady=20, sticky='w')
        self.wasteToolLabel = customtkinter.CTkLabel(self.wasteProductFrame, text="Tool")
        self.wasteToolLabel.grid(row=0, column=4, padx=(20), pady=20, sticky='w')
        
        #create a seperator to distuinguish between sections
        wasteSeperator2 = customtkinter.CTkFrame(self.tabview.tab(tab_), height=2, fg_color="gray")
        wasteSeperator2.grid(row=7, column=0, columnspan=10, padx=20, pady=20, sticky='nsew')

        self.confirmWasteButton = customtkinter.CTkButton(self.tabview.tab(tab_), text="Confirm waste products", command=self.confirmAddWasteProductProcess)
        self.confirmWasteButton.grid(row=8, column=0, padx=20, pady=10)

    def confirmAddWasteProductProcess(self):
        try:
            if messagebox.askquestion(title='Confirm add waste product(s)', message="Do you wish to confirm this waste?"):
                #db call to create waste products
                for wasteProduct in self.wasteProducts:
                    product_id = wasteProduct[0]
                    supplier_id = self.productDB.getRespectiveSupplerID(product_id)
                    wasteReason = wasteProduct[1]
                    wasteQuantity = int(wasteProduct[2]) 
                    wasteState = wasteProduct[3]

                    #create waste product in the database
                    self.wasteDB.createWasteProduct(self.productDB.getProductID(product_id), supplier_id, wasteReason, wasteState)

                    #update stock level (subtracting waste quantity in the stock level db handler)
                    self.stockLevelDB.updateStockLevel(wasteQuantity, self.productDB.getProductID(product_id), isWaste=True)

                #reset widgets
                self.uiWidgetClearer()
                
                self.wasteProducts = []
                self.updateWasteProductList(True)

            #resume with app if "no" option is selected
            else:
                pass

        except Exception as error:
            print(error)
            messagebox.showerror("Error", f"An error occurred! Please try again. If this issue persits, please contact the maintainer. Error {error}")

    def addWasteProductToList(self):
        wasteProduct = [self.findWasteProductEntry.get(), self.wasteDescriptionEntry.get(), self.wasteQuanitityEntry.get(), self.wasteStateCheckboxVar.get()]
        
        #make sure we have all the data to create a waste product
        tally = 0
        for entryWidgetData in wasteProduct:
            if not(entryWidgetData == '') and wasteProduct[2].isdigit(): #make sure the quantity entry is a number
                tally += 1

        if tally == 4:
            self.wasteProducts.append(wasteProduct)
            self.updateWasteProductList()
            self.uiWidgetClearer()
            
            #reset entry widgets for a cleaner look and to not retain previously entered product data as this is already stored in the waste product list
            self.findWasteProductEntry.delete(0, customtkinter.END)
            self.wasteDescriptionEntry.delete(0, customtkinter.END)
            self.wasteQuanitityEntry.delete(0, customtkinter.END)
            self.wasteStateCheckbox.deselect() #make sure the checkbox is in the off state
        
        else:
            messagebox.showwarning("Input Error", "Please enter a valid waste product")

    def updateWasteProductList(self, clear_=False):
        if clear_:
            self.clearWasteProductList()

        for i, wasteProduct in enumerate(self.wasteProducts):
            if i==0:
                self.clearWasteProductList()

            count_label = customtkinter.CTkLabel(self.wasteProductFrame, text=str(i+1))
            count_label.grid(row=i+2, column=0, padx=20, sticky="w", pady=10)

            #Name label with fixed width
            name_label = customtkinter.CTkLabel(self.wasteProductFrame, text=wasteProduct[0])
            name_label.grid(row=i+2, column=1, padx=20, sticky="w", pady=10)

            #Delete button to remove the supplier date
            print(self.wasteProducts, i)
            print(self.wasteProducts[i])

            quantity_label = customtkinter.CTkLabel(self.wasteProductFrame, text=self.wasteProducts[i][2])
            quantity_label.grid(row=i+2, column=2, padx=20, sticky="w", pady=10)
            status_label = customtkinter.CTkLabel(self.wasteProductFrame, text=self.wasteProducts[i][3])
            status_label.grid(row=i+2, column=3, padx=20, sticky="w", pady=10)
            delete_button = customtkinter.CTkButton(self.wasteProductFrame, text="Delete", command=lambda i=i: self.deleteWasteProduct(i))
            delete_button.grid(row=i+2, column=4, padx=20, sticky="w", pady=10)

    def clearWasteProductList(self):
        #clear the existing list
        for widget in self.wasteProductFrame.winfo_children():
            if widget not in [self.wasteProductNumLabel, self.wasteItemLabel, self.wasteItemQuantityLabel, self.wasteStatusLabel]:
                widget.destroy()

    def deleteWasteProduct(self, index):
        # Remove waste product from the list
        del self.wasteProducts[index]
        self.updateWasteProductList()

    #===============================================================================================WEEKLY-REPORT-UI-AND-FUNCTIONALITY===================================================================================================    
    def weeklyReportUI(self, tab_='Weekly report'):
        self.tab_ = tab_

        #this should be a list of potential weeks
        reportsSortedByWeek = []
        prevWeeklyReportsIDS, self.weeklyReportsData = self.weeklyReportDB.getWeeklyReportsAsList()

        for report in prevWeeklyReportsIDS:
            reportsSortedByWeek.append(f"Weekly report - {report[0]}")

        reportsSortedByWeek = reportsSortedByWeek[::-1] #flip the order of weekly report to most recent first to advoid user having to scroll too far

        #this should be a list of potential weeks
        self.seePreviousWeeklyReportButtonCombobox = customtkinter.CTkOptionMenu(self.tabview.tab(tab_), values=reportsSortedByWeek)
        self.seePreviousWeeklyReportButtonCombobox.grid(row=0, column=0, padx=(20, 20), pady=20, sticky='w')

        self.seePreviousWeeklyReportButton = customtkinter.CTkButton(self.tabview.tab(tab_), text="See previous report", command=lambda:self.seePrevReport(self.seePreviousWeeklyReportButtonCombobox.get()))
        self.seePreviousWeeklyReportButton.grid(row=0, column=1, padx=(20, 20), pady=20, sticky='w')

        self.weeklyReportFrame = customtkinter.CTkScrollableFrame(master=self.tabview.tab(self.tab_), width=290, height=100, corner_radius=0, fg_color="transparent")
        self.weeklyReportFrame.grid(row=1, column=0, sticky="nsew", columnspan=6)

        seperator = customtkinter.CTkFrame(self.tabview.tab(tab_), height=2, fg_color="gray", width=660)
        seperator.grid(row=2, column=0, columnspan=10, padx=20, pady=20)

        self.sendEmailVar = customtkinter.StringVar(value=False)
        self.sendEmailCheckbox = customtkinter.CTkCheckBox(self.tabview.tab(tab_), text="Send email breakdown",variable=self.sendEmailVar, onvalue=True, offvalue=False)
        self.sendEmailCheckbox.grid(row=3, column=0, padx=(20, 20), pady=20, sticky='w')
        self.sendEmailCheckbox.select() #set default state as selected 

        self.produceTxtOutputVar = customtkinter.StringVar(value=False)
        self.produceTxtOutput = customtkinter.CTkCheckBox(self.tabview.tab(tab_), text="Produce .txt output",variable=self.sendEmailVar, onvalue=True, offvalue=False)
        self.produceTxtOutput.grid(row=3, column=1, padx=(20, 20), pady=20, sticky='w')
        self.produceTxtOutput.select() #set default state as selected 

        currentDate = datetime.today()
        currentDateMinusWeek = (currentDate - timedelta(weeks=1)).strftime("%d/%m/%Y")

        self.generateWeeklyReportButton = customtkinter.CTkButton(self.tabview.tab(tab_), text="Generate weekly report", command=lambda:self.generateWeeklyReport(currentDateMinusWeek, currentDate))
        self.generateWeeklyReportButton.grid(row=4, column=0, padx=(20, 20), pady=20, sticky='w')

        self.reportInfoLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text=f"*local reports will generate at {self._appLocation}") #tell the user where the report is generated by getting the working directory
        self.reportInfoLabel.grid(row=4, column=1, padx=(20, 20), pady=20, sticky='w')

        seperator2 = customtkinter.CTkFrame(self.tabview.tab(tab_), height=2, fg_color="gray", width=660)
        seperator2.grid(row=5, column=0, columnspan=10, padx=20, pady=20)

    def seePrevReport(self, selected):
        #delete any previous labels if there are any
        for widget in self.weeklyReportFrame.winfo_children():
            widget.destroy()

        date = selected[16:]
        target = []

        for report in self.weeklyReportsData:
            if report[2].strftime("%d/%m/%Y") == date:
                target.append(report)

        for i, report in enumerate(target):
            formattedReport = (f"Weekly report record ID: {report[0]}\n"
                 f"Product_ID: {report[1]}\n"
                 f"Date of creation: {report[2].strftime('%Y-%m-%d %H:%M:%S')}\n"
                 f"Trend in stock level: {report[3]}\n"
                 f"Predicted stock levels for next week: {report[4].decode()}\n"
                 f"Revenue: £{report[5]:.2f}\n"
                 f"COGS: £{report[6]:.2f}\n"
                 f"Profit: £{report[7]:.2f}")
            
            self.weeklyReportDataLabel = customtkinter.CTkLabel(self.weeklyReportFrame, text=f"Report record {i+1}) {formattedReport}") #tell the user where the report is generated by getting the working directory
            self.weeklyReportDataLabel.grid(row=i, column=0, padx=(20, 20), pady=20, sticky='w')

    def findDateRange(self, startDate, endDate):
        if type(startDate) == str: 
            startDate = datetime.strptime(startDate, "%d/%m/%Y")

        if type(endDate) == str: 
            endDate = datetime.strptime(endDate, "%d/%m/%Y")

        dateRangeList = []
        currentDate = startDate

        while currentDate <= endDate:
            dateRangeList.append(currentDate.strftime("%d/%m/%Y"))
            currentDate += timedelta(days=1)

        return dateRangeList

    def generateWeeklyReport(self, startDate, endDate):
        if messagebox.askquestion(title='Confirm generate weekly report', message="Do you wish to generate this weekly report?"):
            #WEEKLY REPORT GENERATION==============================================================================================
            dateRangeList = self.findDateRange(startDate, endDate)
            productNames = self.productDB.getProductNames()
            productDataMap = {}  #dict to store product data 

            #fetch stock history data 
            self.DBHandler.cursor.execute("SELECT stock_count, stock_history_product_name, DATE_FORMAT(date, '%d/%m/%Y'), action FROM stocklevelhistory")
            allStockData = self.DBHandler.cursor.fetchall()  

            #put stock history into the dict
            stockHistoryDict = {}
            for stockCount, productName, dateStr, action in allStockData:
                key = (productName, dateStr, action)

                if key not in stockHistoryDict:
                    stockHistoryDict[key] = []

                stockHistoryDict[key].append(stockCount)  

            #process data into productData2dList
            for dateStr in dateRangeList:
                for productName in productNames:
                    for action in ['delivery', 'count', 'waste']:  
                        key = (productName, dateStr, action)  

                        if key in stockHistoryDict:
                            stockCounts = stockHistoryDict[key]
                            
                            if productName not in productDataMap:
                                productDataMap[productName] = [productName, [], [], []]  
                            
                            #extend the stock counts and corresponding actions
                            productDataMap[productName][1].extend(stockCounts)  
                            productDataMap[productName][2].extend([dateStr] * len(stockCounts))
                            productDataMap[productName][3].extend([action] * len(stockCounts))  

            #conv dict vals into list
            productData2dList = list(productDataMap.values())
            for field in productData2dList:
                print(field, end="\n")

            weeklyReportData = []
            for currentIndex, valueList in enumerate(productData2dList):
                #add the productName to the current products data analysis
                weeklyReportData.append([valueList[0]])

                #create a dates and stockCounts list so that data can be analysed
                dates = []
                stockCounts = []
                actions = []
                for i in range(len(valueList[1])):
                    dateObj = datetime.strptime(valueList[2][i], "%d/%m/%Y")
                    dates.append(dateObj)
                    stockCounts.append(valueList[1][i])
                    actions.append(valueList[3][i])

                #append date and subsequent stock count info to the weekly report for this product
                newDates = []
                for _date in dates:
                    newDates.append(datetime.strftime(_date, "%d/%m/%Y")) #reformat the dates
                    
                weeklyReportData[currentIndex].append(newDates)
                weeklyReportData[currentIndex].append(stockCounts)

                #convert dates to ints
                startDate_ = dates[0]
                days = []

                for _date in dates:
                    days.append((_date - startDate_).days)
                    
                #calculate the trend in stock count (is it positive, negative, or stable?)
                sumX = 0
                sumY = 0
                sumXY = 0
                sumX2 = 0

                for i in range(len(days)):
                    sumX += days[i]
                    sumY += stockCounts[i]
                    sumXY += days[i] * stockCounts[i]
                    sumX2 += days[i] ** 2

                #calc the gradient
                numerator = (len(days) * sumXY) - (sumX * sumY)
                denominator = (len(days) * sumX2) - (sumX ** 2)

                if denominator != 0:
                    gradient = numerator / denominator

                else:
                    gradient = 0  

                if gradient > 0:
                    conclusion = "Increasing stock levels"
                    
                elif gradient < 0:
                    conclusion = "Decreasing stock levels"

                else:
                    conclusion = "No significant change"
                
                #add the type of trend in the stock level of the current product
                weeklyReportData[currentIndex].append(conclusion)

                #calculate the y intercept
                if len(days) > 0:
                    intercept = (sumY - gradient * sumX) / len(days)

                else:
                    intercept = 0  

                #predict stock levels for the next 7 days
                futureDays = []
                futureStock = []

                lastDay = days[-1] #last recorded day

                for i in range(1, 7): 
                    next_day = lastDay + i
                    futureDays.append(next_day)
                    futureStock.append(int(gradient * next_day + intercept))

                #add the predicted stock level for the next week to the data analysis for the current product
                weeklyReportData[currentIndex].append(futureStock)

                #calculate profit margins for the current week for this product
                self.DBHandler.cursor.execute("SELECT product_buy_price, product_sell_price FROM products WHERE product_name = ?", (valueList[0],))
                buyPrice, sellPrice = self.DBHandler.cursor.fetchone()

                #calculate revenue, cost of good sale & net profit
                totalRevenue = 0
                totalCogs = 0
                totalSold = 0  

                for i in range(len(stockCounts)):
                    if actions[i] == "count":  
                        totalSold += stockCounts[i]  
                        totalRevenue += stockCounts[i] * sellPrice  
                        totalCogs += stockCounts[i] * buyPrice 

                    elif actions[i] == "delivery":
                        continue

                    elif actions[i] == "waste":
                        totalSold += stockCounts[i]
                        totalRevenue -= stockCounts[i] * sellPrice
                        totalCogs += stockCounts[i] * buyPrice

                #calc net profit
                totalSold = totalRevenue - totalCogs

                weeklyReportData[currentIndex].append({"revenue": totalRevenue, "cogs": totalCogs, "profit": totalSold})

            #write record to weekly report table
            for product in weeklyReportData:
                product_id = self.productDB.getProductID(product[0])
                self.weeklyReportDB.addWeeklyReportRecord(product_id, product[3], json.dumps(product[4]), product[5]['revenue'], product[5]['cogs'], product[5]['profit'])

            #OPTIONAL STUFFS=======================================================================================================
            #if either of the send email or produce .txt file checkboxes are selected, then generate the multiline string output and go from there
            if self.produceTxtOutputVar.get() or self.sendEmailCheckbox.get():
                totalInfo = """"""
                for i, productReport in enumerate(weeklyReportData):
                    multiLineInfo = f""""""
                    if i != 0:
                        multiLineInfo += "<=====================================NEXT-PRODUCT========================================>\n"

                    multiLineInfo += f"PRODUCT-NAME: {productReport[0]}\n"
                    
                    multiLineInfo += f"_______________________________________________________________________\n"
                    multiLineInfo += f"PRODUCT-STOCK-COUNTS:\n"
                    multiLineInfo += f"_______________________________________________________________________\n"
                    
                    for j, date_ in enumerate(productReport[1]):
                        multiLineInfo += f"{date_}: {productReport[2][j]}\n"

                    multiLineInfo += f"_______________________________________________________________________\n"
                    multiLineInfo += f"LINEAR-REGRESSION-ANALYSIS: {productReport[3]}\n"
                    multiLineInfo += f"_______________________________________________________________________\n"
                    multiLineInfo += f"PREDICTED-STOCK-COUNT-FOR-NEXT-WEEK: \n-> {productReport[4]}\n"
                    multiLineInfo += f"_______________________________________________________________________\n"
                    multiLineInfo += f"<=========================================================================================>\n\n\n\n"

                    totalInfo += multiLineInfo

                #local weekly reports are stored in a weekly reports folder, if it doesnt exist then make it
                if self.produceTxtOutputVar.get():
                    reportPath = f"weeklyReports"
                    if not os.path.exists(reportPath):
                        os.makedirs(reportPath)

                    #create .txt file here
                    newWeeklyReportFilePath = f"weekly_report_{date.today().strftime('%d-%m-%Y')}.txt"
                    print(f"Generated file path: {newWeeklyReportFilePath}")

                    if not os.path.isfile(newWeeklyReportFilePath):
                        with open(newWeeklyReportFilePath, 'w') as file_:
                            file_.write(totalInfo)
                            
                        #move weekly report file to weekly reports
                        shutil.move(newWeeklyReportFilePath, f"weeklyReports/{newWeeklyReportFilePath}")
                    
                    else:
                        message = popUpWindow("Weekly report already exists")
                        message.create()

                #user might want the report emailed, so do this here (however this is selected by default)
                if self.sendEmailCheckbox.get():
                    #send email containing report here
                    emailAlert = appEmail()
                    emailAlert.sendEmail(self._defAlertEmail, f"Weekly report - {date.today().strftime('%d-%m-%Y')}", totalInfo)

    #=================================================================================================SETTINGS-UI-AND-FUNCTIONALITY=================================================================================================    
    def settingsUI(self, tab_='Settings'):
        self.tab_ = tab_

        #user tools
        self.userToolsLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="User tools:")
        self.userToolsLabel.grid(row=0, column=0, padx=(20, 20), pady=20, sticky='w')
        self.addUserButton = customtkinter.CTkButton(self.tabview.tab(tab_), text="Create new user", command=self.addNewUser)
        self.addUserButton.grid(row=1, column=0, sticky="nw", padx=(20, 20))

        #configure settings button states
        if int(self.userAccessLevel) != 1:
            for settingsButton in [self.addUserButton]:
                settingsButton.configure(state="disabled")

        if int(self.userAccessLevel) == 1:
            #show environment variables and edit them if the user is an admin
            self.envVariableLabel = customtkinter.CTkLabel(self.tabview.tab(tab_), text="Environment variables:")
            self.envVariableLabel.grid(row=2, column=0, padx=(20, 20), pady=20, sticky='nw')
            
            self.envVarLabels = {}
            self.envVars = ["DB_USERNAME", "DB_PASSWORD", "DB_HOST", "DB_SCHEMA", "DEF_EMAIL_ADDR", "DEF_EMAIL_ADDR_PASS", "DEF_ALERT_RECIPIENT_EMAIL"]
            rows = [3, 4, 5, 6, 7, 8, 9]

            maxVarLen = max(len(var) for var in self.envVars)
            dots_ = 5 

            self.envVarEntries = {} 
            self.envVarButtons = {}  

            for i, variable in enumerate(self.envVars):
                envValue = os.getenv(variable, "N/A")  
                dots = "." * (maxVarLen + dots_ - len(variable))
                info = f"{i+1}) {variable} {dots} {envValue}"

                #label to display current environment variable
                self.envVarLabels[i] = customtkinter.CTkLabel(self.tabview.tab(tab_), text=info, font=("Courier", 12))
                self.envVarLabels[i].grid(row=rows[i], column=0, padx=(40, 10), pady=(10,10), sticky='w')

                #entry field to input new value
                self.envVarEntries[i] = customtkinter.CTkEntry(self.tabview.tab(tab_), width=200, placeholder_text="new value...")
                self.envVarEntries[i].grid(row=rows[i], column=1, padx=(10, 10), sticky='w')

                #tick button to update the variable
                def updateEnvVar(var=variable, entryWidget=self.envVarEntries[i]):
                    newValue = entryWidget.get()
                    envVarPath="src/config/.env"

                    if newValue:
                        dotenv.set_key(envVarPath, var, newValue, quote_mode='always', export=False, encoding='utf-8')
                        print(f"Updated {var} -> {newValue}") 
                        entryWidget.delete(0, customtkinter.END)

                self.envVarButtons[i] = customtkinter.CTkButton(self.tabview.tab(tab_), text="↻", width=30,  command=updateEnvVar)
                self.envVarButtons[i].grid(row=rows[i], column=2, padx=(10, 0), sticky='w')

    def addNewUser(self):
        user = newUser()
        user.mainloop()

    #=================================================================================================MISC-FUNCTIONALITY=============================================================================================================
    def uiWidgetClearer(self):
        for widget in self.tabview.tab(self.tab_).winfo_children():
            try:
                if widget.cget('placeholder_text'):
                    widget.delete(0, customtkinter.END)
                    widget._activate_placeholder()
                    widget.focus()
            
            except ValueError:
                continue

    #===================================================================================================STATIC-METHODS================================================================================================================
    #func to check if there are any widgets present in a row
    def isRowEmpty(parent, rowNumber):
        for widget in parent.winfo_children():
            info = widget.grid_info() 

            if 'row' in info and info['row'] == rowNumber:
                return False  
        
        return True



if __name__ == "__main__":
    def runMainApp():
        #initalise the databases logon database
        initialiser = logonDBHandler()
        initialiser.initializeDatabase()

        login = Logon()
        login.mainloop()

    def checkStockCounts():
        runStockCheck = CheckStockCount()
        runStockCheck.runStockLevelCheckAgainstMinimum()

    mainAppThread = threading.Thread(target=runMainApp)
    checkStockCountThread = threading.Thread(target=checkStockCounts)

    #for running on mac, the UI needs to run on the main thread, otherwise there will be an exception
    if threading.current_thread() is threading.main_thread():
        runMainApp()

    else:
        threading.main_thread().run(runMainApp)

    checkStockCountThread.start()
    checkStockCountThread.join()