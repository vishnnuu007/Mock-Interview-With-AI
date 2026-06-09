from flask import Blueprint, request, render_template, url_for, session
from flask_mail import Mail, Message
import os
import uuid
from face_model import *

# Assuming these are defined in database.py
from database import *

public = Blueprint('public', __name__)

# Flask-Mail configuration (initialized in main app)
mail = Mail()

@public.route("/")
def home():
    return render_template('home.html')

import random
from flask import session, request, render_template, redirect, url_for, flash
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Your existing email function modified to send OTP
def send_otp_email(to_email, otp):
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('hariharan0987pp@gmail.com', 'rjcbcumvkpqynpep')

        msg = MIMEMultipart()
        msg['From'] = 'hariharan0987pp@gmail.com'
        msg['To'] = to_email
        msg['Subject'] = 'Password Reset OTP'

        body = f"""
        Hello,

        You have requested to reset your password. Please use the following OTP to verify your identity:

        OTP: {otp}

        This OTP is valid for 10 minutes. If you did not request this reset, please ignore this email.

        Best regards,
        Your Team
        """
        msg.attach(MIMEText(body, 'plain'))

        gmail.send_message(msg)
        gmail.quit()
        print("OTP email sent successfully")
        return True

    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
        return False

# Generate a 6-digit OTP
def generate_otp():
    return ''.join(random.choices('0123456789', k=6))

@public.route("/fp", methods=['GET', 'POST'])
def fp():
    if request.method == 'POST':
        if 'submit' in request.form:
            email = request.form['email']
            uname = request.form['uname']

            # Check if user exists
            z = "SELECT * FROM user INNER JOIN login USING(login_id) WHERE username='%s' AND email='%s'" % (uname, email)
            rr = select(z)
            
            if rr:
                # Store user login_id in session
                session['id'] = rr[0]['login_id']
                
                # Generate OTP
                otp = generate_otp()
                
                # Store OTP in session for verification
                session['otp'] = otp
                session['email'] = email
                
                # Send OTP via email
                send_result = send_otp_email(email, otp)
                
                if send_result:
                    # Redirect to OTP verification page
                    return redirect(url_for('public.verify_otp'))
                else:
                    flash("Failed to send OTP email. Please try again.")
            else:
                flash("Invalid username or email. Please try again.")
        
    return render_template('forgetpassword.html')

@public.route("/verify-otp", methods=['GET', 'POST'])
def verify_otp():
    if 'id' not in session or 'otp' not in session:
        return redirect(url_for('public.fp'))
        
    if request.method == 'POST':
        user_otp = request.form.get('otp')
        
        # Check if OTP matches
        if user_otp == session['otp']:
            # OTP verified, clear it from session
            session.pop('otp', None)
            
            # Redirect to password reset page
            return redirect(url_for('public.cp'))
        else:
            flash("Invalid OTP. Please try again.")
            
    return render_template('verify_otp.html', email=session.get('email'))

@public.route("/cp", methods=['GET', 'POST'])
def cp():
    if 'id' not in session:
        return redirect(url_for('public.fp'))
        
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password == confirm_password:
            # Update password in database
            login_id = session['id']
            update_query = "UPDATE login SET password='%s' WHERE login_id='%s'" % (new_password, login_id)
            update(update_query)
            
            # Clear session data
            session.pop('id', None)
            session.pop('email', None)
            
            flash("Password updated successfully. Please login with your new password.")
            return redirect(url_for('public.login'))
        else:
            flash("Passwords do not match. Please try again.")
        
    return render_template('confirmpassword.html')

@public.route("/login", methods=['POST', 'GET'])
def login():
    if 'submit' in request.form:
        username = request.form['uname']
        password = request.form['password']
        print(username, password)
        qry = "select * from login where username='%s' and password='%s'" % (username, password)
        res = select(qry)
        print(res)
        if res:
            session['log'] = res[0]['login_id']
            if res[0]['usertype'] == 'admin':
                return '''<script>alert("Login Successfully");window.location="/admin_home"</script>'''    
            if res[0]['usertype'] == 'user':
                qry1 = "select * from user where login_id='%s'" % (session['log'])
                res1 = select(qry1)
                print(res1)
                if res1:
                    session['user'] = res1[0]['User_id']
                    session['name'] =res1[0]['fname']
                return '''<script>alert("Login Successfully");window.location="/user_home"</script>''' 
            else:
                return """<script>alert('Invalid User');window.location="/login"</script>"""


        else:
            return """<script>alert('Invalid User');window.location="/login"</script>"""

    return render_template('login.html')

from flask_mail import Mail, Message
import random
import string
import smtplib
from email.mime.text import MIMEText

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(to_email,fname,lname,uname,psw):
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('hariharan0987pp@gmail.com', 'rjcbcumvkpqynpep')

        msg = MIMEMultipart()
        msg['From'] = 'hariharan0987pp@gmail.com'
        msg['To'] = to_email
        msg['Subject'] = 'Welcome! Your Registration Credentials"'

        body=f"""
                Hello {fname} {lname},

                Thank you for registering with us! Below are your login credentials:

                Username: {uname}
                Password: {psw}


                Best regards,
                Your Team
                """
        msg.attach(MIMEText(body, 'plain'))

        gmail.send_message(msg)
        gmail.quit()
        print("Email sent successfully")

    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
        raise

@public.route('/registration', methods=['post', 'get'])
def registration():
    if 'submit' in request.form:
        fname = request.form['fname'] 
        lname = request.form['lname']
        place = request.form['place']
        phone = request.form['phone']
        email = request.form['email']
        uname = request.form['uname']
        psw = request.form['psw']

        c="select * from login where username='%s'"%(uname)
        v=select(c)

        h="select * from user where email='%s'"%(email)
        n=select(h)

        if v:
            return """<script>alert('Username already exist');window.location="/registration"</script>"""
        
        elif n:
            return """<script>alert('Email already exist');window.location="/registration"</script>"""

    
        
        else:


            a = "insert into login values(null,'%s','%s','user')" % (uname, psw)
            id = insert(a)

            z = "insert into user values(null,'%s','%s','%s','%s','%s','%s')" % (id, fname, lname, place, phone, email)
            reg = insert(z)

            pid = str(reg)
            isFile = os.path.isdir("static/trainimages/" + pid)  
            print(isFile)
            if not isFile:
                os.mkdir('static\\trainimages\\' + pid)
            
            image1 = request.files['img1']
            path = "static/trainimages/" + pid + "/" + str(uuid.uuid4()) + image1.filename
            image1.save(path)

            image2 = request.files['img2']
            path = "static/trainimages/" + pid + "/" + str(uuid.uuid4()) + image2.filename
            image2.save(path)

            image3 = request.files['img3']
            path = "static/trainimages/" + pid + "/" + str(uuid.uuid4()) + image3.filename
            image3.save(path)
            
            enf("static/trainimages/")

            # Send email with credentials
            try:
                send_email(email,fname,lname,uname,psw)
                print("Email sent successfully")
            except Exception as e:
                print(f"Failed to send email: {e}")

            return render_template('registration.html', success=True, login_url=url_for('public.login'))
        
    return render_template('registration.html', success=False, login_url=url_for('public.login'))