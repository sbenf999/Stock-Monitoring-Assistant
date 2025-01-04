from DBHandler import *

from productDBHandler import *
from supplierDBHandler import *
from wasteDBHandler import *

def runMainDBInstatiator():
    supplierDB = supplierDBHandler()
    productDB = productDBHandler()
    wasteDB = wasteDBHandler()

    databases = [supplierDB, productDB, wasteDB]

    for database in databases:
        try:
            database.initializeDatabase()
            print(f"Database {database} initialised successfully")

        except Exception as error:
            print(error)