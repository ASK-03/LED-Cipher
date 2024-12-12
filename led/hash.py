from tqdm import tqdm
import os
from led_encrypt import led_encrypt
from helper import pad_text, text_to_hex, toHexString

def davies_meyer_hash(message: str, key: str, block_size=16):
    padded_text = pad_text(message, block_size)
    hex_text = text_to_hex(padded_text)
    
    H = "00" * block_size  

    for i in range(0, len(hex_text), block_size):
        block = hex_text[i:i + block_size]
        encrypted = toHexString(led_encrypt(H, block))

        H = "".join(
            f"{int(encrypted[j:j+2], 16) ^ int(H[j:j+2], 16):02x}"
            for j in range(0, len(encrypted), 2)
        )

    return H


def pre_image_attack(target_hash: str, key: str, block_size=16, max_attempts=2**64):
    """
    Simulate a pre-image attack to find an input that hashes to a target value.
    """
    with tqdm(total=max_attempts, desc="Pre-image Attack") as pbar:
        for _ in range(max_attempts):
            candidate = os.urandom(block_size).hex()
            candidate_hash = davies_meyer_hash(candidate, key, block_size)
            if candidate_hash == target_hash:
                return candidate
            pbar.update(1)
    return None


def second_pre_image_attack(original_message: str, key: str, block_size=16, max_attempts=2**64):
    """
    Simulate a second pre-image attack to find a different input with the same hash.
    """
    original_hash = davies_meyer_hash(original_message, key, block_size)
    with tqdm(total=max_attempts, desc="Second Pre-image Attack") as pbar:
        for _ in range(max_attempts):
            candidate = os.urandom(block_size).hex()
            if candidate != original_message:
                candidate_hash = davies_meyer_hash(candidate, key, block_size)
                if candidate_hash == original_hash:
                    return candidate
            pbar.update(1)
    return None 


def find_collision(key: str, block_size=16, max_attempts=2**32):
    """
    Simulate a collision detection attack to find two inputs with the same hash.
    """
    hash_dict = {}
    with tqdm(total=max_attempts, desc="Collision Detection") as pbar:
        for _ in range(max_attempts):
            candidate = os.urandom(block_size).hex()
            candidate_hash = davies_meyer_hash(candidate, key, block_size)
            
            if candidate_hash in hash_dict:
                return hash_dict[candidate_hash], candidate
            else:
                hash_dict[candidate_hash] = candidate
            pbar.update(1) 
    return None


if __name__ == "__main__":
    key = "0123456789ABCDEF"
    toHash = "Abhishek Singh Kushwaha"
    hash = davies_meyer_hash(toHash, key)
    print(f"H({key}, {toHash}) = {hash}")

    original_message = "Hello, World!"
    block_size = 16

    # Pre-image attack
    target_hash = davies_meyer_hash(original_message, key, block_size)
    pre_image = pre_image_attack(target_hash, key, block_size)
    print(f"Pre-image attack result: {pre_image}")

    # Second pre-image attack
    second_pre_image = second_pre_image_attack(original_message, key, block_size)
    print(f"Second pre-image attack result: {second_pre_image}")

    # Collision detection
    collision = find_collision(key, block_size)
    print(f"Collision detection result: {collision}")
