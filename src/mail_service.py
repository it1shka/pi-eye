"""
Module responsible
for handling emails
in case of intruder detection
"""

from __future__ import annotations
import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import config


class MailServer:
    """
    Class that:
    1. Handles creation and auth to SMTP server
    2. Dispatch of emails
    """

    def __init__(self) -> None:
        """
        Creates SMTP server
        and tries to authenticate
        """
        self._server = smtplib.SMTP(
            config.EmailConfig.SMTP_SERVER, config.EmailConfig.SMTP_SERVER_PORT
        )
        self._server.ehlo_or_helo_if_needed()
        self._server.starttls()
        self._server.login(
            config.EmailConfig.SERVICE_MAIL, config.EmailConfig.SERVICE_PASSWORD
        )

    def __enter__(self) -> MailServer:
        """Acquiring from `with`"""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Exiting `with`"""
        self.stop()

    def stop(self) -> None:
        """Explicitly stopping the server"""
        self._server.quit()

    def _create_email(
        self,
        subject: str,
        content: str,
        sender_email: str,
        recipient_email: str,
        file_attachment: str,
    ) -> None:
        """
        General function
        for composing emails
        """
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg.attach(MIMEText(content, "plain"))
        try:
            with open(file_attachment, "rb") as attachment:
                attachment_content = attachment.read()
                attachment_name = os.path.basename(file_attachment)
                part = MIMEApplication(attachment_content, Name=attachment_name)
                part["Content-Disposition"] = (
                    f'attachment; filename="{attachment_name}"'
                )
                msg.attach(part)
        except FileNotFoundError:
            print("Attachment not found")
        str_message = msg.as_string()
        self._server.sendmail(sender_email, recipient_email, str_message)

    def dispatch_emails(self, image_path: str) -> None:
        """
        Preconfigured function that
        sends emails to all owners
        with image of intruder
        """
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = config.EmailConfig.CONTENT % stamp
        for user_email in config.EmailConfig.USER_EMAILS:
            try:
                self._create_email(
                    subject=config.EmailConfig.SUBJECT,
                    content=content,
                    sender_email=config.EmailConfig.SERVICE_MAIL,
                    recipient_email=user_email,
                    file_attachment=image_path,
                )
            except smtplib.SMTPException:
                print(f"Failed to send email to {user_email}")
