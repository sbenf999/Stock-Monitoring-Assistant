import hashlib
import uuid
import sqlite3

class logonDBHandler:
    def __init__(self):
        pass
    
    def createUserCreds(username, password, accessLevel):
        username = username
        password = password
        accessLevel = accessLevel
        credFile = 'user_credentials.db'
        
        return [username, password, accessLevel, credFile]
    
    def hashData(data):
        return hashlib.sha256(str.encode(data)).hexdigest()
    
    def initializeDatabase():
        conn = sqlite3.connect('user_credentials.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                access_level TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def createUser(username, password, accessLevel):
        newUser = logonDBHandler.createUserCreds(username, password, accessLevel)
        logonDBHandler.initializeDatabase()
        
        conn = sqlite3.connect(newUser[3])
        cursor = conn.cursor()
        user_id = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO users (id, username, password, access_level) 
            VALUES (?, ?, ?, ?)
        ''', (logonDBHandler.hashData(str(user_id)), logonDBHandler.hashData(str(username)), logonDBHandler.hashData(str(password)), logonDBHandler.hashData(str(accessLevel))))
        conn.commit()
        conn.close()
        
        return user_id
    
    def readUserCreds():
        conn = sqlite3.connect('user_credentials.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password, access_level FROM users')
        rows = cursor.fetchall()
        conn.close()
        
        return rows
    
    def validateUser(providedUsername, providedPassword):
        conn = sqlite3.connect('user_credentials.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, access_level FROM users WHERE username = ? AND password = ?', (logonDBHandler.hashData(providedUsername), logonDBHandler.hashData(providedPassword)))
        user = cursor.fetchone()
        conn.close()
        
        return user