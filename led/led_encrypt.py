import argparse
import sys
from helper import toMatrix, toHexString

Sbox = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

RC = [
    0x01,
    0x03,
    0x07,
    0x0F,
    0x1F,
    0x3E,
    0x3D,
    0x3B,
    0x37,
    0x2F,
    0x1E,
    0x3C,
    0x39,
    0x33,
    0x27,
    0x0E,
    0x1D,
    0x3A,
    0x35,
    0x2B,
    0x16,
    0x2C,
    0x18,
    0x30,
    0x21,
    0x02,
    0x05,
    0x0B,
    0x17,
    0x2E,
    0x1C,
    0x38,
    0x31,
    0x23,
    0x06,
    0x0D,
    0x1B,
    0x36,
    0x2D,
    0x1A,
    0x34,
    0x29,
    0x12,
    0x24,
    0x08,
    0x11,
    0x22,
    0x04,
]

MDS = [
    [0x4, 0x1, 0x2, 0x2],
    [0x8, 0x6, 0x5, 0x6],
    [0xB, 0xE, 0xA, 0x9],
    [0x2, 0x2, 0xF, 0xB],
]


"""-------------------Round Implementation--------------------"""


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


def addRoundConstant(state, rc):
    state[0][0], state[1][0], state[2][0], state[3][0] = (
        state[0][0] ^ 4,
        state[1][0] ^ 4 ^ 1,
        state[2][0] ^ 2,
        state[3][0] ^ 3,
    )
    state[0][1], state[1][1], state[2][1], state[3][1] = (
        state[0][1] ^ (rc >> 3),
        state[1][1] ^ (((rc >> 2) & 1) << 2 | ((rc >> 1) & 1) << 1 | (rc & 1)),
        state[2][1] ^ (rc >> 3),
        state[3][1] ^ (((rc >> 2) & 1) << 2 | ((rc >> 1) & 1) << 1 | (rc & 1)),
    )


def subSbox(state):
    for i in range(len(state)):
        for j in range(len(state)):
            state[i][j] = Sbox[state[i][j]]
    return state


def shiftRows(state):
    new_state = [[0 for i in range(4)] for i in range(4)]
    for i in range(4):
        new_state[i] = state[i][i:] + state[i][0:i]
    return new_state


def mixColumn(state):
    new_state = [[0 for _ in range(4)] for _ in range(4)]

    for col in range(4):
        for row in range(4):
            new_state[row][col] = 0
            for k in range(4):
                new_state[row][col] ^= GF(MDS[row][k], state[k][col])

    return new_state


"""-------------------Round Implementation--------------------"""


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


"""-------------------Step Implementation--------------------"""


def step(state, k):
    for i in range(4):
        addRoundConstant(state, RC[4 * k + i])
        subSbox(state)
        state = shiftRows(state)
        state = mixColumn(state)

    return state


def addStepKey(state, step_key):
    for i in range(len(state)):
        for j in range(len(state[0])):
            state[i][j] ^= step_key[i][j]


"""-------------------Step Implementation--------------------"""


"""-------------------Encryption--------------------"""


def led_encrypt(plaintxt, master_key):

    state = toMatrix(plaintxt)

    step_keys = generate_keys(master_key)

    for i in range(len(step_keys) - 1):
        # adding key after every four rounfs
        addStepKey(state, step_keys[i])
        state = step(state, i)

    addStepKey(state, step_keys[-1])
    return state


"""-------------------Encryption--------------------"""


def main():

    parser = argparse.ArgumentParser(description="LED Block Cipher Encryption")

    parser.add_argument(
        "-p",
        "--plain_text",
        type=str,
        required=True,
        help="16-character hexadecimal plain text to encrypt",
    )

    parser.add_argument(
        "-k",
        "--master_key",
        type=str,
        required=True,
        help="16-character hexadecimal master key",
    )

    try:
        args = parser.parse_args()

        if len(args.plain_text) != 16:
            raise ValueError("Plain text must be 16 characters long")

        if len(args.master_key) != 16:
            raise ValueError("Master key must be 16 characters long")

        cipher_state = led_encrypt(args.plain_text, args.master_key)
        print("cipher_text:", toHexString(cipher_state))

    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except ImportError:
        print(
            "Error: Unable to import required functions. Ensure helper.py is in the same directory."
        )
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
