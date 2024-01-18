
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from configparser import ConfigParser
from pathlib import Path

class EmailSender:
    def __init__(self):

        self.password = "kflgcpmpemzuprth" # App password
        self.email = "notificacioclient@gmail.com"
        self.server = smtplib.SMTP("smtp.gmail.com", 587)

    def send_email(self, receiver_email, subject, message):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)

            msg = MIMEMultipart()
            msg.attach(MIMEText(message, 'txt', 'utf-8'))  # Puesto en formato html, se puede cambiar también a txt
            msg["Subject"] = Header(subject, 'utf-8')
            msg["From"] = self.email
            msg["To"] = receiver_email

            server.sendmail(self.email, receiver_email, msg.as_string())
            print("Email has been sent successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            server.quit()

# Uso de la classe
if __name__ == "__main__":
    email_sender_ = EmailSender()
    email_sender_.send_email("paumat17@gmail.com", "Hello! This is a cool test sending an email! LOL I'm Pau","this is the fucking message that i have to send to Marc!")
    print("Email has been sent to " + email_sender_.email)