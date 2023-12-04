import socket

def main():
    # server_ip = '10.2.94.209'
    server_ip = 'localhost'
    server_port = 2048

    def send_server_data(client_socket, message):
        client_socket.sendall(message.encode())

    def recv_server_data(client_socket, buffer_size=2048):
        size = int(client_socket.recv(buffer_size).decode())
        # print(size)
        send_server_data(client_socket, message="Ok")
        # recv size as bytes and convert to number
        response = []
        response_len = 0
        while response_len < size:
            chunk = client_socket.recv(buffer_size)
            response.append(chunk.decode())
            response_len += len(chunk)
            # print(f"\nDatalen: {response_len}")
        return ''.join(response)

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
            user_input = ""
            while user_input == "":
                user_input = input("Input:   ").strip()
            print(f"Entered: {user_input}")
            send_server_data(client_socket, user_input)
            server_response = recv_server_data(client_socket)

if __name__ == "__main__":
    main()
