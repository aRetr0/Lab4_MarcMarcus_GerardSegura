# b64decoder.py
def base64_decoder(encoded_str):
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    decoded_bytes = bytearray()

    # Clean the encoded string (remove spaces and newline characters)
    encoded_str = encoded_str.replace(" ", "").replace("\n", "")

    # Remove padding and adjust the length if needed
    padding = encoded_str.count('=')
    encoded_str = encoded_str.rstrip('=')

    # Convert Base64 characters to binary
    binary_str = ""
    for char in encoded_str:
        binary_str += f"{base64_chars.index(char):06b}"

    # Combine binary groups and convert to original data
    for i in range(0, len(binary_str) - padding * 2, 8):
        byte = binary_str[i:i+8]
        decoded_bytes.append(int(byte, 2))

    # Return decoded bytes
    return decoded_bytes

# Read the Base64 encoded image from image.txt and decode it
if __name__ == "__main__":
    with open("image.txt", "r") as file:
        encoded_image = file.read()
    decoded_image = base64_decoder(encoded_image)
    with open("decoded_image.png", "wb") as f:
        f.write(decoded_image)