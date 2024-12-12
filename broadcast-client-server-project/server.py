import socket
import threading
from led.ecb_decrypt import ecb_decrypt
from led.ecb_encrypt import ecb_encrypt
import rsa

SERVER_PORT = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", SERVER_PORT))
server.listen()

# Channel structure: {channel_name: {"password": str, "key": str, "clients": list}}
channels = {
    "general": {"password": "general123", "key": "0000000000000000", "clients": []},
    "sports": {"password": "sports123", "key": "0000000000000001", "clients": []},
    "tech": {"password": "tech123", "key": "0000000000000002", "clients": []},
}

# Generate RSA keys
server_public_key, server_private_key = rsa.newkeys(512)

def handle_client(client_socket, addr):
    try:
        # Send public RSA key to the client
        client_socket.send(server_public_key.save_pkcs1())

        # Receive client's public RSA key
        client_public_key = rsa.PublicKey.load_pkcs1(client_socket.recv(1024))

        # Prompt client to select a channel
        client_socket.send("Available channels: general, sports, tech. Enter your choice: ".encode("utf-8"))
        channel_name = client_socket.recv(1024).decode("utf-8").strip()

        # Check if channel exists
        if channel_name not in channels:
            client_socket.send("Invalid channel name. Disconnecting.".encode("utf-8"))
            client_socket.close()
            return

        # Prompt for channel password
        client_socket.send("Enter channel password: ".encode("utf-8"))
        password = client_socket.recv(1024).decode("utf-8").strip()

        # Verify password
        if password != channels[channel_name]["password"]:
            client_socket.send("Incorrect password. Disconnecting.".encode("utf-8"))
            client_socket.close()
            return

        # Send the channel's key encrypted using the client's public RSA key
        encrypted_key = rsa.encrypt(channels[channel_name]["key"].encode("utf-8"), client_public_key)
        print(f"[*] Sending encrypted key: {encrypted_key}")
        client_socket.send(encrypted_key)

        # Add client to the channel
        channels[channel_name]["clients"].append(client_socket)
        client_socket.send("Joined the channel. You can start chatting.".encode("utf-8"))

        # Handle messages from the client
        while True:
            encrypted_message = client_socket.recv(1024)
            message = ecb_decrypt(encrypted_message.decode("utf-8"), channels[channel_name]["key"])
            print(f"Message from {addr}: {message}")

            # Broadcast the message to other clients in the same channel
            for client in channels[channel_name]["clients"]:
                if client != client_socket:
                    encrypted_broadcast = ecb_encrypt(message, channels[channel_name]["key"])
                    client.send(encrypted_broadcast.encode("utf-8"))
    except Exception as e:
        print(f"Client {addr} disconnected: {e}")
        for channel in channels.values():
            if client_socket in channel["clients"]:
                channel["clients"].remove(client_socket)
        client_socket.close()


while True:
    print("Server is listening for connections...")
    client_socket, addr = server.accept()
    print(f"New connection from {addr}")
    threading.Thread(target=handle_client, args=(client_socket, addr)).start()
