import socket
import threading
import rsa
from led.ecb_decrypt import ecb_decrypt
from led.ecb_encrypt import ecb_encrypt

SERVER_HOST = "localhost"
SERVER_PORT = 12345

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))

# Receive server's RSA public key
server_public_key = rsa.PublicKey.load_pkcs1(client.recv(1024))

# Generate RSA keypair for the client
client_public_key, client_private_key = rsa.newkeys(512)

# Send client's public key to the server
client.send(client_public_key.save_pkcs1())

# Select a channel
print(client.recv(1024).decode("utf-8"))
channel_name = input("Enter channel name: ").strip()
client.send(channel_name.encode("utf-8"))

# Enter channel password
print(client.recv(1024).decode("utf-8"))
password = input("Enter password: ").strip()
client.send(password.encode("utf-8"))

# Receive encrypted key from the server
encrypted_key = client.recv(1024)
print(f"[*] Received encrypted key: {encrypted_key}")
try:
    channel_key = rsa.decrypt(encrypted_key, client_private_key)
    print(f"[*] Decrypted key: {channel_key}")
    channel_key = channel_key.decode("utf-8")
except Exception as e:
    print("Failed to decrypt the key. Disconnecting:", e)
    client.close()
    exit()

print(client.recv(1024).decode("utf-8"))

# Receive messages
def receive_messages():
    while True:
        try:
            encrypted_message = client.recv(1024)
            message = ecb_decrypt(encrypted_message.decode("utf-8"), channel_key)
            print(f"Message: {message}")
        except:
            print("Connection closed by the server.")
            client.close()
            break

# Start thread to receive messages
threading.Thread(target=receive_messages, daemon=True).start()

# Send messages
while True:
    message = input("You: ").strip()
    encrypted_message = ecb_encrypt(message, channel_key)
    client.send(encrypted_message.encode("utf-8"))
