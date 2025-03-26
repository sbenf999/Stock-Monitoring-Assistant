from dbHandling.DBHandler import *
import json

class weeklyReportDBHandler(DBHandler):
    def initializeDatabase(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS weeklyReportRecords (
                    weekly_report_record_id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT, 
                    trend VARCHAR(100) NOT NULL,
                    predicted JSON,
                    revenue DECIMAL(10,2) NOT NULL,
                    cost_of_goods_sold DECIMAL(10,2) NOT NULL,
                    net_profit DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (product_id) REFERENCES products(product_ID)
                )
            ''')

        except Exception as error:
            return False, error
        
    
    def addWeeklyReportRecord(self, productID, trend, predicted, revenue, cogs, netProfit):
        try:
            if isinstance(predicted, dict):
                predicted = json.dumps(predicted)

            params = (productID, trend, predicted, revenue, cogs, netProfit)

            self.cursor.execute('''INSERT INTO weeklyreportrecords (product_id, trend, predicted, revenue, cost_of_goods_sold, net_profit) VALUES (%s, %s, %s, %s, %s, %s)''', params)
            self.connection.commit()

        except Exception as error:
            self.connection.rollback()
            print(f"sldb: {error}")
            return False, error
        
    def getWeeklyReportsAsList(self):
        try:
            self.cursor.execute("SELECT * FROM weeklyreportrecords")
            dataToUse = self.cursor.fetchall()
            self.connection.commit()

            groupedRecordIDs = []
            for record in dataToUse:
                if len(groupedRecordIDs) == 0:
                    groupedRecordIDs.append([record[2].strftime("%d/%m/%Y"), record[0]])

                else:
                    count = 0
                    for prevRecord in groupedRecordIDs:
                        if record[2].strftime("%d/%m/%Y") == prevRecord[0]:
                            count += 1
                            prevRecord.append(record[0])

                    if count == 0:
                        groupedRecordIDs.append([record[2].strftime("%d/%m/%Y"), record[0]])

            return groupedRecordIDs

        except Exception as error:
            self.connection.rollback()
            print(f"wrdb: {error}")
            return False, error