import socket
import os

########################################

ip = ""
port = "5001"

########################################

def upload_files(client_socket, directory):
    client_socket.sendall(b"upload")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, directory)
            file_size = os.path.getsize(file_path)
            client_socket.sendall(f"{relative_path}|{file_size}".encode())
            client_socket.recv(1024)  # Wait for the server to be ready
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    client_socket.sendall(chunk)
    client_socket.sendall(b"done")  # Signal completion

def download_files(client_socket, directory):
    client_socket.sendall(b"download")
    while True:
        file_info = client_socket.recv(1024).decode()
        if file_info == "done":
            break
        file_path, file_size = file_info.split("|")
        file_size = int(file_size)
        full_path = os.path.join(directory, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        client_socket.sendall(b"ready")  # Tell the server to start sending file data
        with open(full_path, "wb") as f:
            bytes_received = 0
            while bytes_received < file_size:
                chunk = client_socket.recv(min(file_size - bytes_received, 4096))
                if not chunk:
                    break
                f.write(chunk)
                bytes_received += len(chunk)

def start_client(server_ip, directory):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    action = input("Enter 'upload' to upload files or 'download' to download files: ").strip().lower()
    if action == "upload":
        upload_files(client_socket, directory)
    elif action == "download":
        download_files(client_socket, directory)
    else:
        print("Invalid action")

    client_socket.close()

if __name__ == "__main__":
    server_ip_address = ip
    current_directory = os.path.dirname(os.path.abspath(__file__))
    start_client(server_ip_address, current_directory)
