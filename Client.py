import socket
import Server


class Client:

    def __init__(self, name, server_address):
        assert isinstance(name, str)
        self.name = name
        self.server_address = server_address
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket')
            exit()

        try:
            self.remote_ip = socket.gethostbyname(server_address)

        except socket.gaierror:
            # could not resolve
            print('Hostname could not be resolved. Exiting')
            exit()

    def start(self):

        self.client_socket.connect((self.remote_ip, Server.Server.PORT))
        try:
            # Set the whole string
            self.client_socket.send(self.name.encode())

        except socket.error:
            # Send failed
            print('Send failed')
            exit()

        while True:
            msg = self.client_socket.recv(128)
            if msg == 0:
                break

        self.client_socket.close()


c = Client("Test 1", '192.168.0.104')
c.start()
