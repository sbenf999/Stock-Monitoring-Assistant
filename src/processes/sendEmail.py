#email imports
import smtplib
import email
from email.mime.text import MIMEText
import smtplib,email,email.encoders,email.mime.text,email.mime.base
from email.mime.multipart import MIMEMultipart

#general imports
from dotenv import load_dotenv
import os

class appEmail:

    # Load environment variables from the .env file
    envVarPath="src/config/.env"
    load_dotenv(dotenv_path=envVarPath)

    __defaultSenderAddr = os.getenv('DEF_EMAIL_ADDR')
    __defaultSenderAddrPass = os.getenv('DEF_EMAIL_ADDR_PASS')
 
    def __init__(self):
        self.mailserver = smtplib.SMTP('smtp.gmail.com',587)
        self.mailserver.starttls()
        self.mailserver.ehlo()
        self.mailserver.login(self.__defaultSenderAddr, self.__defaultSenderAddrPass)

    def sendEmai(self, destinationAddr, subject, content):
        try:
            self.message = MIMEMultipart()
            self.message['From'] = self.__defaultSenderAddr
            self.message['To'] = destinationAddr
            self.message['Subject'] = subject
            message = content
            self.message.attach(MIMEText(message))

            self.mailserver.sendmail('from','to',self.message.as_string())

        except Exception as error:
            print(f"Error encountered when sending email: {error}")
            return False