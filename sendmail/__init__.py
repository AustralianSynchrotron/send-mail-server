from flask import Flask
from flask_mail import Mail


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'mail.synchrotron.org.au'
app.config['MAIL_PORT'] = 587
# app.config['MAIL_DEFAULT_SENDER'] = 'email_robot@synchrotron.org.au'
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['TESTING'] = False
mail = Mail(app)

import sendmail.views
