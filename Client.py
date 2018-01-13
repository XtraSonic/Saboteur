import socket
import Server
import SaboteurModel as sm
import SaboteurView as sv
import pickle
import os


def bytes_to_int(bytes_):
    result = 0
    for b in bytes_:
        result = result * 256 + int(b)
    return result


class Client:
    PLAYER_TEMP_FILE = "Player_temp"
    PLAYER_NAMES_TEMP_FILE = "Player_names_temp"
    BOARD_TEMP_FILE = "Player_names_temp"

    def __init__(self, name, server_address):
        assert isinstance(name, str)
        self.local_player_file = Client.PLAYER_TEMP_FILE + name
        self.local_player_names_file = Client.PLAYER_NAMES_TEMP_FILE + name
        self.local_board_file = Client.BOARD_TEMP_FILE + name
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
        player_file = open(self.local_player_file, "wb")
        try:
            msg_size = bytes_to_int(self.client_socket.recv(32))
            print("got the size", msg_size)
            msg = self.client_socket.recv(msg_size)
            if not msg:
                player_file.close()
                os.remove(self.local_player_file)
                print("No player data recieved... Suicide is the only oprion :'( ")
                self.end_client()
            player_file.write(msg)
        except socket.error:
            player_file.close()
            os.remove(self.local_player_file)
            print("Something went terribly wrong...")
            self.end_client()
        player_file.close()
        player_file = open(self.local_player_file, "rb")
        player = pickle.load(player_file)
        player_file.close()
        assert isinstance(player, sm.Player)
        print("Player obj received succesfully")
        # cleanup
        os.remove(self.local_player_file)

        # Recieve player names object
        player_name_file = open(self.local_player_names_file, "wb")
        try:
            msg_size = bytes_to_int(self.client_socket.recv(32))
            print("got the size", msg_size)
            msg = self.client_socket.recv(msg_size)
            if not msg:
                player_name_file.close()
                os.remove(self.local_player_names_file)
                print("No player names data recieved... Suicide is the only oprion :'( ")
                self.end_client()
            player_name_file.write(msg)
        except socket.error:
            player_name_file.close()
            os.remove(self.local_player_names_file)
            print("Something went terribly wrong...")
            self.end_client()
        player_name_file.close()
        player_name_file = open(self.local_player_names_file, "rb")
        player_names = pickle.load(player_name_file)
        player_name_file.close()
        assert isinstance(player_names, list)
        for el in player_names:
            assert isinstance(el, str)
        print("Player names obj received succesfully")
        # cleanup
        os.remove(self.local_player_names_file)

        # Recieve player names object
        board_file = open(self.local_board_file, "wb")
        try:
            msg_size = bytes_to_int(self.client_socket.recv(32))
            print("got the size", msg_size)
            msg = self.client_socket.recv(msg_size)
            if not msg:
                board_file.close()
                os.remove(self.local_board_file)
                print("No player names data recieved... Suicide is the only oprion :'( ")
                self.end_client()
            board_file.write(msg)
        except socket.error:
            board_file.close()
            os.remove(self.local_board_file)
            print("Something went terribly wrong...")
            self.end_client()
        board_file.close()
        board_file = open(self.local_board_file, "rb")
        board = pickle.load(board_file)
        board_file.close()
        assert isinstance(board, sm.Board)
        print("Board obj received succesfully")
        # cleanup
        os.remove(self.local_board_file)

        self.client_socket.send("READY".encode())

        self.view = sv.ViewController(player, board, player_names)
        self.view.view_game_loop()

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
