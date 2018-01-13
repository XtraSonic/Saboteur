import socket
import Server
import SaboteurModel as sm
import SaboteurView as sv
import pickle
import os
import threading


def bytes_to_int(bytes_):
    result = 0
    for b in bytes_:
        result = result * 256 + int(b)
    return result


class Client:
    PLAYER_TEMP_FILE = "Player_temp"
    PLAYER_NAMES_TEMP_FILE = "Player_names_temp"
    BOARD_TEMP_FILE = "Board_temp"
    CARD_TEMP_FILE = "Card_temp"

    ERROR_NOT_TURN = -1

    def __init__(self, name, server_address, remote_ip=None):
        assert isinstance(name, str)
        self.local_player_file = Client.PLAYER_TEMP_FILE + name
        self.local_player_names_file = Client.PLAYER_NAMES_TEMP_FILE + name
        self.local_board_file = Client.BOARD_TEMP_FILE + name
        self.local_card_file = Client.CARD_TEMP_FILE + name
        self.view = None
        """:type view: sv.ViewController"""
        self.name = name
        self.server_address = server_address
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket')
            exit()

        if remote_ip is None:
            try:
                self.remote_ip = socket.gethostbyname(self.server_address)
            except socket.gaierror:
                # could not resolve
                print('Hostname could not be resolved. Exiting')
                exit()
        else:
            self.remote_ip = remote_ip

    def initialize(self):

        # connect to server
        self.client_socket.connect((self.remote_ip, Server.Server.PORT))
        try:
            # Send the whole name
            self.client_socket.send(self.name.encode())

        except socket.error:
            # Send failed
            print('Sending the name failed')
            self.end_client()

        # Wait for server to be ready
        print("The player", self.name, " waits for the server to be ready")
        try:
            msg = self.client_socket.recv(64).decode()
            if msg == "END":
                print("Server has closed... \nExiting...")
                self.end_client()
            elif not msg == "START":
                print("Received \"", msg, "\" When START was expected...\n committing suicide...", sep="")
                self.end_client()
        except socket.error:
            print("Something went terribly wrong...")
            self.end_client()
        print("Server responded, receiving data now")

        # Setup view
        # Receive player object
        player_file = open(self.local_player_file, "wb")
        try:
            msg_size = bytes_to_int(self.client_socket.recv(32))
            print("got the size", msg_size)
            msg = self.client_socket.recv(msg_size)
            if not msg:
                player_file.close()
                os.remove(self.local_player_file)
                print("No player data received... Suicide is the only option :'( ")
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
        print("Player obj received successfully")
        # cleanup
        os.remove(self.local_player_file)

        # Receive player names object
        player_name_file = open(self.local_player_names_file, "wb")
        try:
            msg_size = bytes_to_int(self.client_socket.recv(32))
            print("got the size", msg_size)
            msg = self.client_socket.recv(msg_size)
            if not msg:
                player_name_file.close()
                os.remove(self.local_player_names_file)
                print("No player names data received... Suicide is the only option :'( ")
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
        print("Player names obj received successfully")
        # cleanup
        os.remove(self.local_player_names_file)

        # Receive player names object
        board_file = open(self.local_board_file, "wb")
        try:
            msg_size = bytes_to_int(self.client_socket.recv(32))
            print("got the size", msg_size)
            msg = self.client_socket.recv(msg_size)
            if not msg:
                board_file.close()
                os.remove(self.local_board_file)
                print("No board data received... Suicide is the only option :'( ")
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
        print("Board obj received successfully")
        # cleanup
        os.remove(self.local_board_file)

        self.client_socket.send("READY".encode())

        self.view = sv.ViewController(player, board, player_names, self)
        print("Client thread id=", threading.get_ident())
        # self.view.play_turn_loop()

    def listen_for_server_commands(self):
        while True:
            pass
            # msg = self.client_socket.recv(64).decode()
            # if msg == "YOUR TURN":
            #     print(self.name, "It is my turn")
            #     self.view.active = True
            # else:
            #     print("The server sent an unknown message:", msg)

    def make_discard_request(self, index):
        # send request
        message = "DISCARD," + str(index)
        print(self.name, "sending discard request:", message)
        self.client_socket.send(message.encode())

        # receive response
        message = self.client_socket.recv(64).decode()
        print(self.name, "got the response", message)
        if message == "OK":
            card = self.receive_card()
            self.view.update_hand(index, card)
            self.view.active = False
            return None
        elif message == "NOT YOUR TURN":
            print("Not my turn", self.name)
            return Client.ERROR_NOT_TURN
        else:
            print("UHM, Why am i here ?")
            return "WTF"

    def receive_card(self):
        print()
        card_temp_file = open(self.local_card_file, "wb")
        try:
            msg_size = bytes_to_int(self.client_socket.recv(32))
            print("got the size", msg_size)
            msg = self.client_socket.recv(msg_size)
            if not msg:
                card_temp_file.close()
                os.remove(self.local_card_file)
                print("No card data received... Suicide is the only option :'( ")
                self.end_client()
            card_temp_file.write(msg)
        except socket.error:
            card_temp_file.close()
            os.remove(self.local_card_file)
            print("Something went terribly wrong...")
            self.end_client()
        card_temp_file.close()
        card_temp_file = open(self.local_card_file, "rb")
        card = pickle.load(card_temp_file)
        card_temp_file.close()
        assert isinstance(card, sm.Card) or card is None
        print("Card obj received successfully", card)
        # cleanup
        os.remove(self.local_card_file)
        return card

    def end_client(self):
        self.client_socket.close()
        exit()

c1 = Client("Test 1", "DESKTOP-N1OHTUE", "192.168.0.213")
c2 = Client("Test 2", "DESKTOP-N1OHTUE", "192.168.0.213")
c3 = Client("Test 3", "DESKTOP-N1OHTUE", "192.168.0.213")
# c1.initialize()
# c1.listen_for_server_commands()
# c1.end_client()
c2.initialize()
c3.listen_for_server_commands()
c2.end_client()
# c3.initialize()
#c3.listen_for_server_commands()
# c3.end_client()