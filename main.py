from flask import Flask, render_template
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import time

app = Flask(__name__)

SENDER_EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

@app.route('/send_emails')
def send_emails():
    with open('event_data.json', 'r') as file:
        users = json.load(file)
    for user in users:
        fullname = user['fullname']
        registration = user['registration']
        recipient_email = user['email']
        email_content = render_template('email_template.html', data=user)
        send_email(recipient_email, "The Secure Way Registration Confirmation", email_content)
        time.sleep(3)

    return "Emails sent successfully to all users."

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
