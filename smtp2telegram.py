#!/bin/python3

import os
import re
import sys
import html
import email
import subprocess
import asyncio
from aiosmtpd.controller import Controller
import telegram

# Definitions
SMTP_SERVER_PORT = 1025

# The .cred file contains the following variables
# TELEGRAM_TOKEN = "0000000000:AAaaaAaAAAAAAAAAAAAA-AAAaaaaaaaaAAA"
# TELEGRAM_CHAT_ID = 000000000
from mycredentials import *


# Get interface IP
def get_linux_ipv4():
    ips = []
    dump = subprocess.check_output(["ip", "addr"]).decode(errors="ignore")
    for ip in re.findall("(?<=inet )[\d]+\.[\d]+\.[\d]+\.[\d]+", dump):
        if ip.startswith("127."):
            continue
        ips.append(ip)
    return ips


# Cleanup email message
def cleanup_email(raw):
    message = email.message_from_bytes(raw)

    to = message.get("To")
    frm = message.get("From")
    sub = message.get("Subject").strip()
    date = message.get("Date")
    ctype = message.get("Content-Type")

    # By default consider body everything that is not mapped to keys
    body = raw.decode(errors="ignore").strip()
    for k in message.keys():
        body = body.replace(f"{k}: {message.get(k)}", "").strip()
    body = "raw payload:\n" + body

    # If it is multipart, get only the texts
    if message.is_multipart():
        for part in message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))
            if ctype == "text/plain" and "attachment" not in cdispo:
                body = part.get_payload().strip()
                break
    elif ctype is not None and ctype.startswith("text/plain"):
        body = "plain text:\n" + message.get_payload()
    elif ctype is not None and ctype.startswith("text/html"):
        body = html.unescape(message.get_payload())
        body = re.sub("<.*?>", "", body)
        body = "html text:\n" + body

    # Limit length of body
    if len(body) > 1240:
        body = body[:1000]
    return f"{frm} -> {to}\n{date}\n{sub}\n\n{body}"


# Telegram message
async def send_message(msg):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)


# SMTP handler class
class MyHandler:
    async def handle_DATA(self, server, session, envelope):
        message = cleanup_email(envelope.content)
        # Send the message asynchronously
        await send_message(message)
        return "250 Message accepted for delivery"


# Running the SMTP server
async def run(ip, port):
    print(f"{sys.argv[0]} serving at {ip}:{port}")

    handler = MyHandler()
    controller = Controller(handler, hostname=ip, port=port)
    controller.start()

    try:
        # Run the event loop indefinitely
        while True:
            await asyncio.sleep(3600)  # Keep server running
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        server_ip = sys.argv[1]
    else:
        print("Finding interface IP...")
        server_ip = get_linux_ipv4()[0]
    asyncio.run(run(server_ip, SMTP_SERVER_PORT))
