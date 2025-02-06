#email imports
from email.message import EmailMessage
import smtplib

#general imports
from dotenv import load_dotenv
import os

class appEmail:

    #Load environment variables from the .env file
    envVarPath="src/config/.env"
    load_dotenv(dotenv_path=envVarPath)

    #configure private environment variables for the sender account and sender password
    __defaultSenderAddr = os.getenv('DEF_EMAIL_ADDR')
    __defaultSenderAddrPass = os.getenv('DEF_EMAIL_ADDR_PASS')
 
    def __init__(self):
        self.mailserver = smtplib.SMTP('smtp.gmail.com',587)
        self.mailserver.starttls()
        self.mailserver.ehlo()
        self.mailserver.login(self.__defaultSenderAddr, self.__defaultSenderAddrPass)

    def sendEmail(self, destinationAddr, subject, content):
        try:
            self.message = EmailMessage()
            self.message.set_content(content)
            self.message['subject'] = subject
            self.message['to'] = destinationAddr
            self.message['from'] = self.__defaultSenderAddr

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.__defaultSenderAddr, self.__defaultSenderAddrPass)
            server.send_message(self.message)

            server.quit()

        except Exception as error:
            print(f"Error encountered when sending email: {error}")
            return False
 