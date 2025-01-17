import smtplib
import email
from email.mime.text import MIMEText
import smtplib,email,email.encoders,email.mime.text,email.mime.base
from email.mime.multipart import MIMEMultipart

class email:
    __defaultSenderAddr = "stockmonitoringassistant@gmail.com"
    __defaultSenderAddrPass = "ytav hxke tgqf ofel"
 
    def __init__(self):
        self.mailserver = smtplib.SMTP('smtp.gmail.com',587)
        self.mailserver.starttls()
        self.mailserver.ehlo()
        self.mailserver.login(self.__defaultSenderAddr, self.__defaultSenderAddrPass)

    def sendEmai(self, destinationAddr, subject, content):
        self.message = MIMEMultipart()
        self.message['From'] = self.__defaultSenderAddr
        self.message['To'] = destinationAddr
        self.message['Subject'] = subject
        message = content
        self.message.attach(MIMEText(message))

        self.mailserver.sendmail('from','to',self.message.as_string())
