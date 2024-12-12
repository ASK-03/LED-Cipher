import argparse
import sys
from helper import toMatrix,toHexString,GF,generate_keys
import random

inverse_Sbox=[0x5, 0xE, 0xF, 0x8, 0xC, 0x1, 0x2, 0xD, 0xB, 0x4, 0x6, 0x3, 0x0, 0x7, 0x9, 0xA]

RC = [0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F,0x1E, 0x3C, 0x39, 0x33, 0x27, 0x0E, 0x1D, 0x3A, 0x35, 0x2B,0x16, 0x2C, 0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E,0x1C, 0x38, 0x31, 0x23, 0x06, 0x0D, 0x1B, 0x36, 0x2D, 0x1A,0x34, 0x29, 0x12, 0x24, 0x08, 0x11, 0x22, 0x04]

IMDS = [
[0xC, 0xC, 0xD, 0x4],
[0x3, 0x8, 0x4, 0x5],
[0x7, 0x6, 0x2, 0xE],
[0xD, 0x9, 0x9, 0xD]
]




"""-------------------Round Implementation--------------------"""


def addRoundConstant(state,rc):
  state[0][0],state[1][0],state[2][0],state[3][0]=state[0][0]^4,state[1][0]^4^1,state[2][0]^2,state[3][0]^3
  state[0][1],state[1][1],state[2][1],state[3][1]=state[0][1]^(rc>>3),state[1][1]^(((rc>>2)&1)<<2|((rc>>1)&1)<<1|(rc&1)),state[2][1]^(rc>>3),state[3][1]^(((rc>>2)&1)<<2|((rc>>1)&1)<<1|(rc&1))


def inverse_mix_column(state):
  new_state = [[0 for _ in range(4)] for _ in range(4)]

  for col in range(4):
      for row in range(4):
          new_state[row][col] = 0
          for k in range(4):
              new_state[row][col] ^= GF(IMDS[row][k], state[k][col])

  return new_state


def inverse_shift_rows(state):
  new_state=[[0 for i in range(4)] for i in range(4)]
  for i in range(4):
      new_state[i]=state[i][4-i:]+state[i][:4-i]
  return new_state


def inverse_sub(state):
  for i in range(len(state)):
    for j in range(len(state)):
      state[i][j]=inverse_Sbox[state[i][j]]



"""-------------------Round Implementation--------------------"""


"""-------------------Step Implementation--------------------"""


def reverse_step(state,k):
  for i in range(3,-1,-1):
    state=inverse_mix_column(state)
    state=inverse_shift_rows(state)
    inverse_sub(state)
    addRoundConstant(state,RC[4*k+i])
    return state


def addStepKey(state,step_key):
  for i in range(len(state)):
    for j in range(len(state[0])):
      state[i][j]^=step_key[i][j]


"""-------------------Step Implementation--------------------"""


"""-------------------Decryption--------------------"""

"""-------------------Integral Attack on Step-1 by guessing column 4--------------------"""

def generate_master_key(user_chars):
    possible_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f']
    if len(user_chars) != 4:
        raise ValueError("You must provide exactly 4 characters for positions 4, 8, 12, and 16.")
    
    master_key = [None] * 16  # This ensures the list has 16 elements

    # Set the user-defined characters for positions 4, 8, 12, and 16 (1-indexed)
    master_key[3] = user_chars[0]  # Position 4
    master_key[7] = user_chars[1]  # Position 8
    master_key[11] = user_chars[2] # Position 12
    master_key[15] = user_chars[3] # Position 16

    # Fill the other positions with random values from possible_values
    for i in range(16):
        if master_key[i] is None:  # If the position is not user-defined
            master_key[i] = random.choice(possible_values)

    # Convert the master key list to a string and return
    return ''.join(map(str, master_key))

def xor_all_elements(elements):
    """
    XOR all elements in a list.

    :param elements: A list of integers.
    :return: The result of XORing all elements.
    """
    result = 0  # Initialize the result to 0
    for element in elements:
        result ^= element  # Perform XOR with each element

    return result


