import socket
import os
import threading

##############################################

port = "5001"

##############################################

def handle_client(client_socket, base_directory):
    operation = client_socket.recv(1024).decode()
    
    if operation == "upload":
        receive_files(client_socket, base_directory)
    elif operation == "download":
        send_files(client_socket, base_directory)
    client_socket.close()

def send_files(client_socket, directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            file_size = os.path.getsize(file_path)
            client_socket.sendall(f"{relative_path}|{file_size}".encode())
            client_socket.recv(1024)  # Wait for the client to be ready
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    client_socket.sendall(chunk)
    client_socket.sendall(b"done")  # Signal completion

def receive_files(client_socket, directory):
    while True:
        file_info = client_socket.recv(1024).decode()
        if file_info == "done":
            break
        file_path, file_size = file_info.split("|")
        file_size = int(file_size)
        full_path = os.path.join(directory, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        client_socket.sendall(b"ready")  # Tell the client to start sending file data
        with open(full_path, "wb") as f:
            bytes_received = 0
            while bytes_received < file_size:
                chunk = client_socket.recv(min(file_size - bytes_received, 4096))
                if not chunk:
                    break
                f.write(chunk)
                bytes_received += len(chunk)

def start_server(directory):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)
    print("Server listening on port " + port + "...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, directory))
        client_handler.start()

if __name__ == "__main__":
    current_directory = os.path.dirname(os.path.abspath(__file__))
    start_server(current_directory)
