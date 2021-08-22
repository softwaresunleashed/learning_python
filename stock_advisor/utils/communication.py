
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64

# Project specific imports
from config.config import *


########################
# Communication - Email
########################
def sendemail(stock, message):
    user = "stockadvisor.noreply@gmail.com"
    password = "9211hacker"
    to = ["stockadvisor.noreply@gmail.com"]
    subject = "Stock Alert!"
    message = message
    path = ROOT_PATH_CHART
    file = path + str(stock) + '.png'

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.starttls()

    gmail.login(user, password)
    gmail.set_debuglevel(1)

    header = MIMEMultipart()
    header['Subject'] = subject
    header['From'] = user
    header['To'] = ', '.join(to)

    message = MIMEText(message, 'plain')
    header.attach(message)

    if (os.path.isfile(file)):
        attch = MIMEBase('application', 'octet-stream')
        attch.set_payload(open(file, 'rb').read())
        encode_base64(attch)
        attch.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        header.attach(attch)

    gmail.sendmail(user, to, header.as_string())
    gmail.quit()
    print('OK!')
