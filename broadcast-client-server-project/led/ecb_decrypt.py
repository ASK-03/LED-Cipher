from .led_decrypt import led_decrypt
from .helper import hex_to_text, unpad_text, toHexString


def ecb_decrypt(encrypted_text, key):
    """Decrypt text using ECB mode."""
    decrypted_hex = ""
    for i in range(0, len(encrypted_text), 16):  # 16 hex characters = 64 bits
        block = encrypted_text[i:i + 16]
        decrypted_hex += toHexString(led_decrypt(block, key))

    # Convert back to text and remove padding
    padded_text = hex_to_text(decrypted_hex)
    return unpad_text(padded_text)

    return encrypted


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ECB Encryption using LED Block Cipher")

    parser.add_argument(
        "-c",
        "--cipher",
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
    decrypted_text = ecb_decrypt(args.cipher, args.key)

    print(f"Encrypted text: {decrypted_text}")