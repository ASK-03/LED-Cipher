def toMatrix(string):

    lst = []
    for nibble in string:
        if nibble.upper() in "ABCDEF":
            lst.append(ord(nibble.upper()) - 55)
        else:
            lst.append(int(nibble))

    state_matrix = [lst[k : k + 4] for k in range(0, 16, 4)]

    return state_matrix


def toHexString(state):

    flattened = [num for row in state for num in row]
    hex_chars = []
    for num in flattened:
        if 0 <= num <= 9:
            hex_chars.append(str(num))
        elif 10 <= num <= 15:
            hex_chars.append(chr(num + 55))
        else:
            raise ValueError(f"Invalid matrix value: {num}. Must be between 0 and 15.")
    return "".join(hex_chars)


def GF(a, b):
    p = 0
    for _ in range(4):
        if b & 1:
            p ^= a
        overflow = a & 0x8
        a = (a << 1) & 0xF
        if overflow:
            a ^= 0x3
        b >>= 1
    return p


"""-------------------Key-Schedule of no use :|--------------------"""


def generate_keys(key):
    mk = []
    for nibble in key:
        if nibble.upper() in "ABCDEF":
            mk.append(ord(nibble.upper()) - 55)
        else:
            mk.append(int(nibble))

    subkeys = []
    for i in range(9):
        subkey = []
        for j in range(16):
            index = (j + (16 * i)) % 16
            subkey.append(mk[index])
        # Reshape the subkey into a 4x4 matrix
        subkey_matrix = [subkey[k : k + 4] for k in range(0, 16, 4)]
        subkeys.append(subkey_matrix)

    return subkeys


"""-------------------Key-Schedule of no use :|--------------------"""

def text_to_hex(text):
    # Convert each character in the text to its hexadecimal representation
    hex_text = ''.join(format(ord(char), '02x') for char in text)
    return hex_text


def hex_to_text(hex_text):
    # Convert every two characters (one byte) from hexadecimal to a character
    text = ''.join(chr(int(hex_text[i:i+2], 16)) for i in range(0, len(hex_text), 2))
    return text

def pad_text(text, block_size=8):
    """Apply PKCS#7 padding to the text."""
    pad_len = block_size - (len(text) % block_size)
    return text + chr(pad_len) * pad_len

def unpad_text(padded_text):
    """Remove PKCS#7 padding."""
    pad_len = ord(padded_text[-1])
    return padded_text[:-pad_len]