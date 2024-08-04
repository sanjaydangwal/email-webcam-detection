import smtplib
import imghdr
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()
SENDER = os.getenv("SENDER")
PASSWORD = os.getenv("PASSWORD")
RECIVER = os.getenv("RECIVER")


def send_email(image_path):
    print("send_email started!")
    email_message = EmailMessage()
    email_message["subject"] = "New object showed up!"
    email_message.set_content("Hey! We just saw a new object.")

    with open(image_path, 'rb') as file:
        content = file.read()

    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECIVER, email_message.as_string())
    gmail.quit()
    print("send_email ended!")


if __name__ == "__main__":
    send_email("Images/19.png")
