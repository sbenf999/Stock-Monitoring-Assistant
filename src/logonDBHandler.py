import mysql.connector
from mysql.connector import errorcode
import hashlib
import uuid


class logonDBHandler:
    __username = "root"
    __password = "BeltMadness3"
    __host = "192.168.0.142"
    __database = "nea"
    connection = ""
    cursor = ""

    def __init__(self):
        try:
            self.connection = mysql.connector.connect(user=self.__username,password=self.__password, host=self.__host, database=self.__database, auth_plugin='mysql_native_password') #auth_plugin='mysql_native_password' needed to be added to self.connection as this was throwing a cache error. Possible cause of issue on the school computers?
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

    def initializeDatabase(self):
        mycursor = self.connection.cursor()
        mycursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(50) PRIMARY KEY,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(64) NOT NULL,
                access_level VARCHAR(50) NOT NULL
            )
        ''')

        self.connection.commit()

    def createUserCreds(self, username, password, accessLevel):
        user_id = str(uuid.uuid4())
        mycursor = self.connection.cursor()

        mycursor.execute("""INSERT INTO users (id, username, password, access_level) VALUES ('%s', '%s', '%s', '%s')""" % (user_id,username, logonDBHandler.hashData(str(password)), accessLevel))

        self.connection.commit()

    def readUserCreds(self):
        mycursor = self.connection.cursor()
        mycursor.execute('SELECT id, username, password, access_level FROM users')
        rows = mycursor.fetchall()
        self.connection.close()
        
        return rows
    
    def validateUser(self, providedUsername, providedPassword):
        mycursor = self.connection.cursor()
        mycursor.execute('SELECT id, access_level FROM users WHERE username = ? AND password = ?', (logonDBHandler.hashData(providedUsername), logonDBHandler.hashData(providedPassword)))
        user = mycursor.fetchone()
        self.connection.close()
        
        return user
    
    #<=======================STATIC-METHODS=======================>#
    
    def hashData(data):
        return hashlib.sha256(str.encode(data)).hexdigest()
