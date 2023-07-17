from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def create(to_address, subject, html_body):
    message = MIMEMultipart()
    message["To"] = to_address
    # Needed to make the email open in the editor
    message["X-Unsent"] = "1"
    message["Subject"] = subject
    message.attach(MIMEText(html_body, "html"))

    return message