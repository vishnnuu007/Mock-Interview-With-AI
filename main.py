from flask import*
from public import public
from admin import admin
from user import user

import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail
app=Flask(__name__)

app.secret_key='abcdef'

app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(user)
app.run(debug=True)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'hariharan0987pp@gmail.com'
app.config['MAIL_PASSWORD'] = 'rjcbcumvkpqynpep'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)