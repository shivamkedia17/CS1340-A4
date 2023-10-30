import socket

def main():
    server_ip = "10.2.94.209"  # Replace with the server's IP address
    server_port = 1100

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))
        message = "Hello, server!"
        client_socket.sendall(message.encode())
        response = client_socket.recv(1024)
        print(f"Server Response: {response.decode()}")

if __name__ == "__main__":
    main()
