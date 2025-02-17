#database imports
from dbHandling.DBHandler import *
from dbHandling.stockLevelDBHandler import *
from dbHandling.productDBHandler import *

#process imports
from processes.sendEmail import *

#graphing imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure 
import numpy as np
import matplotlib.pyplot as plt

#general imports
import customtkinter

class CheckStockCount(DBHandler):
    __defaultStockLevelTable = "stocklevel"
    
    def runStockLevelCheckAgainstMinimum(self):
        self.cursor.execute(f"SELECT product_id, stock_count, minimum_stock_level, reOrder_level FROM {self.__defaultStockLevelTable} WHERE stock_count <= minimum_stock_level")
        dataToUse = self.cursor.fetchall()

        self.productDBHandler = productDBHandler()

        for i in range(len(dataToUse)):
            productName = self.productDBHandler.getProductName(dataToUse[i][0])

            subject = f"Stock level alert: stock count for '{productName}' is lower than minimum"
            content = f"Stock level {dataToUse[i][1]} is lower than minimum stock level {dataToUse[i][2]}. A new delivery is recommended."
            
            emailAlert = appEmail()
            emailAlert.sendEmail(self._defAlertEmail, subject, content)

    def plotGraph(self, productName):
        xAxisVals = []
        yAxisVals = []

        self.graphFrame = customtkinter.CTkFrame(self)
        self.graphFrame.pack(pady=20, padx=20, fill="both", expand=True)

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(xAxisVals, yAxisVals, marker="o", linestyle="-", color="#1F538D")
        ax.set_title(f"{productName} stock level")
        ax.set_xlabel("Date")
        ax.set_ylabel("Stock level")

        self.canvas = FigureCanvasTkAgg(fig, master=self.graphFrame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.canvas.draw()


