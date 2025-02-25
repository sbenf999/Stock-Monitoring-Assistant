#database imports
import mysql.connector
from mysql.connector import errorcode

#general imports
from dotenv import load_dotenv
import os

#overarching parent class for handling database connections. All child classes will serve a specific function
class DBHandler:

    #Load environment variables from the .env file
    envVarPath="src/config/.env"
    load_dotenv(dotenv_path=envVarPath)

    __username = os.getenv('DB_USERNAME')
    __password = os.getenv('DB_PASSWORD')
    __host = os.getenv('DB_HOST')
    __schema = os.getenv('DB_SCHEMA')
    _defAlertEmail = os.getenv('DEF_ALERT_RECIPIENT_EMAIL')
    connection = ""
    cursor = ""

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user=self.__username, password=self.__password, host=self.__host, database=self.__schema)#, auth_plugin='mysql_native_password') 
            self.cursor = self.connection.cursor(prepared=True)
            print(self.isConnected()) 

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(err)
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)   

    #method to test connection to server
    def isConnected(self):
        if self.connection.is_connected():
            return f"Database {self} initialised successfully"
        
        return False

    def getCount(self, tableName, displayType=True):
        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM {tableName}")
            rowCount = self.cursor.fetchone()[0]

            if displayType:
                spacing = 3-len(str(rowCount))
                zeros = spacing*"0"
                prettified = f"{zeros}{rowCount} {tableName}"
                return prettified
            
            else:
                return rowCount

        except Exception as error:
            print(f"Error encountered (getCount): {error}")
            return None
        
    def getColumnNames(self, tableName):
        self.cursor.execute(f"SELECT * FROM {tableName} LIMIT 0")
        self.cursor.fetchall()

        columnNames = []
        for description in self.cursor.description:
            columnNames.append(description[0])

        return columnNames
    
    def getColumnData(self, columnName, tableName):
        self.cursor.execute(f"SELECT {columnName} FROM {tableName}") 
    
        return self.cursor.fetchall()
    
    def getColumnCount(self, tableName):
        self.cursor.execute(f"SELECT * FROM {tableName} LIMIT 1") 
        self.cursor.fetchall()
        columnCount = len(self.cursor.description)
        
        return columnCount

    def getTables(self):
        try:
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            tableNames = [table[0] for table in tables]
            return tableNames

        except Exception as error:
            print(f"error encountered: {error}")

    def getData(self, tableName):
        self.cursor.execute(f"SELECT * FROM {tableName}")
        return self.cursor.fetchall()
    
    def generalUpdateRecord(self, tableName, columnName, oldVar, newVar):
        self.cursor.execute(f"INSERT INTO {tableName} ({columnName}) VALUES (%s) WHERE {columnName} == {oldVar}", (newVar,))

    def close(self):
        self.connection.close()
