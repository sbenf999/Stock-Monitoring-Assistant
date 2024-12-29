from DBHandler import *

from productDBHandler import *
from supplierDBHandler import *
from wasteDBHandler import *

supplierDB = supplierDBHandler()
productDB = productDBHandler()
wasteDB = wasteDBHandler()

databases = [supplierDB, productDB, wasteDB]

for database in databases:
    print(database.initializeDatabase())