def led_decrypt(ciphertxt, master_key):
    state = toMatrix(ciphertxt)
    step_keys = generate_keys(master_key)
    addStepKey(state, step_keys[0])  
    temp_state = reverse_step(state, 0)
    return temp_state

mapper = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}

possible_keys = []
for bit_3 in range(16):
  if bit_3 > 9:
    bit_3 = mapper[bit_3]  
  else:
    pass
  for bit_7 in range(16):
    if bit_7 > 9:
      bit_7 = mapper[bit_7]  
    else:
      pass
    for bit_11 in range(16):
      if bit_11 > 9:
        bit_11 = mapper[bit_11]  
      else:
        pass
      for bit_15 in range(16):
        if bit_15 > 9:
          bit_15 = mapper[bit_15]  
        else:
          pass
        ciphertext_list = ["B79F9A50AC84A205", "9FB657961E9A63CF", "035AD8F55FB390FA", "6BE63C04D9571D87", "7EF5ECBC1942B8CE", "3E353726CC848782", "B4E6A522FF2EB0B5", "624D32824197196E", "E17703501B88AE5A", "1E3E197FAAA0B26B", "256E89E79337C81A", "384A9B0D2EC5FF3F", "914EC5045944AE72", "4F11812C6EF99CB0", "98119B47DFE97AD4", "0B16F9D9BE1E6ACE"]
        bit3 = []
        bit7 = []
        bit11 = []
        bit15 = []
        user_chars = [f'{bit_3}', f'{bit_7}', f'{bit_11}', f'{bit_15}']
        master_key = generate_master_key(user_chars)
        for ciphertext in  ciphertext_list :
          get_state = led_decrypt(ciphertext, master_key)
          bit3.append(get_state[0][3])
          bit7.append(get_state[1][0])
          bit11.append(get_state[2][1])
          bit15.append(get_state[3][2])
        bit3_xor = xor_all_elements(bit3)
        bit7_xor = xor_all_elements(bit7)
        bit11_xor = xor_all_elements(bit11)
        bit15_xor = xor_all_elements(bit15)
        bit15_xor = xor_all_elements(bit15)
        if int(bit3_xor) == int(bit7_xor) == int(bit11_xor) == int(bit15_xor) == 0:
          possible_keys.append(f"{user_chars[0]}{user_chars[1]}{user_chars[2]}{user_chars[3]}")
          
print(len(possible_keys))
print("b_3, b_7, b_11, b_15", possible_keys)


"""-------------------Integral Attack on Step-1 by guessing column 3--------------------"""

def generate_master_key(user_chars):
    possible_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f']
    if len(user_chars) != 4:
        raise ValueError("You must provide exactly 4 characters for positions 2, 6, 10, and 14.")
    
    master_key = [None] * 16 

    master_key[2] = user_chars[0]  # Position 2
    master_key[6] = user_chars[1]  # Position 6
    master_key[10] = user_chars[2]  # Position 10
    master_key[14] = user_chars[3] # Position 14

    for i in range(16):
        if master_key[i] is None:
            master_key[i] = random.choice(possible_values)

    return ''.join(map(str, master_key))

def xor_all_elements(elements):
    """
    XOR all elements in a list.

    :param elements: A list of integers.
    :return: The result of XORing all elements.
    """
    result = 0  # Initialize the result to 0
    for element in elements:
        result ^= element  # Perform XOR with each element

    return result


def led_decrypt(ciphertxt, master_key):
    state = toMatrix(ciphertxt)
    step_keys = generate_keys(master_key)
    addStepKey(state, step_keys[0])  
    temp_state = reverse_step(state, 0)
    return temp_state


possible_keys = []

