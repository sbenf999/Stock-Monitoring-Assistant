from dbHandling.DBHandler import *

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
                    product_price DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_ID)
                )
            ''')

        except Exception as error:
            return False, error
        

    def createProduct(self, supplier_id, product_name, product_description, product_pack_size, product_weight, product_price, product_barcode=000000000):
        try:
            self.cursor.execute('''INSERT INTO products (supplier_id, product_name, product_description, product_pack_size, product_weight, product_barcode, product_price) VALUES (%s, %s, %s, %s, %s, %s, %s)''', (supplier_id, product_name, product_description, product_pack_size, product_weight, product_barcode, product_price))
            self.connection.commit()
            return True
        
        except Exception as error:
            self.connection.rollback()
            return False, error
        

    #need to program
    def deleteProduct(self):
        pass

    def updateProductStockCount(self):
        pass

    def updateProductValue(self, value):
        pass