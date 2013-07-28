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


Send email

    python send_email.py somebody@gmail.com subject body
