import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from config import *


def mail(target_mail, file=""):
    server = smtplib.SMTP(SMTP_SERVER, 587)  # Hotmail uses this server and port
    server.ehlo()
    server.starttls()
    try:
        server.login(SERVICE_MAIL, SERVICE_PASSWORD)
    except smtplib.SMTPAuthenticationError as e:
        print("Could not log in.")
        print(e.smtp_error)
        return
    message = create_email_message(SUBJECT, CONTENT, SERVICE_MAIL, target_mail, file)
    try:
        server.sendmail(SERVICE_MAIL, target_mail, message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()


def create_email_message(
    subject: str,
    content: str,
    sender_email: str,
    recipient_email: str,
    file_attachment: str,
):
    # format content
    content = content.replace("%time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Create a MIMEText object
    mime_message = MIMEMultipart()
    mime_message["Subject"] = subject
    mime_message["From"] = sender_email
    mime_message["To"] = recipient_email
    mime_message.attach(MIMEText(content, "plain"))

    try:
        with open(file_attachment, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=basename(file_attachment))
        part["Content-Disposition"] = 'attachment; filename="%s"' % basename(
            file_attachment
        )
        mime_message.attach(part)
    except FileNotFoundError:
        print("Attachment not found")

    return mime_message.as_string()


if __name__ == "__main__":
    mail("272632@student.pwr.edu.pl")
