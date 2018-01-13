import socket
import Server
import SaboteurModel as sm
import SaboteurView as sv
import pickle
import os


class Client:
    PLAYER_FILE_NAME = "Player_temp"

    def __init__(self, name, server_address):
        assert isinstance(name, str)
        self.local_player_file_name = Client.PLAYER_FILE_NAME + name
        self.view = []
        self.name = name
        self.server_address = server_address
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket')
            exit()

        try:
            self.remote_ip = socket.gethostbyname(self.server_address)

        except socket.gaierror:
            # could not resolve
            print('Hostname could not be resolved. Exiting')
            exit()

    def start(self):

        # connect to server
        self.client_socket.connect((self.remote_ip, Server.Server.PORT))
        try:
            # Send the whole name
            self.client_socket.send(self.name.encode())

        except socket.error:
            # Send failed
            print('Sendin the name failed')
            self.end_client()

        # Wait for server to be ready
        print("The player", self.name, " waits for the server to be ready")
        try:
            msg = self.client_socket.recv(64).decode()
            if msg == "END":
                print("Server has closed... \nExiting...")
                self.end_client()
            elif not msg == "START":
                print("Received \"", msg, "\" When START was expected...\ncommiting suicide...", sep="")
                self.end_client()
        except socket.error:
            print("Something went terribly wrong...")
            self.end_client()
        print("Server responded, revieving data now")

        # Setup view
        # Recieve player object
        player_file = open(self.local_player_file_name, "wb")
        try:
            msg = self.client_socket.recv(1024)
            if not msg:
                player_file.close()
                os.remove(self.local_player_file_name)
                print("No player data recieved... Suicide is the only oprion :'( ")
                self.end_client()
            player_file.write(msg)
        except socket.error:
            player_file.close()
            os.remove(self.local_player_file_name)
            print("Something went terribly wrong...")
            self.end_client()

        player_file.close()
        player_file = open(self.local_player_file_name, "rb")
        player = pickle.load(player_file)
        player_file.close()
        assert isinstance(player, sm.Player)
        print(player.name, player.saboteur)

        # cleanup
        os.remove(self.local_player_file_name)

        # self.view = sv.ViewController(player, board, player_names)

    def end_client(self):
        self.client_socket.close()
        exit()


c1 = Client("Test 1", "XtraSonic-PC")
c2 = Client("Test 2", "XtraSonic-PC")
c3 = Client("Test 3", "XtraSonic-PC")
c1.start()
c1.end_client()
# c2.start()
# c2.end_client()
# c3.start()
# c3.end_client()
