from flask import Flask, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import time
import csv
import dotenv
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

dotenv.load_dotenv()

SENDER_EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

if not SENDER_EMAIL or not PASSWORD:
    print("Error: Email credentials are missing.")
    exit(1)

def add_text_to_certificate(name, regno):
    event_details = "{{For attending The Secure Way on 14th November 2024}}"
    template_path = 'certificate.png'
    output_folder = "certificates"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    img = Image.open(template_path)
    name_font_path = 'PlaylistScript.otf'
    name_font_size = 150
    event_font_size = 50
    event_font_path = 'arial.ttf'
    name_font = ImageFont.truetype(name_font_path, name_font_size)
    event_font = ImageFont.truetype(event_font_path, event_font_size)

    img_width, img_height = img.size
    draw = ImageDraw.Draw(img)
    
    name_bbox = draw.textbbox((0, 0), name, font=name_font)
    name_text_width = name_bbox[2] - name_bbox[0]
    name_text_height = name_bbox[3] - name_bbox[1]
    name_x = (img_width - name_text_width) / 2
    name_y = img_height / 2 - name_text_height / 2 + 30
    draw.text((name_x, name_y), name, font=name_font, fill="white")

    event_bbox = draw.textbbox((0, 0), event_details, font=event_font)
    event_text_width = event_bbox[2] - event_bbox[0]
    event_text_height = event_bbox[3] - event_bbox[1]
    event_x = (img_width - event_text_width) / 2
    event_y = name_y + name_text_height + 100
    draw.text((event_x, event_y), event_details, font=event_font, fill="white")

    output_path = os.path.join(output_folder, f"{regno}.pdf")
    img.save(output_path, "PDF", resolution=100.0)
    return output_path

def create_certificate():
    with open('users.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for user in reader:
            try:
                fullname = user['name']
                registration = user['regno']
                recipient_email = user['email']

                email_content = render_template('certificate_template.html', data=user)
                certificate_path = add_text_to_certificate(fullname, registration)

                send_certificate(recipient_email, "Certificate: The Secure Way by AWS Cloud Club LPU}", email_content, certificate_path)
                print(f"Email sent to {recipient_email}")
                time.sleep(3)
            except Exception as e:
                print(f"Failed to send email to {recipient_email}: {str(e)}")

    print("All emails sent successfully")

def send_certificate(to_email, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    with open(attachment_path, "rb") as attachment_file:
        attachment = MIMEApplication(attachment_file.read(), _subtype="pdf")
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
        msg.attach(attachment)

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
            print(f"Mail Server Started")
            create_certificate()
        except Exception as e:
            print(f"Error: {str(e)}")

