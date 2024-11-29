# sendmail.py
import smtplib
from email import message_from_file


def send_email():
    # Set up SMTP server configuration and credentials
    smtp_server = "smtp.smtp2go.com"
    smtp_port = 2525
    smtp_user = "tecnocampus"
    smtp_password = "Fx5eff49VgoynPtj"

    # Load the MIME file
    mime_file_path = "mimemail.txt"
    with open(mime_file_path, "r") as mime_file:
        mime_message = message_from_file(mime_file)

    try:
        # Connect to the SMTP server and send the e-mail
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(mime_message)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    send_email()
