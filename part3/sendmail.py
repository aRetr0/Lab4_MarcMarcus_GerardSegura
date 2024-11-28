# sendmail.py
import os
import smtplib
from email import message_from_file

from part2.encoder.mimeencoder import build_mime_message


def send_email():
    # Set up SMTP server configuration and credentials
    smtp_server = "smtp.smtp2go.com"
    smtp_port = 2525
    smtp_user = "tecnocampus"
    smtp_password = "Fx5eff49VgoynPtj"

    from_addr = "sender@example.com"
    to_addr = "recipient@example.com"
    cc_addr = "cc@example.com"
    subject = "Subject of the email"

    # Read body text
    with open("body.txt", "r") as body_file:
        body_text = body_file.read()

    # List all attachments
    attachments_dir = "attachments"
    attachments = [os.path.join(attachments_dir, f) for f in os.listdir(attachments_dir) if
                   os.path.isfile(os.path.join(attachments_dir, f))]

    # List all inline images
    inline_images_dir = "inline_images"
    inline_images = [os.path.join(inline_images_dir, f) for f in os.listdir(inline_images_dir) if
                     os.path.isfile(os.path.join(inline_images_dir, f))]

    # Build MIME message
    mime_message_str = build_mime_message(from_addr, to_addr, cc_addr, subject, body_text, attachments, inline_images)

    # Save MIME message to file
    with open("mimemail.txt", "w") as mime_file:
        mime_file.write(mime_message_str)

    # Load the MIME file
    with open("mimemail.txt", "r") as mime_file:
        mime_message = message_from_file(mime_file)

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            # Send the email
            server.send_message(mime_message)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    send_email()
