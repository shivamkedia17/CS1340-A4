import socket

def main():
    # server_ip = '10.2.94.209'
    server_ip = 'localhost'
    server_port = 2048

    def send_server_data(client_socket, message):
        client_socket.sendall(message.encode())

    def recv_server_data(client_socket, buf_size=1024):
        response = client_socket.recv(buf_size)
        return response.decode()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))
        message = "Hi, this is a new client."
        send_server_data(client_socket, message)
        server_response = recv_server_data(client_socket)
        while True:
            if server_response == "Connection Closed":
                print("Connection closed by server. Exiting.")
                break
            print(server_response)
            user_input = input()
            send_server_data(client_socket, user_input)
            server_response = recv_server_data(client_socket)

if __name__ == "__main__":
    main()
