import mysql.connector
from mysql.connector import errorcode
import hashlib
import uuid
import string
import secrets
from popUpWindow import *

class logonDBHandler:
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

    def initializeDatabase(self):
        mycursor = self.connection.cursor()
        try:
            mycursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id VARCHAR(50) PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    password VARCHAR(64) NOT NULL,
                    access_level VARCHAR(50) NOT NULL,
                    recovery_code VARCHAR(100) NOT NULL         
                )
            ''')

            self.connection.commit()
        
        except Exception as error:
            return False

    def createUserCreds(self, username, password, accessLevel):
        user_id = str(uuid.uuid4())
        mycursor = self.connection.cursor()

        if self.validateUser(username, password):
            message = popUpWindow("User already exists")
            message.create()
            return False
        
        else:
            recoveryCode = self.createAccRecoveryCode()
            print(f"Recovery code: {recoveryCode}")
            message = popUpWindow(f"Recovery code: {recoveryCode}")
            message.create()
            try:
                mycursor.execute("""INSERT INTO users (user_id, username, password, access_level, recovery_code) VALUES ('%s', '%s', '%s', '%s', '%s')""" % (user_id,username, logonDBHandler.hashData(str(password)), accessLevel, logonDBHandler.hashData(str(recoveryCode))))
            except Exception as e:
                print(e)
        self.connection.commit()

    def readUserCreds(self):
        mycursor = self.connection.cursor()
        mycursor.execute('SELECT user_id, username, password, access_level FROM users')
        rows = mycursor.fetchall()
        self.connection.close()
        
        return rows
    
    def validateUser(self, providedUsername, providedPassword):
        mycursor = self.connection.cursor()
        mycursor.execute('SELECT user_id, access_level FROM users WHERE username = %s AND password = %s', (providedUsername, logonDBHandler.hashData(str(providedPassword))))
        data = mycursor.fetchone()
        print(data)
        if data:
            return True
        else:
            return False
        
    def changePasswordProcess(self, username, old_password, new_password):
        mycursor = self.connection.cursor()
        mycursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        current_password = mycursor.fetchall()

        if current_password is None:
            return False

        elif current_password[0][0] == logonDBHandler.hashData(str(old_password)):
            mycursor.execute('UPDATE users SET password = %s WHERE username = %s', (logonDBHandler.hashData(str(new_password)), username))
            self.connection.commit()
            
            return True
        
        else:
            return False
        
    def genTempPass(self):
        tempPass = ""
        for i in range (4):
            tempPass += secrets.choice(string.digits)
        
        return tempPass
    
    def changePasswordOutright(self, accountName, newPassword):
        mycursor = self.connection.cursor()
        mycursor.execute('UPDATE users SET password = %s WHERE username = %s', (logonDBHandler.hashData(str(newPassword)), accountName))
        self.connection.commit()

    def createAccRecoveryCode(self):
        recoveryCode = ""
        for i in range(3):
            recoveryCode += secrets.choice(string.ascii_uppercase)

        recoveryCode += "-"
        for i in range(3):
            recoveryCode += secrets.choice(string.digits)

        return recoveryCode

    def validateRecoveryCode(self, username, leftH, rightH):
        mycursor = self.connection.cursor()
        mycursor.execute('SELECT recovery_code FROM users WHERE username = %s', (username,))
        result = mycursor.fetchone()[0]

        recoveryCode = f"{leftH}-{rightH}"
        if logonDBHandler.hashData(str(recoveryCode)) == result:
            return True
        
        return False
    
    def getUserAccessLevel(self, username):
        mycursor = self.connection.cursor()
        mycursor.execute('SELECT access_level FROM users WHERE username = %s', (username,))
        result = mycursor.fetchone()[0]

        return result

    #<=======================STATIC-METHODS=======================>#
    
    def hashData(data):
        return hashlib.sha256(str.encode(data)).hexdigest()
