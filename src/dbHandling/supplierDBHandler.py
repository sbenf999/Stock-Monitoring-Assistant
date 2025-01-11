from dbHandling.DBHandler import *

class supplierDBHandler(DBHandler):
    def initializeDatabase(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS suppliers (
                    supplier_id INT auto_increment PRIMARY KEY,
                    supplier_name VARCHAR(100) NOT NULL,
                    supplier_description CHAR(255) NOT NULL,
                    supplier_delivery_date JSON
                )
            ''')

        except Exception as error:
            return False, error
        

    def getSupplierNames(self):
        try:
            self.cursor.execute("SELECT supplier_name FROM suppliers")
            results = self.cursor.fetchall()
            supplier_names = [row[0] for row in results]
            return supplier_names
        
        except Exception as error:
            return False, error
        
    def createSupplier(self, supplier_name, supplier_description, supplier_delivery_date):
        try:
            self.cursor.execute('''INSERT INTO suppliers (supplier_name, supplier_description, supplier_delivery_date) VALUES (%s, %s, %s)''', (supplier_name, supplier_description, supplier_delivery_date))
            self.connection.commit()
            return True
        
        except Exception as error:
            self.connection.rollback()
            return False, error
        
    
    def getSupplierID(self, supplier_name):
        try:
            self.cursor.execute('''SELECT supplier_id FROM suppliers WHERE supplier_name = %s''', (supplier_name))
            self.connection.commit()
            result = self.cursor.fetchone()
            return result
        
        except Exception as error:
            self.connection.rollback()
            return False, error
        

    #needs to be programmed
    def deleteSupplier(self):
        pass

    def getSupplierDeliveryDates(self):
        pass
        