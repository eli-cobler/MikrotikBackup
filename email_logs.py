#
#  email_logs.py
#  MikrotikBackup
#
#  Created by Eli Cobler on 06/21/19.
#  Copyright © 2018 Eli Cobler. All rights reserved.
#
#  Mikrotikbackup is a tool used to backup all of our mikrotik routers.
#
#  This file will send out and email with the log files attached to the specified email receptiant.

import email, smtplib, ssl, os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = 'Mikrotik Backup Log Files'
body = 'Attached is all the log files for Mikrotik Backup'
sender_email = 'sparkappnotifications@gmail.com'
receiver_email = 'eli@sparkservices.net'
password = "rigzhubdkgwzbmva"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# Add body to email
message.attach(MIMEText(body, "plain"))

log_directory = os.listdir('logs/')

for log in log_directory:
    filename = os.path.join('logs/', log) # File to attach

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename.replace('logs','')}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()



# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)