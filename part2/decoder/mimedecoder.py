# mimedecoder.py
import os
from part1.b64decoder import base64_decoder

def parse_headers(headers_section: str) -> dict:
    """
    Parse the headers section of a MIME message and return a dictionary of headers.
    :param headers_section:
    :return:
    """
    headers = {}
    for line in headers_section.split('\n'):
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key] = value
    return headers

def extract_boundary(content_type: str) -> str:
    """
    Extract the boundary string from the Content-Type header.
    :param content_type:
    :return:
    """
    boundary_prefix = 'boundary="'
    start = content_type.find(boundary_prefix) + len(boundary_prefix)
    end = content_type.find('"', start)
    return content_type[start:end]

def decode_mime_message(file_path: str) -> None:
    """
    Decode a MIME message and save the decoded body and attachments to files.
    :param file_path:
    :return:
    """
    with open(file_path, 'r') as file:
        content = file.read()

    # Split header and body sections
    headers_section, body_section = content.split('\n\n', 1)
    headers = parse_headers(headers_section)

    # Save headers to header.txt
    os.makedirs('decoder', exist_ok=True)
    with open('decoder/header.txt', 'w') as header_file:
        for key, value in headers.items():
            header_file.write(f"{key}: {value}\n")

    # Identify boundary in the Content-Type header
    boundary = extract_boundary(headers.get('Content-Type', ''))

    # Split the body into parts using the boundary
    parts = body_section.split(f'--{boundary}')

    for part in parts:
        if part.strip() == '--' or not part.strip():
            continue

        part_headers_section, part_body = part.split('\n\n', 1)
        part_headers = parse_headers(part_headers_section)

        content_disposition = part_headers.get('Content-Disposition', '')
        content_transfer_encoding = part_headers.get('Content-Transfer-Encoding', '').lower()

        if 'attachment' in content_disposition:
            filename_prefix = 'filename="'
            start = content_disposition.find(filename_prefix) + len(filename_prefix)
            end = content_disposition.find('"', start)
            filename = content_disposition[start:end]

            if content_transfer_encoding == 'base64':
                decoded_data = base64_decoder(part_body)
            else:
                decoded_data = part_body.encode()

            with open(f'decoder/{filename}', 'wb') as attachment_file:
                attachment_file.write(decoded_data)
        else:
            if content_transfer_encoding == 'base64':
                decoded_data = base64_decoder(part_body).decode()
            else:
                decoded_data = part_body

            with open('decoder/body.txt', 'w') as body_file:
                body_file.write(decoded_data)

if __name__ == "__main__":
    decode_mime_message('mimemail.txt')