for bit_3 in range(16):
  if bit_3 > 9:
    bit_3 = mapper[bit_3]  
  else:
    pass
  for bit_7 in range(16):
    if bit_7 > 9:
      bit_7 = mapper[bit_7]  
    else:
      pass
    for bit_11 in range(16):
      if bit_11 > 9:
        bit_11 = mapper[bit_11]  
      else:
        pass
      for bit_15 in range(16):
        if bit_15 > 9:
          bit_15 = mapper[bit_15]  
        else:
          pass
        ciphertext_list = ["B79F9A50AC84A205", "9FB657961E9A63CF", "035AD8F55FB390FA", "6BE63C04D9571D87", "7EF5ECBC1942B8CE", "3E353726CC848782", "B4E6A522FF2EB0B5", "624D32824197196E", "E17703501B88AE5A", "1E3E197FAAA0B26B", "256E89E79337C81A", "384A9B0D2EC5FF3F", "914EC5045944AE72", "4F11812C6EF99CB0", "98119B47DFE97AD4", "0B16F9D9BE1E6ACE"]
        bit3 = []
        bit7 = []
        bit11 = []
        bit15 = []
        user_chars = [f'{bit_3}', f'{bit_7}', f'{bit_11}', f'{bit_15}']
        master_key = generate_master_key(user_chars)
        for ciphertext in  ciphertext_list :
          get_state = led_decrypt(ciphertext, master_key)
          bit3.append(get_state[0][2])
          bit7.append(get_state[1][3])
          bit11.append(get_state[2][0])
          bit15.append(get_state[3][1])
        bit3_xor = xor_all_elements(bit3)
        bit7_xor = xor_all_elements(bit7)
        bit11_xor = xor_all_elements(bit11)
        bit15_xor = xor_all_elements(bit15)
        if int(bit3_xor) == int(bit7_xor) == int(bit11_xor) == int(bit15_xor) == 0:
          possible_keys.append(f"{user_chars[0]}{user_chars[1]}{user_chars[2]}{user_chars[3]}")
          
print(len(possible_keys))
print("b_2, b_6, b_10, b_14", possible_keys)




"""-------------------Integral Attack on Step-1 by guessing column 2--------------------"""

def generate_master_key(user_chars):
    possible_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f']
    if len(user_chars) != 4:
        raise ValueError("You must provide exactly 4 characters for positions 2, 6, 10, and 14.")
    
    master_key = [None] * 16 

    master_key[1] = user_chars[0]  # Position 2
    master_key[5] = user_chars[1]  # Position 6
    master_key[9] = user_chars[2]  # Position 10
    master_key[13] = user_chars[3] # Position 14

    for i in range(16):
        if master_key[i] is None:
            master_key[i] = random.choice(possible_values)

    return ''.join(map(str, master_key))

def xor_all_elements(elements):
    """
    XOR all elements in a list.

    :param elements: A list of integers.
    :return: The result of XORing all elements.
    """
    result = 0  # Initialize the result to 0
    for element in elements:
        result ^= element  # Perform XOR with each element

    return result


def led_decrypt(ciphertxt, master_key):
    state = toMatrix(ciphertxt)
    step_keys = generate_keys(master_key)
    addStepKey(state, step_keys[0])  
    temp_state = reverse_step(state, 0)
    return temp_state
     

possible_keys = []
for bit_3 in range(16):
  if bit_3 > 9:
    bit_3 = mapper[bit_3]  
  else:
    pass
  for bit_7 in range(16):
    if bit_7 > 9:
      bit_7 = mapper[bit_7]  
    else:
      pass
    for bit_11 in range(16):
      if bit_11 > 9:
        bit_11 = mapper[bit_11]  
      else:
        pass
      for bit_15 in range(16):
        if bit_15 > 9:
          bit_15 = mapper[bit_15]  
        else:
          pass
        ciphertext_list = ["B79F9A50AC84A205", "9FB657961E9A63CF", "035AD8F55FB390FA", "6BE63C04D9571D87", "7EF5ECBC1942B8CE", "3E353726CC848782", "B4E6A522FF2EB0B5", "624D32824197196E", "E17703501B88AE5A", "1E3E197FAAA0B26B", "256E89E79337C81A", "384A9B0D2EC5FF3F", "914EC5045944AE72", "4F11812C6EF99CB0", "98119B47DFE97AD4", "0B16F9D9BE1E6ACE"]
        bit3 = []
        bit7 = []
        bit11 = []
        bit15 = []
        user_chars = [f'{bit_3}', f'{bit_7}', f'{bit_11}', f'{bit_15}']
        master_key = generate_master_key(user_chars)
        for ciphertext in  ciphertext_list :
          get_state = led_decrypt(ciphertext, master_key)
          bit3.append(get_state[0][1])
          bit7.append(get_state[1][2])
          bit11.append(get_state[2][3])
          bit15.append(get_state[3][0])
        bit3_xor = xor_all_elements(bit3)
        bit7_xor = xor_all_elements(bit7)
        bit11_xor = xor_all_elements(bit11)
        bit15_xor = xor_all_elements(bit15)
        if int(bit3_xor) == int(bit7_xor) == int(bit11_xor) == int(bit15_xor) == 0:
          possible_keys.append(f"{user_chars[0]}{user_chars[1]}{user_chars[2]}{user_chars[3]}")
          
