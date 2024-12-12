# Broadcast Messaging System

This project demonstrates a basic broadcast messaging system implemented using Python's socket programming. It enables real-time group communication by allowing multiple clients to connect to a server, with messages broadcasted to all connected clients.

**Note:** This project is intended as a learning exercise to showcase socket programming and multi-threading in Python. It is not suitable for production use.

## Features

- **Multi-Client Support:** Handles multiple clients concurrently for group communication.
- **Real-Time Broadcasting:** Instantly shares messages from one client to all others.
- **Threaded Client Management:** Each client runs in a separate thread for seamless communication.
- **Connection Management:** Automatically removes disconnected clients from the server's active client list.
- **Simple Setup:** Minimal configuration required to get started.
- **Secure Communication:**
  - **Asymmetric Key Exchange:** Uses RSA for secure key exchange between clients and the server.
  - **Symmetric Message Encryption:** Encrypts and decrypts messages using a shared symmetric key, ensuring confidentiality across communication channels.

## Dependencies

- **Python3**: Ensure that you have Python 3 installed on your system. You can download and install Python 3 from the official Python website: https://www.python.org.
- **pip**: pip is the package installer for Python. It is usually installed by default when you install Python. However, make sure you have pip installed and it is up to date. You can check the version of pip by running the following command:

  ```
  pip --version
  ```

  (Use this command to check, if pip is installed correctly)

  ```
  pip install -r requirements.txt
  ```

  After cloning the repository, to install all the requirements at once.

## Installation

To use, follow the steps given below:

- Navigate to the project directory:
  ```
  cd broadcast-client-server-project
  ```
- Install the necessary Python packages by running the following command:
  ```
  pip install -r requirements.txt
  ```

## Setup Instructions

### 1. Run the server

```
bash
python3 server.py
```

**(The server will now listen for incoming connections on port `12345`)**

### 2. Run the Client

```
bash
python3 client.py
```

**Tip: Start some more server in the same way in different terminals.**

**(The client will connect to the server running on `127.0.0.1:12345`)**

### 3. Messaging

Once connected, any message sent by one client will be broadcasted to all other connected clients. Type exit to disconnect a client from the server.

## Troubleshooting

- **Port Conflicts:** If port **12345** is in use, modify the `SERVER_PORT` in both `server.py` and `client.py`.
- **Connection Issues:** Ensure that the server is running and reachable from the client.
