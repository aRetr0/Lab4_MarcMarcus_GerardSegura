# b64encoder.py
def base64_encoder(data):
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    encoded_str = ""

    # Convert original data to binary
    binary_str = ''.join(f"{byte:08b}" for byte in data)

    # Divide binary data into 6-bit groups
    padding_length = (6 - len(binary_str) % 6) % 6
    binary_str = binary_str.ljust(len(binary_str) + padding_length, '0')

    # Convert 6-bit groups to Base64 characters
    for i in range(0, len(binary_str), 6):
        six_bit_group = binary_str[i:i+6]
        encoded_str += base64_chars[int(six_bit_group, 2)]

    # Add padding if necessary
    padding = '=' * (len(data) % 3)
    encoded_str += padding

    return encoded_str

# Example usage
if __name__ == "__main__":
    with open("decoded_image.png", "rb") as file:
        image_data = file.read()
    encoded_image = base64_encoder(image_data)
    with open("image.txt", "w") as f:
        f.write(encoded_image)