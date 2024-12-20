from DBHandler import *

class supplierDBHandler(DBHandler):
    def initializeDatabase(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    product_id INT auto_increment PRIMARY KEY,
                    supplier_id INT,
                    product_name VARCHAR(100) NOT NULL,
                    product_description VARCHAR(200),
                    product_pack_size INT NOT NULL,
                    product_weight INT NOT NULL,
                    product_barcode STR NOT NULL
                    FOREGIN KEY (supplier_id) REFERENCES suppliers(supplier_ID)
                )
            ''')

        except Exception as error:
            return False, error