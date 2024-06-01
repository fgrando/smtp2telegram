#!/bin/python3

import re
import sys
import subprocess
import asyncore
from smtpd import SMTPServer
import telegram

# Definitions
SMTP_SERVER_PORT = 1025
TELEGRAM_TOKEN = "0000000000:AAaaaAaAAAAAAAAAAAAA-AAAaaaaaaaaAAA"
TELEGRAM_CHAT_ID = 000000000


# get interface ip
def get_linux_ipv4():
    ips = []
    dump = subprocess.check_output(["ip", "addr"]).decode(errors="ignore")
    for ip in re.findall("(?<=inet )[\d]+\.[\d]+\.[\d]+\.[\d]+", dump):
        if ip.startswith("127."):
            continue
        ips.append(ip)
    return ips


# Telegram message
def send_message(msg):
    import asyncio

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    asyncio.run(bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg))


# SMTP server
class EmlServer(SMTPServer):
    def process_message(
        self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None
    ):
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        message = data.decode(errors="ignore")
        send_message(message)


def run(ip, port):
    print(f"{sys.argv[0]} serving at {ip}:{port}")
    srv = EmlServer((ip, port), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        server_ip = sys.argv[1]
    else:
        print("finding interface ip...")
        server_ip = get_linux_ipv4()[0]
    run(server_ip, SMTP_SERVER_PORT)
