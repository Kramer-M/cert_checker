# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.
# Create a text/plain message
def sendMail(recipient, textbody):
    msg = EmailMessage()
    msg.set_content(textbody)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = "Certificate Warning"
    msg['From'] = "manuel.kramer01@sap.com"
    msg['To'] = recipient

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

sendMail("manuel.kramer01@sap.com", "Test")