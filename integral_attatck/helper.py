def toMatrix(string):
    
    lst= []
    for nibble in string:
        if nibble.upper() in "ABCDEF":
            lst.append(ord(nibble.upper()) - 55)
        else:
            lst.append(int(nibble))
    
    state_matrix = [lst[k:k + 4] for k in range(0, 16, 4)]

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
    return ''.join(hex_chars)


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
  mk=[]
  for nibble in key:
    if nibble.upper() in "ABCDEF":
      mk.append(ord(nibble.upper())-55)
    else:
      mk.append(int(nibble))

  subkeys = []
  for i in range(9):
      subkey = []
      for j in range(16):
          index = (j + (16 * i)) % 16
          subkey.append(mk[index])
      # Reshape the subkey into a 4x4 matrix
      subkey_matrix = [subkey[k:k + 4] for k in range(0, 16, 4)]
      subkeys.append(subkey_matrix)

  return subkeys

"""-------------------Key-Schedule of no use :|--------------------"""
