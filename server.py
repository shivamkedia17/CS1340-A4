import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        block_size = 1024
        data = self.request.recv(block_size).strip()
        print(f"Received data: {data.decode()}")
        self.request.sendall(data)

if __name__ == "__main__":
    server_ip   = "10.2.94.209"
    server_port = 1100
    server_address = (server_ip, server_port)  # Listen on all available network interfaces
    server = socketserver.TCPServer(server_address, MyTCPHandler)
    print(f"Server is listening on port {server_port}...")
    server.serve_forever()
