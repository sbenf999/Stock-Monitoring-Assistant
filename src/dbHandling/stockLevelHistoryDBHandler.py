from dbHandling.DBHandler import *

class stockLevelHistoryDBHandler(DBHandler):
    def initializeDatabase(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS stockLevelHistory (
                    stockHistory_id INT AUTO_INCREMENT PRIMARY KEY,
                    stock_id INT,
                    product_id INT,
                    stock_history_product_name VARCHAR(100) NOT NULL,
                    stock_count INT,
                    date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (stock_id) REFERENCES stocklevel(stock_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            ''')

        except Exception as error:
            return False, error
        
    def addStockLevelHistoryData(self, stockID, productID, stockHistoryProductName, stockCount):
        try:
            params = (stockID, productID, stockHistoryProductName, stockCount[0])

            self.cursor.execute('''INSERT INTO stockLevelHistory (stock_id, product_id, stock_history_product_name, stock_count) VALUES (%s, %s, %s, %s)''', params)
            self.connection.commit()
            return True

        except Exception as error:
            self.connection.rollback()
            print(f"slhdb: {error}")
            return False, error
        
    def getGraphValues(self, productName):
        try:
            self.cursor.execute('''SELECT date, stock_count FROM stocklevelhistory WHERE stock_history_product_name = %s''', (productName,))
            data = self.cursor.fetchall()
            return data

        except Exception as error:
            self.connection.rollback()
            print(f"slhdb: {error}")
            return False, error
