from dbHandling.DBHandler import *
from dbHandling.stockLevelHistoryDBHandler import *
from dbHandling.productDBHandler import *
import json

class stockLevelDBHandler(DBHandler):
    stockLevelHistoryDB = stockLevelHistoryDBHandler()
    productDBHandler_ = productDBHandler()

    def initializeDatabase(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS stockLevel (
                    stock_id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT,
                    stock_count INT NOT NULL,
                    minimum_stock_level INT NOT NULL, 
                    reOrder_level INT NOT NULL,
                    lastDelivery JSON,         
                    FOREIGN KEY (product_id) REFERENCES products(product_ID)
                )
            ''')

        except Exception as error:
            return False, error

    def addStockLevelData(self, productID, minStockLevel, reOrderLevel, *, stockCount=0, lastDelivery="[]"):
        try:
            if isinstance(lastDelivery, dict):
                lastDelivery = json.dumps(lastDelivery)

            params = (productID, minStockLevel, reOrderLevel, stockCount, lastDelivery)

            self.cursor.execute('''INSERT INTO stocklevel (product_id, minimum_stock_level, reOrder_level, stock_count, lastDelivery) VALUES (%s, %s, %s, %s, %s)''', params)
            self.connection.commit()

            stockID = self.getStockID(productID)
            self.stockLevelHistoryDB.addStockLevelHistoryData(stockID, productID, self.productDBHandler_.getProductName(productID), stockCount)

            return True

        except Exception as error:
            self.connection.rollback()
            print(f"sldb: {error}")
            return False, error
        
    def updateStockLevel(self, addedStockCount, productID, isDelivery=False):
        try:
            self.cursor.execute("SELECT stock_count FROM stockLevel WHERE product_id = %s", (productID,))
            stockLevelNum = self.cursor.fetchone()
            print(stockLevelNum, addedStockCount)

            if isDelivery: #if the update stock level is for a delivery, we are simply adding more not overwriting the previous stock level (as a delivery = more stock)
                self.cursor.execute("UPDATE stockLevel SET stock_count = stock_count + %s WHERE product_id = %s", (addedStockCount, productID))
            
            else:
                self.cursor.execute("UPDATE stockLevel SET stock_count = %s WHERE product_id = %s", (addedStockCount, productID))

            self.connection.commit()

            #update stock level history table with change in stockLevel
            stockID = self.getStockID(productID)
            self.stockLevelHistoryDB.addStockLevelHistoryData(stockID, productID, self.productDBHandler_.getProductName(productID), stockLevelNum[0])

        except Exception as error:
            print(f"error in updateStockLevel: {error}")
            return False
        
    def getStockID(self, productID):
        try:
            self.cursor.execute("SELECT stock_Id FROM stockLevel WHERE product_id = %s", (productID,))
            return self.cursor.fetchone()[0]

        except Exception as error:
            print(f"error in getStockId: {error}")
            return False

    def updateLastDelivery(self, lastDelivery, productID):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM stockLevel")
            rowCount = self.cursor.fetchone()[0]

            if rowCount == 0:
                self.cursor.execute("INSERT INTO stockLevel (lastDelivery) VALUES (%s) WHERE product_id = %s", (lastDelivery,productID))

            else:
                self.cursor.execute("UPDATE stockLevel SET lastDelivery = %s WHERE product_id = %s", (lastDelivery,productID))

            self.connection.commit()

        except Exception as error:
            print(f"error: {error}")
            return False