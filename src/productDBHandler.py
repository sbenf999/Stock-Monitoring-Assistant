from DBHandler import *

class productDBHandler(DBHandler):
    def initializeDatabase(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    product_id INT AUTO_INCREMENT PRIMARY KEY,
                    supplier_id INT,
                    product_name VARCHAR(100) NOT NULL,
                    product_description VARCHAR(200),
                    product_pack_size INT NOT NULL,
                    product_weight INT NOT NULL,
                    product_barcode VARCHAR(50) NOT NULL,
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_ID)
                )
            ''')

        except Exception as error:
            return False, error