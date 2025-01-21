from dbHandling.DBHandler import *
import json

class stockLevelDBHandler(DBHandler):
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
            return True

        except Exception as error:
            self.connection.rollback()
            print(f"sldb: {error}")
            return False, error
        
    def updateStockLevel(self, addedStockCount, productID):
        DBHandler.dbCall("INSERT INTO stocklevel (stock_count) VALUES (%s) WHERE product_id = %s", (addedStockCount,productID))

    def updateLastDelivery(self, lastDelivery, productID):
        DBHandler.dbCall("UPDATE stocklevel SET lastDelivery = %s WHERE product_id = %s", (lastDelivery,productID))