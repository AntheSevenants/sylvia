from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def create(to_address, subject, html_body):
    """Generate an EML containing the chosen calendar

    Args:
        to_address (str): To email address to be pre-filled
        subject (str): subject to be pre-filled
        html_body (str): HTML content of the email

    Returns:
        str: EML email (could be base64 encoded!)
    """

    message = MIMEText(html_body, "html", _charset='UTF-8')
    message["To"] = to_address
    # Needed to make the email open in the editor
    message["X-Unsent"] = "1"
    message["Subject"] = subject

    return message.as_string()