from led_decrypt_orgnl import led_decrypt
from helper import toHexString
key__3_7_11_15 = ['0000', '0d8a', '36a8', '3b22', '4538', '48b2', '7390', '7e1a', '913d', '9cb7', 'a795', 'aa1f', 'd405', 'd98f', 'e2ad', 'ef27']
key_2_6_10_14 = ['0000', '0ff7', '748c', '7b7b', 'a246', 'adb1', 'd6ca', 'd93d']
key_1_5_9_13 = ['0000', '004a', '0599', '05d3', '1396', '13dc', '160f', '1645', '20a7', '20ed', '253e', '2574', '3331', '337b', '36a8', '36e2', '42b5', '42ff', '472c', '4766', '5123', '5169', '54ba', '54f0', '6212', '6258', '678b', '67c1', '7184', '71ce', '741d', '7457', '82ab', '82e1', '8732', '8778', '913d', '9177', '94a4', '94ee', 'a20c', 'a246', 'a795', 'a7df', 'b19a', 'b1d0', 'b403', 'b449', 'c01e', 'c054', 'c587', 'c5cd', 'd388', 'd3c2', 'd611', 'd65b', 'e0b9', 'e0f3', 'e520', 'e56a', 'f32f', 'f365', 'f6b6', 'f6fc']
key_0_4_8_12 = ['0000', '5656', 'be6d', 'e83b']
filtered_keys = []
for key_1 in key__3_7_11_15:
    for key_2 in key_2_6_10_14 :
        for key_3 in key_1_5_9_13:
            for key_4 in key_0_4_8_12:
                master_key = f"{key_4[0]}{key_3[0]}{key_2[0]}{key_1[0]}{key_4[1]}{key_3[1]}{key_2[1]}{key_1[1]}{key_4[2]}{key_3[2]}{key_2[2]}{key_1[2]}{key_4[3]}{key_3[3]}{key_2[3]}{key_1[3]}"
                state = led_decrypt("B79F9A50AC84A205", master_key)
                pln_txt = toHexString(state)
                if pln_txt == "023456789ABCDEF0":
                    filtered_keys.append(master_key)
print(len(filtered_keys))
print(filtered_keys)

print(len(key__3_7_11_15))
print(len(key_2_6_10_14))
print(len(key_1_5_9_13))
print(len(key_0_4_8_12))

