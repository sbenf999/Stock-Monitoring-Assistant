import mysql.connector
from mysql.connector import errorcode

#overarching parent class for handling database connections. All child classes will serve a specific function
class DBHandler:
    __username = "root"
    __password = "BeltMadness3"
    __host = "192.168.0.142"
    __database = "nea"
    connection = ""
    cursor = ""

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user=self.__username,password=self.__password, host=self.__host, database=self.__database, auth_plugin='mysql_native_password') 
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