print(len(possible_keys))
print("b_1, b_5, b_9, b_13", possible_keys)


"""-------------------Integral Attack on Step-1 by guessing column 1--------------------"""

def generate_master_key(user_chars):
    possible_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f']
    if len(user_chars) != 4:
        raise ValueError("You must provide exactly 4 characters for positions 2, 6, 10, and 14.")
    
    master_key = [None] * 16 

    master_key[0] = user_chars[0]  # Position 2
    master_key[4] = user_chars[1]  # Position 6
    master_key[8] = user_chars[2]  # Position 10
    master_key[12] = user_chars[3] # Position 14

    for i in range(16):
        if master_key[i] is None:
            master_key[i] = random.choice(possible_values)

    return ''.join(map(str, master_key))

def xor_all_elements(elements):
    """
    XOR all elements in a list.

    :param elements: A list of integers.
    :return: The result of XORing all elements.
    """
    result = 0  # Initialize the result to 0
    for element in elements:
        result ^= element  # Perform XOR with each element

    return result


def led_decrypt(ciphertxt, master_key):
    state = toMatrix(ciphertxt)
    step_keys = generate_keys(master_key)
    addStepKey(state, step_keys[0])  
    temp_state = reverse_step(state, 0)
    return temp_state


possible_keys = []
for bit_3 in range(16):
  if bit_3 > 9:
    bit_3 = mapper[bit_3]  
  else:
    pass
  for bit_7 in range(16):
    if bit_7 > 9:
      bit_7 = mapper[bit_7]  
    else:
      pass
    for bit_11 in range(16):
      if bit_11 > 9:
        bit_11 = mapper[bit_11]  
      else:
        pass
      for bit_15 in range(16):
        if bit_15 > 9:
          bit_15 = mapper[bit_15]  
        else:
          pass
        ciphertext_list = ["B79F9A50AC84A205", "9FB657961E9A63CF", "035AD8F55FB390FA", "6BE63C04D9571D87", "7EF5ECBC1942B8CE", "3E353726CC848782", "B4E6A522FF2EB0B5", "624D32824197196E", "E17703501B88AE5A", "1E3E197FAAA0B26B", "256E89E79337C81A", "384A9B0D2EC5FF3F", "914EC5045944AE72", "4F11812C6EF99CB0", "98119B47DFE97AD4", "0B16F9D9BE1E6ACE"]
        bit3 = []
        bit7 = []
        bit11 = []
        bit15 = []
        user_chars = [f'{bit_3}', f'{bit_7}', f'{bit_11}', f'{bit_15}']
        master_key = generate_master_key(user_chars)
        for ciphertext in  ciphertext_list :
          get_state = led_decrypt(ciphertext, master_key)
          bit3.append(get_state[0][0])
          bit7.append(get_state[1][1])
          bit11.append(get_state[2][2])
          bit15.append(get_state[3][3])
        bit3_xor = xor_all_elements(bit3)
        bit7_xor = xor_all_elements(bit7)
        bit11_xor = xor_all_elements(bit11)
        bit15_xor = xor_all_elements(bit15)
        if int(bit3_xor) == int(bit7_xor) == int(bit11_xor) == int(bit15_xor) == 0:
          possible_keys.append(f"{user_chars[0]}{user_chars[1]}{user_chars[2]}{user_chars[3]}")
          
print(len(possible_keys))
print("b_0, b_4, b_8, b_12", possible_keys)






