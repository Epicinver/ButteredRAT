import binascii
import base64

# first encode in hex
# then encode in base64

tokendecoded = input("Bot token: ")

def encode_token(s: str) -> str:
    # Step 1: convert string to bytes and then to hex
    hexed = binascii.hexlify(s.encode('utf-8'))  # bytes

    # Step 2: convert hex bytes to string
    hexed_str = hexed.decode('utf-8')

    # Step 3: base64 encode the hex string
    b64ed = base64.b64encode(hexed_str.encode('utf-8'))


tokenencoded = encode_token(tokendecoded)
input(f"{tokenencoded} is the obfuscated token. Use that. Click enter to close")