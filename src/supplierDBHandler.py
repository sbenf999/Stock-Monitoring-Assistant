from DBHandler import *

class supplierDBHandler(DBHandler):
    def initializeDatabase(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS suppliers (
                    supplier_id INT auto_increment PRIMARY KEY,
                    supplier_description CHAR(255) NOT NULL,
                    supplier_delivery_date VARCHAR(50) NOT NULL
                )
            ''')

        except Exception as error:
            return False, error