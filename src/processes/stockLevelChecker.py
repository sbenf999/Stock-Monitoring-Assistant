#database imports
from dbHandling.DBHandler import *
from dbHandling.stockLevelDBHandler import *
from dbHandling.productDBHandler import *
from dbHandling.stockLevelHistoryDBHandler import *

#graphing imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure 
import numpy as np
import matplotlib.pyplot as plt

#process imports
from processes.sendEmail import *

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
