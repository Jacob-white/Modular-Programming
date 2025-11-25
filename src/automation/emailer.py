import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..core.logger import logger

class Emailer:
    """
    Simple SMTP emailer.
    """
    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str, sender_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_email(self, to_email: str, subject: str, body: str, is_html: bool = False):
        """
        Sends an email.
        """
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'html' if is_html else 'plain'))

            # In a real scenario, use context manager and handle TLS
            # server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            # server.starttls()
            # server.login(self.sender_email, self.sender_password)
            # server.send_message(msg)
            # server.quit()
            
            logger.info(f"Mock email sent to {to_email} with subject: {subject}")
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise
