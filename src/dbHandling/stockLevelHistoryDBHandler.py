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
                    date DATETIME NOT NULL,
                    FOREIGN KEY (stock_id) REFERENCES stocklevel(stock_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id)
                )
            ''')

        except Exception as error:
            return False, error
