from DBHandler import *

class wasteDBHandler(DBHandler):
    def initializeDatabase(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS waste (
                    waste_id INT auto_increment PRIMARY KEY,
                    product_id INT,
                    supplier_id INT,
                    waste_reason VARCHAR(200) NOT NULL,
                    waste_dealt_with BOOL NOT NULL,
                    FOREGIN KEY (product_id) REFERENCES products(product_id)
                    FOREGIN KEY (supplier_id) REFERENCES suppliers(supplier_id)
                )
            ''')

        except Exception as error:
            return False, error