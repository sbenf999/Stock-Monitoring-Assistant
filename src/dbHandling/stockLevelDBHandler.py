from dbHandling.DBHandler import *

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

    def addStockLevelData(self, productID, minStockLevel, reOrderLevel, *, stockCount=None, lastDelivery=None):
        try:
            self.cursor.execute('''INSERT INTO stocklevel (product_id, minimum_stock_level, reOrder_level) VALUES (%s, %s, %s)''', (productID, minStockLevel, reOrderLevel))
            self.connection.commit()
            return True
        
        except Exception as error:
            self.connection.rollback()
            print(f"sldb: {error}")
            return False, error