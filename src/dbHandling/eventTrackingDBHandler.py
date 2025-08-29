from dbHandling.DBHandler import *

class eventTrackingDBHandler(DBHandler):
    def initializeDatabase(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS eventTracking (
                    event_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    username VARCHAR(50),
                    eventName VARCHAR(200) NOT NULL,
                    date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );
            ''')

        except Exception as error:
            return False, error
        
    def logEvent(self, user_id, username, eventName):
        self.cursor.execute("""INSERT INTO eventTracking (user_id, username, eventName) VALUES (%s, %s, %s)""",(user_id, username, eventName))
        self.connection.commit()

    def filterDBCall(self, columnName):
        pass

