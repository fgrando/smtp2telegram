#!/usr/bin/python3

import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SERVER="127.0.0.1" # machine running the smtp2telegram

def get_message(email_from, email_to, message):
    msg = MIMEMultipart("alternative")

    msg["From"] = email_from
    msg["To"] = ";".join(email_to)
    msg["Subject"] = r"notifysmtp"

    content = MIMEText(message)
    msg.attach(content)

    # current = os.path.dirname(__file__)
    # name = "send.py"
    # full_filename = os.path.join(dirname, name)

    # attach = MIMEText(open(full_filename, "rb").read(), "base64", "UTF-8")
    # attach['Content-Type'] = 'application/octet-stream'
    # attach['Content-Disposition'] = f'attachment; filename={name}'
    # msg.attach(attach)

    return msg


def send_mail(
    email_from,
    message,
    email_to=["nt@smtpnotify.py"],
    mail_host=SERVER,
    mail_port=1025,
):
    smtp = smtplib.SMTP()
    smtp.set_debuglevel(0)
    smtp.connect(mail_host, mail_port)
    msg = get_message(email_from, email_to, message)
    smtp.sendmail(email_from, email_to, msg.as_string())
    smtp.quit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} 'the desired message' 'from@email.com'")
        print(f"       {sys.argv[0]} 'another example msg' $(hostname)")
        exit(-1)

    msg = sys.argv[1]
    src = sys.argv[2]
    exit(send_mail(src, msg))
