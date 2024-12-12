from .led_encrypt import led_encrypt
from .helper import text_to_hex, pad_text, toHexString


def ecb_encrypt(text, key):
    """Encrypt text using ECB mode."""
    # Pad the text and convert to hexadecimal
    padded_text = pad_text(text)
    hex_text = text_to_hex(padded_text)

    encrypted = ""
    for i in range(0, len(hex_text), 16):  # 16 hex characters = 64 bits
        block = hex_text[i:i + 16]
        encrypted += toHexString(led_encrypt(block, key))

    return encrypted


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ECB Encryption using LED Block Cipher")

    parser.add_argument(
        "-t",
        "--text",
        type=str,
        required=True,
        help="Text to encrypt using LED Block Cipher",
    )

    parser.add_argument(
        "-k",
        "--key",
        type=str,
        required=True,
        help="16-character hexadecimal master key for LED Block Cipher",
    )

    args = parser.parse_args()
    encrypted_text = ecb_encrypt(args.text, args.key)

    print(f"Encrypted text: {encrypted_text}")