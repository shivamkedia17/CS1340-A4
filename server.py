import socketserver

class TCPHandler(socketserver.BaseRequestHandler):
    def recv_msg(self):
            block_size = 1024
            data = self.request.recv(block_size).strip()
            response = data.decode()
            # Log the received message to the console
            print(f"{self.client_address}: {data.decode()}")
            return response

    def send_msg(self, message):
        self.request.sendall(message.encode())

    def greet(self):
        self.send_msg("Hi yada yada, type \"close\" to close the connection.")

    def handle(self):
        initial_message = self.recv_msg()
        self.greet()
        message = "meow"
        counter = 0
        while True:
            client_response = self.recv_msg()
            if client_response == "close":
                self.request.sendall(b"Connection Closed")
                self.request.close()
                break
            else:
                counter += 1
                self.request.sendall(f"{client_response} {message} {counter}".encode())

    def use_features(self, option):
        pass


def main():
    # server_ip       = '10.2.94.209'
    server_ip       = 'localhost'
    server_port     = 2048
    server_address  = (server_ip, server_port)
    server          = socketserver.TCPServer(server_address, TCPHandler)

    '''
    The socketserver library is basically an elegantly written API that provides a way to deal with servers.
    Some APIs are provided, In this case it's a TCP server class.
    It's constructor does the following:
    1. Binds a server-side socket to server_address
    2. Activates the server: starts to listen for connections as long as there are less connections than the backlog
    3. By default:
        - reuseaddress is false: server enters a brief waiting state after being shut down
        - reuseport is false: two sockets cannot bind to the same port--
             this option will be useful if I plan on making the server multithreaded
    4. Requests are handled using the Handler class defined above
    '''

    print(f"Server up. Listening on port {server_port}...")
    print(f"Press Ctrl-C to gracefully shut down the server.")
    print(f"--------------Message Log-----------------------")

    try:
        server.serve_forever(poll_interval=1)
    except KeyboardInterrupt:
        try:
            print(f"\n-----------------------------------------------")
            print("Shutting Down server...")
            server.shutdown()
            server.server_close()
            print("Successfully shut down server.")
        except Exception as e:
            print(f"{e} occurred while shutting down server.")

if __name__ == "__main__":
    main()
