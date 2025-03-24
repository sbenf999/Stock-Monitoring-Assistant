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