# mimeencoder.py
import os
import quopri
import random
import string

from part1.b64encoder import base64_encoder


def generate_boundary(length: int = 30) -> str:
    """
    Generate a random boundary string.
    :param length:
    :return:
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def build_mime_message(from_addr: str,
                       to_addr: str,
                       cc_addr: str,
                       subject: str,
                       body_text: str,
                       attachments: list[str]) -> str:
    """
    Build a MIME message with the provided parameters.
    :param from_addr:
    :param to_addr:
    :param cc_addr:
    :param subject:
    :param body_text:
    :param attachments:
    :return:
    """
    boundary = generate_boundary()
    mime_message = []

    # Add main headers
    mime_message.append(f"From: {from_addr}")
    mime_message.append(f"To: {to_addr}")
    mime_message.append(f"CC: {cc_addr}")
    mime_message.append(f"Subject: {subject}")
    mime_message.append(f"Content-Type: multipart/mixed; boundary=\"{boundary}\"")
    mime_message.append("")

    # Add the body text
    mime_message.append(f"--{boundary}")
    mime_message.append("Content-Type: text/plain; charset=UTF-8")
    mime_message.append("Content-Transfer-Encoding: quoted-printable")
    mime_message.append("")
    mime_message.append(quopri.encodestring(body_text.encode()).decode())
    mime_message.append("")

    # Process each attachment
    for attachment in attachments:
        filename = os.path.basename(attachment)
        with open(attachment, "rb") as file:
            file_content = file.read()
        encoded_content = base64_encoder(file_content)

        mime_message.append(f"--{boundary}")
        mime_message.append(f"Content-Type: application/octet-stream; name=\"{filename}\"")
        mime_message.append(f"Content-Disposition: attachment; filename=\"{filename}\"")
        mime_message.append("Content-Transfer-Encoding: base64")
        mime_message.append("")
        mime_message.append(encoded_content)
        mime_message.append("")

    # Final boundary
    mime_message.append(f"--{boundary}--")
    mime_message.append("")

    return "\n".join(mime_message)


def main():
    from_addr = "smpt2go@tecno-campus.cat"
    to_addr = "gseguraa@edu.tecnocampus.cat"
    cc_addr = "mmarcusm@edu.tecnocampus.cat"
    subject = "Subject of the email"

    # Read body text
    with open("body.txt", "r") as body_file:
        body_text = body_file.read()

    # List all attachments
    attachments_dir = "attachments"
    attachments = [os.path.join(attachments_dir, f) for f in os.listdir(attachments_dir) if
                   os.path.isfile(os.path.join(attachments_dir, f))]

    # Build MIME message
    mime_message = build_mime_message(from_addr, to_addr, cc_addr, subject, body_text, attachments)

    # Save to mimemail.txt
    with open("mimemail.txt", "w") as mime_file:
        mime_file.write(mime_message)


if __name__ == "__main__":
    main()