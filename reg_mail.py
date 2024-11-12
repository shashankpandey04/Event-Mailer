from flask import Flask, render_template
import csv
import dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import time

app = Flask(__name__)

dotenv.load_dotenv()

SENDER_EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

if not SENDER_EMAIL or not PASSWORD:
    print("Error: Email credentials are missing.")
    exit(1)

def create_emails():
    with open('users.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for user in reader:
            try:
                name = user['name']
                regno = user['regno']
                recipient_email = user['email']
                email_content = render_template('email_template.html', data=user)
                send_email(recipient_email, "Registration Confirmation: The Secure Way by AWS Cloud Club LPU", email_content)
                print(f"Email sent to {name} | {regno} at {recipient_email}")
            except:
                print(f"Failed to send email to {name} | {regno} at {recipient_email}")
                if not os.path.exists('error.csv'):
                    with open('error.csv', 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['name', 'regno', 'email'])
                with open('error.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([name, regno, recipient_email])
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
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")

if __name__ == '__main__':
    with app.app_context():
        try:
            print("Mail Server Started")
            print(create_emails())
        except Exception as e:
            print(f"Error: {str(e)}")
