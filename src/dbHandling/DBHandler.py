#database imports
import mysql.connector
from mysql.connector import errorcode

#graphing imports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#general imports
import customtkinter
from dotenv import load_dotenv
import os

#overarching parent class for handling database connections. All child classes will serve a specific function
class DBHandler:

    # Load environment variables from the .env file
    envVarPath="src/config/.env"
    load_dotenv(dotenv_path=envVarPath)

    __username = os.getenv("DB_USERNAME")
    __password = os.getenv("DB_PASSWORD")
    __host = os.getenv("DB_HOST")
    __schema = os.getenv("DB_SCHEMA")
    connection = ""
    cursor = ""

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user=self.__username, password=self.__password, host=self.__host, database=self.__schema, auth_plugin='mysql_native_password') 
            self.cursor = self.connection.cursor(prepared=True)   

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(err)
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)   
    
    def createBarGraphVisualisation(self, root):
        categories = self.getTables()
        values = []
        for category in categories:
            values.append(self.getCount(category, False))

        

    def getCount(self, tableName, displayType=True):
        _allowed_tables = self.getTables()

        if tableName not in _allowed_tables:
            raise ValueError(f"Invalid table name: {tableName}")
        
        try:
            query = f"SELECT COUNT(*) FROM {tableName}"
            self.cursor.execute(query)
            rowCount = self.cursor.fetchone()[0]

            if displayType:
                spacing = 3-len(str(rowCount))
                zeros = spacing*"0"
                prettified = f"{zeros}{rowCount} {tableName}"
                return prettified
            
            else:
                return rowCount

        except Exception as error:
            print(f"Error encountered: {error}")
            return None

    def getTables(self):
        self.cursor.execute("SHOW TABLES")
        tables = self.cursor.fetchall()
        tableNames = [table[0] for table in tables]
        return tableNames

    def close(self):
        self.connection.close()