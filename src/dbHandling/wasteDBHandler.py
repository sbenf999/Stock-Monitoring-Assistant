from dbHandling.DBHandler import *

class wasteDBHandler(DBHandler):
    def initializeDatabase(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS waste (
                    waste_id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT,
                    supplier_id INT,
                    waste_reason VARCHAR(200) NOT NULL,
                    waste_dealt_with BOOLEAN NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES products(product_id),
                    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
                )
            ''')

        except Exception as error:
            return False, error
        
    def createWasteProduct(self, product_id, supplier_id, waste_reason, waste_dealt_with):
        try:
            self.cursor.execute('''INSERT INTO waste (product_id, supplier_id, waste_reason, waste_dealt_with) VALUES (%s, %s, %s, %s)''', (product_id, supplier_id, waste_reason, waste_dealt_with))
            self.connection.commit()
            return True
        
        except Exception as error:
            self.connection.rollback()
            print(f"Error in create waste product: {error}")
            return False, error