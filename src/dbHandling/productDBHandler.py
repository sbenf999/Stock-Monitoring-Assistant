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
                    product_buy_price DECIMAL(10,2) NOT NULL,
                    product_sell_price DECIMAL (10,2) NOT NULL,
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_ID)
                )
            ''')

        except Exception as error:
            return False, error
        
    def createProduct(self, supplier_id, product_name, product_description, product_pack_size, product_weight, product_buy_price, product_sell_price, product_barcode=000000000):
        try:
            self.cursor.execute('''INSERT INTO products (supplier_id, product_name, product_description, product_pack_size, product_weight, product_barcode, product_buy_price, product_sell_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (supplier_id, product_name, product_description, product_pack_size, product_weight, product_barcode, product_buy_price, product_sell_price))
            self.connection.commit()
            return True
        
        except Exception as error:
            self.connection.rollback()
            print(f"Error in create product: {error}")
            return False, error
    
    def getProductNames(self):
        try:
            self.cursor.execute("SELECT product_name FROM products")
            results = self.cursor.fetchall()
            productNames = [row[0] for row in results]
            return productNames
        
        except Exception as error:
            return False, error

    def getProductID(self, productName):
        try:
            self.cursor.execute("SELECT product_id FROM products WHERE product_name = %s", (productName,))
            results = self.cursor.fetchone()
            return results[0]
        
        except Exception as error:
            return False, error
        
    def getProductName(self, productID):
        try:
            self.cursor.execute("SELECT product_name FROM products WHERE product_id = %s", (productID,))
            results = self.cursor.fetchone()
            return results[0]
        
        except Exception as error:
            return False, error
        
    def getRespectiveSupplerID(self, productName):
        try:
            self.cursor.execute("SELECT supplier_id FROM products WHERE product_name = %s", (productName,))
            results = self.cursor.fetchone()
            return results[0]
        
        except Exception as error:
            return False, error

    #need to program
    def deleteProduct(self):
        pass

    def updateProductValue(self, dbColumnVal, productID):
        self.cursor.execute("UPDATE products SET %s WHERE product_id = %s", (dbColumnVal, productID))
        self.connection.commit()