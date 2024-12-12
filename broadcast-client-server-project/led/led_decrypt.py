import argparse
import sys
from .helper import toMatrix, toHexString, GF, generate_keys

inverse_Sbox = [
    0x5,
    0xE,
    0xF,
    0x8,
    0xC,
    0x1,
    0x2,
    0xD,
    0xB,
    0x4,
    0x6,
    0x3,
    0x0,
    0x7,
    0x9,
    0xA,
]

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

IMDS = [
    [0xC, 0xC, 0xD, 0x4],
    [0x3, 0x8, 0x4, 0x5],
    [0x7, 0x6, 0x2, 0xE],
    [0xD, 0x9, 0x9, 0xD],
]


"""-------------------Round Implementation--------------------"""


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


def inverse_mix_column(state):
    new_state = [[0 for _ in range(4)] for _ in range(4)]

    for col in range(4):
        for row in range(4):
            new_state[row][col] = 0
            for k in range(4):
                new_state[row][col] ^= GF(IMDS[row][k], state[k][col])

    return new_state


def inverse_shift_rows(state):
    new_state = [[0 for i in range(4)] for i in range(4)]
    for i in range(4):
        new_state[i] = state[i][4 - i :] + state[i][: 4 - i]
    return new_state


def inverse_sub(state):
    for i in range(len(state)):
        for j in range(len(state)):
            state[i][j] = inverse_Sbox[state[i][j]]


"""-------------------Round Implementation--------------------"""


"""-------------------Step Implementation--------------------"""


def reverse_step(state, k):
    for i in range(3, -1, -1):
        state = inverse_mix_column(state)
        state = inverse_shift_rows(state)
        inverse_sub(state)
        addRoundConstant(state, RC[4 * k + i])
    return state


def addStepKey(state, step_key):
    for i in range(len(state)):
        for j in range(len(state[0])):
            state[i][j] ^= step_key[i][j]


"""-------------------Step Implementation--------------------"""


"""-------------------Decryption--------------------"""


def led_decrypt(ciphertxt, master_key):

    state = toMatrix(ciphertxt)

    step_keys = generate_keys(master_key)

    for i in range(len(step_keys) - 2, -1, -1):

        addStepKey(state, step_keys[i])
        state = reverse_step(state, i)

    addStepKey(state, step_keys[0])
    return state


"""-------------------Decryption--------------------"""


def main():

    parser = argparse.ArgumentParser(description="LED Block Cipher Encryption")

    parser.add_argument(
        "-c",
        "--cipher_text",
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

        if len(args.cipher_text) != 16:
            raise ValueError("Plain text must be 16 characters long")

        if len(args.master_key) != 16:
            raise ValueError("Master key must be 16 characters long")

        plain_state = led_decrypt(args.cipher_text, args.master_key)
        print("plain_text:", toHexString(plain_state))

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
