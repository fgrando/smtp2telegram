# smtp2telegram
Simple SMTP bridge to Telegram using python.


## Dependencies
Python 3.x and some pip packages are needed:

	sudo apt install python3-pip
	pip install --force-reinstall python-telegram-bot

(ensure no other telegram packages are installed)


## Install
Add the following to `/etc/systemd/system/smtp2telegram.service`:

	[Unit]
	Description=SMTP bridge to Telegram

	[Service]
	ExecStart=/usr/bin/smtp2telegram.py

	[Install]
	WantedBy=multi-user.target

## Usage
	/usr/bin/smtp2telegram.py 192.168.1.10
If the interface ip is not provided, the script will get the first interface ip found.

SMTP will be serving at the provided/found IP and port `1025`.No authentication or encryption is used.

Edit the following variables inside the script to provide telegram bot id and chat id:
- TELEGRAM_TOKEN = `"0000000000:AAaaaAaAAAAAAAAAAAAA-AAAaaaaaaaaAAA"`
- TELEGRAM_CHAT_ID = `000000000`

## Example
- login message:

	/usr/bin/smtpnotify "$(hostname) new login $(w)" "$(hostname)"

