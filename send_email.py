#!/usr/bin/env python
#-*- coding:utf-8 -*-
import ConfigParser
from email.MIMEText import MIMEText
from email.Header import Header
from email.MIMEMultipart import MIMEMultipart
import os

import sys
import smtplib


def do_send_email(subject, body, to_addrs=None, cc_addrs=None, bcc_addrs=None):
    assert (to_addrs or cc_addrs or bcc_addrs)
    if not to_addrs: to_addrs = []
    if not cc_addrs: cc_addrs = []
    if not bcc_addrs: bcc_addrs = []

    config_in_d = get_config_in_d()

    smtp = smtplib.SMTP()

    if config_in_d['debug']:
        smtp.set_debuglevel(1)

    code, msg = smtp.connect(host=config_in_d['smtp_host'], port=config_in_d['smtp_port'])
    assert code == 220

    code, msg = smtp.ehlo()
    assert code == 250

    code, msg = smtp.starttls()
    assert code == 220

    code, msg = smtp.login(user=config_in_d['username'], password=config_in_d['password'])
    assert code == 235

    msg = MIMEMultipart()
    text = MIMEText(body, "html", "utf-8")
    msg.attach(text)

    msg["From"] = config_in_d['username']
    if to_addrs:
        msg["To"] = ",".join(to_addrs)
    if cc_addrs:
        msg["Cc"] = ",".join(cc_addrs)
    if bcc_addrs:
        msg["Bcc"] = ",".join(bcc_addrs)
    msg["Subject"] = Header(subject, "utf-8")
    print 'to_addrs', type(to_addrs), to_addrs
    smtp.sendmail(from_addr=config_in_d['username'], to_addrs=to_addrs, msg=msg.as_string())
    smtp.quit()

def send_email(to_addrs, subject, body):
    try:
        do_send_email(subject=subject, body=body, to_addrs=to_addrs)
        return 0
    except Exception:
        import traceback
        traceback.print_exc(3, sys.stderr)
        return -1

def get_config_in_d():
    config_full_path = os.path.expanduser("~/.config/send_email.conf")
    config = ConfigParser.ConfigParser()
    config.read(config_full_path)
    return dict(
        smtp_host = config.get('main', 'smtp_host'),
        smtp_port = config.get('main', 'smtp_port'),
        username = config.get('main', 'username'),
        password = config.get('main', 'password'),
        debug = config.getint('main', 'debug'),
    )


def test_send_email():
    subject = u"又挂了"
    body = u"又挂了"
    send_email(to_addrs=['bot@example.com'],
        subject=subject,
        body=body)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog=sys.argv[0])

    parser.add_argument('--to', required=True, help='split string by ","')
    # parser.add_argument('--cc', help='split string by ","')
    # parser.add_argument('--bcc', help='split string by ","')
    parser.add_argument('--subject', required=True)
    parser.add_argument('--body', required=True)

    args = parser.parse_args()

    to_addrs = args.to.strip().split(',')
    exit(send_email(to_addrs=to_addrs, subject=args.subject, body=args.body))
        
    
