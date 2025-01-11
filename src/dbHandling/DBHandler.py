import mysql.connector
from mysql.connector import errorcode

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
        print(os.getenv("DB_USERNAME"))
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
                
    def close(self):
        self.connection.close()