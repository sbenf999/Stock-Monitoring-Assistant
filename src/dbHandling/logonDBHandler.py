#database imports
import mysql.connector
from mysql.connector import errorcode

#general imports
import hashlib
import string
import secrets

#import proccesses and any db handlers
from processes.popUpWindow import *
from processes.sendEmail import *
from dbHandling.DBHandler import *

class logonDBHandler(DBHandler):
    def initializeDatabase(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT auto_increment PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    password VARCHAR(64) NOT NULL,
                    access_level VARCHAR(50) NOT NULL,
                    recovery_code VARCHAR(100) NOT NULL,
                    email_address VARCHAR(100) NOT NULL   
                )
            ''')

            self.connection.commit()
        
        except Exception as error:
            return False, error

    def createUserCreds(self, username, password, accessLevel, emailAddress):
        if self.validateUser(username, password):
            message = popUpWindow("User already exists")
            message.create()
            return False
        
        else:
            #create the account recovery code in case a user forgets their password and they need to reset it
            recoveryCode = self.createAccRecoveryCode()
            #create a pop-up window with the users recovery code as well as sending them an email containing it
            message = popUpWindow(f"Recovery code: {recoveryCode}")
            message.create()
            newEmail = appEmail()
            newEmail.sendEmai(emailAddress, "Recovery code for Onestop Stock Monitoring Assistant", f"Recovery code: {recoveryCode}") 
            
            try:
                #Use parameterized query for safety
                self.cursor.execute("""INSERT INTO users (username, password, access_level, recovery_code, email_address) VALUES (%s, %s, %s, %s, %s)""",(username,logonDBHandler.hashData(str(password)),accessLevel,logonDBHandler.hashData(str(recoveryCode)),emailAddress,))
                message = popUpWindow("User created successfully")

            except Exception as e:
                print(e)

        self.connection.commit()

    def readUserCreds(self):
        self.cursor.execute('SELECT user_id, username, password, access_level FROM users')
        rows = self.cursor.fetchall()
        self.connection.close()
        
        return rows
    
    def getUserNames(self, current=False):
        try:
            self.cursor.execute("SELECT username FROM users")
            results = self.cursor.fetchall()
            print(results)
            userNames = [row[0] for row in results]

            return userNames
        
        except Exception as error:
            return False, error

    def validateUser(self, providedUsername, providedPassword):
        try:
            hashedPassword = logonDBHandler.hashData(str(providedPassword))
            self.cursor.execute('SELECT user_id, access_level FROM users WHERE username = %s AND password = %s',(providedUsername, hashedPassword))
            data = self.cursor.fetchone()
            print(f"Query Result: {data}")  # Debugging output
            return bool(data)  # Return True if data is found, else False
        
        except Exception as e:
            print(f"Error during user validation: {e}")
            return False
        
    def changePasswordProcess(self, username, old_password, new_password):
        self.cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        current_password = self.cursor.fetchall()

        if current_password is None:
            return False

        elif current_password[0][0] == logonDBHandler.hashData(str(old_password)):
            self.cursor.execute('UPDATE users SET password = %s WHERE username = %s', (logonDBHandler.hashData(str(new_password)), username))
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
        self.cursor.execute('UPDATE users SET password = %s WHERE username = %s', (logonDBHandler.hashData(str(newPassword)), accountName))
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
        self.cursor.execute('SELECT recovery_code FROM users WHERE username = %s', (username,))
        result = self.cursor.fetchone()[0]

        recoveryCode = f"{leftH}-{rightH}"
        if logonDBHandler.hashData(str(recoveryCode)) == result:
            return True
        
        return False
    
    def getUserAccessLevel(self, username):
        self.cursor.execute('SELECT access_level FROM users WHERE username = %s', (username,))
        result = self.cursor.fetchone()[0]

        return result

    #<=======================STATIC-METHODS=======================>#
    
    def hashData(data):
        return hashlib.sha256(str.encode(data)).hexdigest()
    
