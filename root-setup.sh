apt update
apt install git python3-pip
pip install --force-reinstall python-telegram-bot

gitdir=$(pwd)
cd /usr/bin/
ln -s $gitdir/smtp2telegram.py smtp2telegram

cd /etc/systemd/system
ln -s $gitdir/smtp2telegram.service .

cd $gitdir
systemctl start smtp2telegram
systemctl enable smtp2telegram
systemctl status smtp2telegram