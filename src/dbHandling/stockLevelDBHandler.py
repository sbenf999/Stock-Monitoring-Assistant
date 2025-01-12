from dbHandling.DBHandler import *

class stockLevelDBHandler(DBHandler):
    tableName="stockLevel"

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
