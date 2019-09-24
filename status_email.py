import smtplib, ssl, database
from html3 import html3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

router_list = database.get()
routers = []
for item in router_list:
    data = item.split(':')
    routers.append(data[0])

routers_dict = {}
for item in router_list:
    data = item.split(':')
    routers_dict[data[0]] = [data[1], data[2], data[3], data[4], data[5], data[6]]

port = 587  # For starttls
smtp_server = "smtp.office365.com"
sender_email = "eli@sparkservices.net"
receiver_email = "support@sparkservices.net"
password = ("Con31055")

message = MIMEMultipart("alternative")
message["Subject"] = "Mikrotik Backup Status Update"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
This is an Status update for Mikrotik Backup"""

h = html3.HTML()
t = h.table()
t.th("Name")
t.th("IP Address")
t.th("Backup Status")
t.th("Config Status")
t.th("Last Attempted Backup")
for k, v in routers_dict.items():
    r = t.tr(align='left')
    r.td(k)
    r.td(v[0])
    r.td(v[3])
    r.td(v[4])
    r.td(v[5])
#print(t)

html = str(t)

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")
#part3 = MIMEText(html2, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP("smtp.office365.com", 587) as server:
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
