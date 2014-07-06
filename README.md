## About

A simple send E-mail script in pure Python, it is released under the MIT License.


## Usage

Create configuration file ~/.config/send_email.conf

    [main]
    smtp_host=smtp.gmail.com
    smtp_port=587
    username=xxx@gmail.com
    password=secret
    debug=0


Send email via CLI

    $ python send_email.py --to=somebody@gmail.com --subject=hello --body="world !"


Send emails in Python script


    #!/usr/bin/env python

    from send_email import do_send_email
    bcc_addrs = ['a@qq.com', 'b@qq.com', 'c@gmail.com']

    try:
        do_send_email(subject=u'test Bcc',
                      body='Your E-Mail address should not in To, or Cc and Bcc Field.',
                      to_addrs=['somebody@gmail.com'],
                      bcc_addrs=bcc_addrs)
    except Exception:
        import traceback
        traceback.print_exc(3, sys.stderr)