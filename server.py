# from prettytable import PrettyTable
import socketserver

class TCPHandler(socketserver.BaseRequestHandler):
    def recv_msg(self):
        block_size = 2048
        data = self.request.recv(block_size).strip()
        response = data.decode()
        # Log the received message to the console
        print(f"{self.client_address}: {data.decode()}")
        return response

    # communication protocol is such that first the size of the data is sent
    # and then the data itself is sent
    def send_msg(self, message):
        data = message.encode()
        size = f"{len(data)}"
        self.request.send(size.encode())
        if self.recv_msg() == "Ok":
            self.request.sendall(data)

    # Please don't sue me, I couldn't think of too many related questions,
    # So I drew inspiration from the CS@Ashoka Handbook v3
    # (Some answers are copy-pasted from there)
    def greet(self):
        greeting = """
    Welcome! Below is a list of queries related to the Computer Science major at Ashoka University.
    You can choose a question by typing the corresponding number.
    E.g: You want the core course list. In your prompt, enter "3" (without the quotes).
    ----------------------------------------------------------------------------------------------
    1.  What is the total number of CS credits required to complete the 4-year BSc Hons
            degree in CS?
    2.  Could you provide a breakdown of CS credits?
    3.  What are the core courses?
    4.  Can you give a list a pre-requisites for core courses?
    5.  What are some electives offered?
    6.  What is the Recommended Trajectory for a pure CS major?
    7.  What are ISMs? What is the CS department's policy on ISM credit?
    8.  What Internship and Research opportunities are availabe for undergraduates?
    9.  Awards and Recognitions by the CS department
    10. CS Representatives and Elections
    11. Clubs and Societies - CS@Ashoka
    12. Please give some advice on obtaining LORs from faculty.
    ----------------------------------------------------------------------------------------------
    Lastly, type "close" to close the connection.
        """
        self.send_msg(greeting)

    def handle(self):
        initial_message = self.recv_msg()
        self.greet()
        message = "meow"
        counter = 0
        while True:
            client_response = self.recv_msg()
            if client_response == "close":
                # self.request.sendall(b"Connection Closed")
                self.send_msg("Connection Closed")
                self.request.close()
                break
            else:
                counter += 1
                self.send_msg(f"{client_response} {message} {counter}")
                # self.request.sendall(f"{client_response} {message} {counter}".encode())

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
